

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
    res = {}
    for key, value in data.items():
        res[f':{key}'] = value
    return res

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
    attribute_name = 'id' # default
    attribute_value = id # default
    if isinstance(id, dict):
        keys = list(id.keys())
        attribute_name = keys[0]
        attribute_value = id[keys[0]]
    return {
        "name": attribute_name,
        "value": attribute_value
    }

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
