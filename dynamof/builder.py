import decimal
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer


def update_expression(data):
    """Builds a string thats a dynamo friendly
    expression"""
    keys = [f'{key} = :{key}' for key, value in data.items()]
    key_expression = ', '.join(keys)
    return f'SET {key_expression}'

def expression_attribute_values(data):
    """Builds an object that contains ':'
    prepended to the key to make a dynamo
    friendly ExpressionAttributeValues"""
    values = value_type_tree(data)
    exp_values = {}
    for key, value in values.items():
        exp_values[f':{key}'] = value
    return exp_values


def condition_expression(id):
    key = 'id' # default
    if isinstance(id, dict):
        keys = list(id.keys())
        key = keys[0]
    return f'{key} = :{key}'

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
