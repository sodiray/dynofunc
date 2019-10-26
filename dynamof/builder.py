import json
import collections
import functools as ft
from boto3.dynamodb.types import TypeSerializer
import pydash as _

from dynamof.utils import new_id, shake, merge, update
from dynamof.funcs import Function
from dynamof.constants import DYNAMO_RESERVED_WORDS


def request_tree(operation_name, attributes, table_name, hash_key, conditions):
    return {
        'operation_name': operation_name,
        'attributes': attributes,
        'table_name': table_name,
        'hash_key': hash_key,
        'conditions': conditions
    }

def attribute_group(keys, values, conditions):
    return {
        'keys': keys,
        'values': values,
        'conditions': conditions
    }

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
    return {
        'original': original,
        'key': key,
        'value': value,
        'alias': alias,
        'func': func
    }

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
            auto_id: new_id()
        }

    def replace_reserved_key(attr):
        alias = DYNAMO_RESERVED_WORDS.get(attr.get('original').upper(), None)
        if alias is not None:
            return update(attr, alias=alias)
        return attr

    def build_key(attr):
        key = attr.get('key')
        return update(attr, key=f':{key}')

    def apply_function_values(attr):
        value = attr.get('value')
        if isinstance(value, Function):
            fn = value
            return update(attr,
                func=fn,
                value=fn.value())
        return attr

    def build_value_type_tree(attr):
        return update(attr,
            value=TypeSerializer().serialize(attr.get('value')))

    attribute_parsing_pipeline = [
        replace_reserved_key,
        build_key,
        apply_function_values,
        build_value_type_tree
    ]

    def pipeline(k, v):
        def caller(data, parser):
            return parser(data)
        return ft.reduce(caller, attribute_parsing_pipeline, attribute(k, k, v, k, None))

    attrs = attribute_group(
        keys=[pipeline(k, v) for k, v in key.items()],
        values=[pipeline(k, v) for k, v in attributes.items()],
        conditions=[pipeline(k, v) for k, v in condition_attrs.items()]
    )

    return lambda fn: fn(request_tree(operation_name, attrs, table_name, hash_key, conditions))

def TableName(request):
    return request.get('table_name')

def Key(request):
    """Creates the `Key` argument for a boto3 request description.
    @param request: ResultTree
    @return dict

    Example:

    return { 'id': { 'S': 'ab384020' }}
    """
    return merge([{
        key.get('alias'): key.get('value')
    } for key in _.get(request, 'attributes.keys')])

def ConditionExpression(request):
    """Creates the `ConditionExpression` argument for a boto3 request description.
    @param request: ResultTree
    @return dict

    Example:

    return "Price > :limit"
    """
    if request.get('conditions') is None:
        return None
    condition_attrs = _.get(request, 'attributes.conditions')
    return _.get(request, 'conditions.expression')(condition_attrs)

def KeyConditionExpression(request):
    if request.get('conditions') is None:
        return None
    condition_attrs = _.get(request, 'attributes.conditions')
    return _.get(request, 'conditions.expression')(condition_attrs)

def UpdateExpression(request):
    def expression(attr):
        fn = attr.get('func')
        if fn is not None:
            return fn.expression(attr)
        alias = attr.get('alias')
        key = attr.get('key')
        return f'{alias} = {key}'
    key_expressions = [expression(key) for key in _.get(request, 'attributes.values')]
    key_expression = ', '.join(key_expressions)
    return f'SET {key_expression}'

def ExpressionAttributeNames(request):
    all_attributes = [
        *_.get(request, 'attributes.keys'),
        *_.get(request, 'attributes.values'),
        *_.get(request, 'attributes.conditions')
    ]
    aliased_attributes = [attr for attr in all_attributes if attr.get('alias')[0] == '#']
    attr_names = {}
    for attr in aliased_attributes:
        attr_names[attr.get('alias')] = attr.get('original')
    return attr_names

def Item(request):
    return merge([
        { attr.get('original'): attr.get('value') } for attr in _.get(request, 'attributes.values')
    ])

def ExpressionAttributeValues(request):
    all_attributes = [
        # *_.get(request, 'attributes.keys'),
        *_.get(request, 'attributes.values'),
        *_.get(request, 'attributes.conditions')
    ]
    return {
        attr.get('key'): attr.get('value') for attr in all_attributes
    }

def KeySchema(request):
    return [{
        'AttributeName': request.get('hash_key'),
        'KeyType': 'HASH'
    }]


def AttributeDefinitions(request):
    return [{
        'AttributeName': request.get('hash_key'),
        'AttributeType': 'S'
    }]

def ProvisionedThroughput(request):
    return {
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }
