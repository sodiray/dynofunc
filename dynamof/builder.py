from boto3.dynamodb.types import TypeSerializer

from dynamof.utils import guid, merge, update, immutable
from dynamof.funcs import Function
from dynamof.constants import DYNAMO_RESERVED_WORDS


def request_tree(operation_name, attributes, table_name, hash_key, conditions):
    return immutable({
        'operation_name': operation_name,
        'attributes': attributes,
        'table_name': table_name,
        'hash_key': hash_key,
        'conditions': conditions
    })

def attribute_group(keys, values, conditions):
    return immutable({
        'keys': keys,
        'values': values,
        'conditions': conditions
    })

def attribute(original, key, value, alias, func):
    """
    Parameters
    ----------
    original : str
        The orignial name the client passed us for the attribute.
        Should never change for later references

        Ex. { 'item': 'a' } => 'item'


    key : str
        The key we should use in expressions to refer to the value
        of this attribute

        Ex. { 'item': 'a' } => ':item'

    value : dict
        The typed value of the attribute. NOTE: The attribute name should
        be stripped out so only the object defining the value/type is stored
        here. Different operations will use this and some will need to set a
        custom key so here were only storing the value of the value/type tree

        Ex. { 'item': 'a' } => { 'S': 'a' }

    alias : str
        The name we should use when refering to the dynamodb _column_. Typically
        this will be the same as `original`. However, in the case of reserved attr
        names it will be updated to something dynamodb friendly

        Ex. { 'item': 'a' } => '#item'

    func : Function
        A func from `dynamof.funcs` that should be called to modify the attr
    """
    return immutable({
        'original': original,
        'key': key,
        'value': value,
        'alias': alias,
        'func': func
    })

def parse_attr(a_attribute):

    def replace_reserved_key(func):
        """Finds reserved dynamo keywords in the attribute
        names and sets an alias the is safe to use instead"""
        def wrapper(attr):
            alias = DYNAMO_RESERVED_WORDS.get(attr.original.upper(), None)
            if alias is not None:
                return func(update(attr, alias=alias))
            return func(attr)
        return wrapper

    def build_key(func):
        """Builds the key that can be used to reference
        the attribute's value in an expression"""
        def wrapper(attr):
            return func(update(attr, key=f':{attr.key}'))
        return wrapper

    def apply_function_values(func):
        """Allows us to support passing a special Function as the
        value of the attribute. Here, if the value property is a
        Function we move it to the func property to be used later
        and call it to get the real value"""
        def wrapper(attr):
            if isinstance(attr.value, Function):
                fn = attr.value
                return func(update(attr,
                    func=fn,
                    value=fn.value()))
            return func(attr)
        return wrapper

    def build_value_type_tree(func):
        """Last step in parsing pipeline, reads the value of the
        attribute and uses boto's serializer to convert it to that
        freaky tree with type indicators that dynamo requires"""
        def wrapper(attr):
            return func(update(attr,
                value=TypeSerializer().serialize(attr.value)))
        return wrapper

    @replace_reserved_key
    @build_key
    @apply_function_values
    @build_value_type_tree
    def parse(a):
        return a

    return parse(a_attribute)

def builder(
    operation_name,
    table_name,
    key=None,
    attributes=None,
    conditions=None,
    hash_key=None,
    auto_id=None):

    key = key or {}
    attributes = attributes or {}
    condition_attrs = conditions.attributes if conditions is not None else {}

    if auto_id is not None:
        attributes = {
            **attributes,
            auto_id: guid()
        }

    attrs = attribute_group(
        keys=[parse_attr(attribute(k, k, v, k, None)) for k, v in key.items()],
        values=[parse_attr(attribute(k, k, v, k, None)) for k, v in attributes.items()],
        conditions=[parse_attr(attribute(k, k, v, k, None)) for k, v in condition_attrs.items()]
    )

    return lambda fn: fn(request_tree(operation_name, attrs, table_name, hash_key, conditions))

def TableName(request):
    return request.table_name

def Key(request):
    """Creates the `Key` argument for a boto3 request description.
    @param request: ResultTree
    @return dict

    Example:

    return { 'id': { 'S': 'ab384020' }}
    """
    return merge([{
        key.alias: key.value
    } for key in request.attributes.keys])

def ConditionExpression(request):
    """Creates the `ConditionExpression` argument for a boto3 request description.
    @param request: ResultTree
    @return dict

    Example:

    return "Price > :limit"
    """
    if request.conditions is None:
        return None
    return request.conditions.expression(request.attributes.conditions)

def KeyConditionExpression(request):
    if request.conditions is None:
        return None
    return request.conditions.expression(request.attributes.conditions)

def UpdateExpression(request):
    def expression(attr):
        if attr.func is not None:
            return attr.func.expression(attr)
        return f'{attr.alias} = {attr.key}'
    key_expressions = [expression(key) for key in request.attributes.values]
    key_expression = ', '.join(key_expressions)
    return f'SET {key_expression}'

def ExpressionAttributeNames(request):
    all_attributes = [
        *request.attributes.keys,
        *request.attributes.values,
        *request.attributes.conditions
    ]
    aliased_attributes = [attr for attr in all_attributes if attr.alias[0] == '#']
    attr_names = {}
    for attr in aliased_attributes:
        attr_names[attr.alias] = attr.original
    return attr_names

def Item(request):
    return merge([
        { attr.original: attr.value } for attr in request.attributes.values
    ])

def ExpressionAttributeValues(request):
    all_attributes = [
        *request.attributes.values,
        *request.attributes.conditions
    ]
    return {
        attr.key: attr.value for attr in all_attributes
    }

def KeySchema(request):
    return [{
        'AttributeName': request.hash_key,
        'KeyType': 'HASH'
    }]


def AttributeDefinitions(request):
    return [{
        'AttributeName': request.hash_key,
        'AttributeType': 'S'
    }]

def ProvisionedThroughput(request): # pylint: disable=unused-argument
    return {
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
