"""Args is a collection of function that take in a request and return a specific
boto3 argument"""

from dynamof.core.model import RequestTree
from dynamof.core.utils import merge, immutable
from dynamof.core.dynamo import get_safe_alias


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

    if request.conditions is not None and request.conditions.references is not None:
        for ref in request.conditions.references:
            aliased_attributes.append(immutable({
                'alias': get_safe_alias(ref),
                'original': ref
            }))

    return { attr.alias: attr.original for attr in aliased_attributes }

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
            'AttributeName': request.hash_key.get('name'),
            'KeyType': 'HASH'
        }
    ]
    if request.range_key is not None:
        schema.append({
            'AttributeName': request.range_key.get('name'),
            'KeyType': 'RANGE'
        })
    return schema


def AttributeDefinitions(request: RequestTree):
    '''Finds all the hash keys and range keys in the given
    request (including indexes) and sets them in the boto
    standard AttributeDefinitions argument model. Also, looks
    for type annotations in the key names ('key_name:str' or 'key_name:int'),
    strips them from the name, and uses them to set the AttributeType.'''

    remove_duplicates = lambda list_of_keys: [dict(t) for t in {tuple(d.items()) for d in list_of_keys}]
    remove_nones = lambda list_of_keys: [k for k in list_of_keys if k is not None]

    all_keys = remove_duplicates(remove_nones([
        request.hash_key,
        request.range_key,
        *[i.get('range_key') for i in request.gsi or []],
        *[i.get('hash_key') for i in request.gsi or []],
        *[i.get('range_key') for i in request.lsi or []]
    ]))

    return [{
        'AttributeName': key.get('name'),
        'AttributeType': key.get('type')
    } for key in all_keys]

def ProvisionedThroughput(request: RequestTree): # pylint: disable=unused-argument
    return {
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }

def LocalSecondaryIndexes(request: RequestTree):

    def make_index(lsi):
        name = lsi.get('name')
        range_key = lsi.get('range_key').get('name')
        hash_key = request.hash_key.get('name')
        return {
            'IndexName': name,
            'KeySchema': [
                {
                    'AttributeName': hash_key,
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
        hash_key = gsi.get('hash_key').get('name')
        range_key = gsi.get('range_key', {}).get('name', None)
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
