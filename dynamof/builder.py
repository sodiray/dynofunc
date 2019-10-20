import decimal
import json
import collections
import functools as ft
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

from dynamof.utils import new_id
from dynamof.funcs import Function
from dynamof.constants import DYNAMO_RESERVED_WORDS


ResultTree = collections.namedtuple("ResultTree", [
    "attributes",
    "table_name",
    "conditions"
])

AttributeGroup = collections.namedtuple("AttributeGroup", [
    "keys",
    "values",
    "conditions"
])

class Attribute:
    """Describes an item's key value relationships as it maps to dynamo
    This is needed because a caller may pass:
    {
      'item': [ 'a']
    }
    as an attribute (either key or attribute) but it goes to dynamo as:
    {
      ':item': {
        'L': [
          { 'S': 'a' }
        ]
      }
    }
    This DTO keeps track of these different changes and mappings so many different
    functions can have the correct/same refrence to attributes.
    NOTE: Making a class immutable in python is a pain... so please just don't
    mutate the items in this class. use `update` instead.
    """
    def __init__(self, original, key, value, alias=None, expression=None):
        self.original = original        # { 'item': 'a' } => 'item'
        self.key = key                  # { 'item': 'a' } => ':item'
        self.value = value              # { 'item': 'a' } => { 'S': 'a' }
        self.alias = alias              # { 'item': 'a' } => '#item'
        self.expression = expression    # { 'item': 'a' } => '#item = :item'
    def update(self, key=None, value=None, alias=None, expression=None):
        return Attribute(
            original=self.original,
            key=key or self.key,
            value=value or self.value,
            alias=alias or self.alias,
            expression=expression or self.expression)
    def __str__(self):
        return json.dumps(self.__dict__, indent=2) # pragma: no cover



def build_request_tree(
    table_name,
    key=None,
    attributes=None,
    conditions=None,
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
        alias = DYNAMO_RESERVED_WORDS.get(attr.key.upper(), None)
        if alias is not None:
            return attr.update(alias=alias)
        return attr

    def build_key(attr):
        return attr.update(key=f':{attr.key}')

    def build_expression(attr):
        attr_name = attr.alias or attr.original
        if isinstance(attr.value, Function):
            expression = attr.value.make_expression(attr_name, attr.key)
            value = attr.value.make_value()
            return attr.update(expression=expression, value=value)
        expression = f'{attr_name} = {attr.key}'
        return attr.update(expression=expression)

    def build_value_type_tree(attr):
        return attr.update(value=value_type_tree({
            f'{attr.key}': attr.value
        }))

    attribute_parsing_pipeline = [
        replace_reserved_key,
        build_key,
        build_expression,
        build_value_type_tree
    ]

    def pipeline(k, v):
        def caller(data, parser):
            return parser(data)
        return ft.reduce(caller, attribute_parsing_pipeline, Attribute(k, k, v))

    attrs = AttributeGroup(
        [pipeline(k, v) for k, v in key.items()],
        [pipeline(k, v) for k, v in attributes.items()],
        [pipeline(k, v) for k, v in condition_attrs.items()]
    )

    return ResultTree(attrs, table_name, conditions)




def build_key_arg(request):
    key_obj = {}
    for key_attr in request.attributes.keys:
        key_obj[key_attr.original] = key_attr.value
    return key_obj

def build_condition_expression(request):
    if request.conditions is None:
        return None
    return request.conditions.expression

def build_update_expression(request):
    key_expressions = [key.expression for key in request.attributes.values]
    key_expression = ', '.join(key_expressions)
    return f'SET {key_expression}'

def build_expression_attribute_names(request):
    # --expression-attribute-names '{"#ri": "RelatedItems"}'
    all_attributes = [*request.attributes.keys, *request.attributes.values, *request.attributes.conditions]
    aliased_attributes = [attr for attr in all_attributes if attr.alias is not None]
    attr_names = {}
    for attr in aliased_attributes:
        attr_names[attr.alias] = attr.original
    return attr_names

def build_expression_attribute_values(request):
    values = [{ attr.original: attr.value } for attr in request.attributes.values]
    return dict(collections.ChainMap(*values))






def key_schema(hash_key):
    return [{
        'AttributeName': hash_key,
        'KeyType': 'HASH'
    }]

def attribute_definitions(keys):
    return [{
        'AttributeName': key,
        'AttributeType': 'S'
    } for key in keys]

def provisioned_throughput():
    return {
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }

def deep_strip_Decimals(obj):
    """Patches an issue with dynamo where it takes in number
    types but always returns Decimal class type.
    https://github.com/boto/boto3/issues/369
    """
    if isinstance(obj, list):
        return [deep_strip_Decimals(item) for item in obj]
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = deep_strip_Decimals(v)
        return obj
    if isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        return float(obj)
    return obj

def value_type_tree(data):

    if data is None:
        return None

    s = TypeSerializer()

    result = {}
    for key, val in data.items():
        result[key] = s.serialize(val)

    return result

def destructure_type_tree(data):

    if data is None:
        return None

    d = TypeDeserializer()

    result = {}

    for key, val in data.items():
        result[key] = d.deserialize(val)

    return deep_strip_Decimals(result)
