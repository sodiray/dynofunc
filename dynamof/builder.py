import numbers


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

def detect_type(value): # pylint: disable=too-many-return-statements

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
        return 'SS' # default to type string set for mixed types

    if hasattr(value, 'decode'):
        return 'B'

    return 'S' # if for some reason the type could not be detected default to string

def value_type_item(data):

    tree = {}
    data_type = detect_type(data)

    # If its a list - build a tree item for each item
    if data_type == 'L':
        tree[data_type] = [value_type_item(item) for item in data]
        return tree

    # If its a map/dict - build a tree for each attribute
    if data_type == 'M':
        tree[data_type] = value_type_tree(data)
        return tree

    if data_type == 'NULL':
        tree['NULL'] = True
        return tree

    # If its a set - convert it to a list (boto3 friendly)
    if data_type in [ 'SS', 'NS', 'BS' ]:
        tree[data_type] = list(data)
        return tree

    # For the rest of the simple types
    tree[data_type] = data

    return tree

def value_type_tree(data):

    tree = {}
    for key, value in data.items():
        tree[key] = value_type_item(value)
    return tree

def destructure_type_tree(data):
    if data is None:
        return None
    result = {}
    for key_name, type_obj in data.items():
        result = {
            **result,
            key_name: list(type_obj.values())[0]
        }
    return result
