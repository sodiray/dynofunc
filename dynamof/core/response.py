
from boto3.dynamodb.types import TypeDeserializer

from dynamof.core.utils import strip_Decimals, immutable


def destructure_type_tree(data):

    if data is None:
        return None

    # Using `strip_Decimals` here to patch an
    # undesireable behavior with dynamo where
    # it takes in number types but always returns
    # Decimal class type.
    # https://github.com/boto/boto3/issues/369

    return strip_Decimals({
        k: TypeDeserializer().deserialize(v) for k, v in data.items()
    })

def response(response):

    return immutable({

        'retries': lambda: response.get('ResponseMetadata', {}).get('RetryAttempts', None),

        'success': lambda: response.get('ResponseMetadata', {}).get('HTTPStatusCode', 0) == 200,

        'item': lambda: destructure_type_tree(response.get('Item', {})),

        'items': lambda: [destructure_type_tree(item) for item in response.get('Items', [])],

        'count': lambda: response.get('Count', None),

        'scanned_count': lambda: response.get('ScannedCount', None),

        'raw': lambda: response

    })
