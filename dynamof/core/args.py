"""Args is a collection of function that take in a request and return a specific
boto3 argument"""

from dynamof.core.model import RequestTree
from dynamof.core.utils import merge


def TableName(request: RequestTree):
    return request.table_name

def Key(request: RequestTree):
    """Creates the `Key` argument for a boto3 request description.
    @param request: ResultTree
    @return dict

    Example:

    return { 'id': { 'S': 'ab384020' }}
    """
    return merge([{
        key.alias: key.value
    } for key in request.attributes.keys])

def ConditionExpression(request: RequestTree):
    """Creates the `ConditionExpression` argument for a boto3 request description.
    @param request: ResultTree
    @return dict

    Example:

    return "Price > :limit"
    """
    if request.conditions is None:
        return None
    return request.conditions.expression(request.attributes.conditions)

def KeyConditionExpression(request: RequestTree):
    if request.conditions is None:
        return None
    return request.conditions.expression(request.attributes.conditions)

def UpdateExpression(request: RequestTree):
    def expression(attr):
        if attr.func is not None:
            return attr.func.expression(attr)
        return f'{attr.alias} = {attr.key}'
    key_expressions = [expression(key) for key in request.attributes.values]
    key_expression = ', '.join(key_expressions)
    return f'SET {key_expression}'

def ExpressionAttributeNames(request: RequestTree):
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

def Item(request: RequestTree):
    return merge([
        { attr.original: attr.value } for attr in request.attributes.values
    ])

def ExpressionAttributeValues(request: RequestTree):
    all_attributes = [
        *request.attributes.values,
        *request.attributes.conditions
    ]
    return {
        attr.key: attr.value for attr in all_attributes
    }

def KeySchema(request: RequestTree):
    schema = [
        {
            'AttributeName': request.hash_key,
            'KeyType': 'HASH'
        }
    ]
    if request.range_key is not None:
        schema.append({
            'AttributeName': request.range_key,
            'KeyType': 'RANGE'
        })
    return schema


def AttributeDefinitions(request: RequestTree):

    key_sources = [
        request.hash_key,
        request.range_key,
        *[i.get('range_key') for i in request.gsi or []],
        *[i.get('hash_key') for i in request.gsi or []],
        *[i.get('range_key') for i in request.lsi or []]
    ]

    return [{
        'AttributeName': key,
        'AttributeType': 'S'
    } for key in set(key_sources) if key is not None]

def ProvisionedThroughput(request: RequestTree): # pylint: disable=unused-argument
    return {
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }

def LocalSecondaryIndexes(request: RequestTree):

    def make_index(lsi):
        name = lsi.get('name')
        range_key = lsi.get('range_key', None)
        return {
            'IndexName': name,
            'KeySchema': [
                {
                    'AttributeName': request.hash_key,
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': range_key,
                    'KeyType': 'RANGE'
                }
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            }
        }

    if request.lsi is None:
        return None

    return [
        make_index(i) for i in request.lsi
    ]

def GlobalSecondaryIndexes(request: RequestTree):

    def make_index(gsi):
        name = gsi.get('name')
        hash_key = gsi.get('hash_key', None)
        range_key = gsi.get('range_key', None)
        throughput = gsi.get('throughput', 10)
        return {
            'IndexName': name,
            'KeySchema': [
                {
                    'AttributeName': name,
                    'KeyType': type
                } for name, type in [[hash_key, 'HASH'], [range_key, 'RANGE']] if name is not None
            ],
            'Projection': {
                'ProjectionType': 'ALL'
            },
            'ProvisionedThroughput': {
                'ReadCapacityUnits': throughput,
                'WriteCapacityUnits': throughput
            }
        }

    if request.gsi is None:
        return None

    return [
        make_index(i) for i in request.gsi
    ]

def IndexName(request: RequestTree):
    return request.index_name
