import numbers
from enum import Enum
from boto3.dynamodb.conditions import Key

def build_update_expression(data):
    """Builds a string thats a dynamo friendly
    expression"""
    keys = [f'{key} = :{key}' for key, value in data.items()]
    key_expression = ', '.join(keys)
    return f'SET {key_expression}'

def build_expression_attribute_values(data):
    """Builds an object that contains ':'
    prepended to the key to make a dynamo
    friendly ExpressionAttributeValues"""
    values = build_value_type_tree(data)
    exp_values = {}
    for key, value in values.items():
        exp_values[f':{key}'] = value
    return exp_values


def build_key(identifier):
    """Used to build the proper Key object
    for dynamo"""
    if isinstance(identifier, dict):
        return identifier
    else:
        return {
            'id': identifier # default to 'id' for primitives like string
        }

def build_condition_expression(id):
    key = 'id' # default
    if isinstance(id, dict):
        keys = list(id.keys())
        key = keys[0]
    return f'{key} = :{key}'

def build_key_schema(hash_key):
    return [{
        'AttributeName': hash_key,
        'KeyType': 'HASH'
    }]

def build_attribute_definitions(keys):
    return [{
        'AttributeName': key,
        'AttributeType': 'S'
    } for key in keys]

def build_provisioned_throughput():
    return {
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }

def detect_type(value):

    if value is None:
        return 'NULL' # null/none

    if isinstance(value, str):
        return 'S' # string

    if isinstance(value, bool):
        return 'BOOL' # boolean

    if isinstance(value, numbers.Number):
        return 'N' # number

    if isinstance(value, dict):
        return 'M' # map/dict

    if isinstance(value, list):
        return 'L' # list/array

    if isinstance(value, set):
        sub_types = [detect_type(item) for item in value]
        if all(st == 'S' for st in sub_types):
            return 'SS' # set that is all string type
        if all(st == 'N' for st in sub_types):
            return 'NS' # set that is all number type
        if all(st == 'B' for st in sub_types):
            return 'BS' # set that is all byte type
        return 'SS' # default to type string set

    if hasattr(value, 'decode'):
        return 'B'

def build_value_type_item(data):

    tree = {}
    data_type = detect_type(data)

    if data_type == 'L':
        tree[data_type] = [build_value_type_item(item) for item in data]
        return tree

    if data_type == 'M':
        tree[data_type] = build_value_type_tree(data)
        return tree

    if data_type == 'NULL':
        tree['NULL'] = True
        return tree

    if data_type in [ 'SS', 'NS', 'BS' ]:
        tree[data_type] = list(data)
        return tree

    tree[data_type] = data

    return tree

def build_value_type_tree(data):

    tree = {}
    for key, value in data.items():
        tree[key] = build_value_type_item(value)
    return tree

# def build_attribute_updates_tree(data):
