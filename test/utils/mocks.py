import pytest
from boto3 import client
from unittest.mock import patch
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

def create_mock_exc(message='', code=''):
    return ClientError({
        'Error': {
            'Message': message,
            'Code': code
        }
    }, 'any')

mock_bad_gateway_exc = create_mock_exc(message='Bad Gateway')
mock_condition_not_met_exc = create_mock_exc(code='ConditionalCheckFailedException')
mock_table_does_not_exist_exc = create_mock_exc(message='Cannot do operations on a non-existent table')
mock_preexisting_table_exc = create_mock_exc(message='Cannot create preexisting table')
mock_unknown_exc = create_mock_exc(message='nothing you ever heard of before')


class MockDynamoClient:
    def __init__(self):
        def do_nothing(*args, **kwargs):
            pass
        self.put_item = do_nothing
        self.create_table = do_nothing
        self.delete_item = do_nothing
        self.describe_table = do_nothing
        self.get_item = do_nothing
        self.query = do_nothing
        self.update_item = do_nothing
        self.scan = do_nothing

mock_dynamo_client = MockDynamoClient()
