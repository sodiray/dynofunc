import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from test.utils.assertions import assertIsOperation, assertObjectsEqual, assertIsResponse
from test.utils.mocks import (
    mock_bad_gateway_exc,
    mock_table_does_not_exist_exc,
    mock_unknown_exc,
    mock_dynamo_client
)

from dynamof.core import exceptions

from dynamof.attribute import attr, cand, cor
from dynamof.operations.create import create, run


def test_create_is_operation():
    res = create(table_name='users', hash_key='username')
    assertIsOperation(res)

def test_create_description_sets_table_name():
    res = create(table_name='users', hash_key='username')
    assert res.description['TableName'] == 'users'

def test_create_description_sets_key_schema():
    res = create(table_name='users', hash_key='username')
    KeySchema = res.description['KeySchema']
    assert len(KeySchema) == 1
    schema_item = KeySchema[0]
    assert schema_item['AttributeName'] == 'username'
    assert schema_item['KeyType'] == 'HASH'

def test_create_description_provisioned_throughputs():
    res = create(table_name='users', hash_key='username')
    ProvisionedThroughput = res.description['ProvisionedThroughput']
    assert ProvisionedThroughput['ReadCapacityUnits'] == 1
    assert ProvisionedThroughput['WriteCapacityUnits'] == 1

def test_run_create_success():
    res = run(mock_dynamo_client, {})
    assertIsResponse(res)
