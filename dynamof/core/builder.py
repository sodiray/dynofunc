from boto3.dynamodb.types import TypeSerializer

from dynamof.core.utils import guid, merge, update, pipe
from dynamof.core.model import AttributeGroup, Attribute, RequestTree
from dynamof.core.dynamo import DYNAMO_RESERVED_WORDS
from dynamof.core.Immutable import Immutable


def parse_attr(key, value):

    def make_attr(k, v):
        return Attribute(k, k, v, k, None)

    def replace_reserved_key(attr):
        """Finds reserved dynamo keywords in the attribute
        names and sets an alias the is safe to use instead"""
        alias = DYNAMO_RESERVED_WORDS.get(attr.original.upper(), None)
        if alias is not None:
            return update(attr, alias=alias)
        return attr

    def build_key(attr):
        """Builds the key that can be used to reference
        the attribute's value in an expression"""
        return update(attr, key=f':{attr.key}')

    def apply_function_values(attr):
        """Allows us to support passing a special Function as the
        value of the attribute. Here, if the value property is a
        Function we move it to the func property to be used later
        and call it to get the real value"""
        is_function = lambda val: isinstance(val, Immutable) and val.expression is not None and val.value is not None
        if is_function(attr.value):
            fn = attr.value
            return update(attr,
                func=fn,
                value=fn.value())
        return attr

    def build_value_type_tree(attr):
        """Last step in parsing pipeline, reads the value of the
        attribute and uses boto's serializer to convert it to that
        freaky tree with type indicators that dynamo requires"""
        return update(attr,
            value=TypeSerializer().serialize(attr.value))

    @pipe(make_attr)
    @pipe(replace_reserved_key)
    @pipe(build_key)
    @pipe(apply_function_values)
    @pipe(build_value_type_tree)
    def parse(a):
        return a

    return parse(key, value)

def builder(
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

    attrs = AttributeGroup(
        keys=[parse_attr(k, v) for k, v in key.items()],
        values=[parse_attr(k, v) for k, v in attributes.items()],
        conditions=[parse_attr(k, v) for k, v in condition_attrs.items()]
    )

    return lambda fn: fn(RequestTree(attrs, table_name, hash_key, conditions))

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
