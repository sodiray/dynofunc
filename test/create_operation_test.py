import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from test.assertions import assertIsOperation

from dynamof.operations import create

def test_create_is_operation():
    res = create(table_name='users', hash_key='username')
    assertIsOperation(res)

def test_create_description_key_schema():
    res = create(table_name='users', hash_key='username')
    assert res['description']['TableName'] == 'users'


def test_create_description_key_schema():
    res = create(table_name='users', hash_key='username')
    KeySchema = res['description']['KeySchema']
    assert len(KeySchema) == 1
    schema_item = KeySchema[0]
    assert schema_item['AttributeName'] == 'username'
    assert schema_item['KeyType'] == 'HASH'

def test_create_description_key_schema():
    res = create(table_name='users', hash_key='username')
    AttributeDefinitions = res['description']['AttributeDefinitions']
    assert len(AttributeDefinitions) == 1
    definition_item = AttributeDefinitions[0]
    assert definition_item['AttributeName'] == 'username'
    assert definition_item['AttributeType'] == 'S'

def test_create_description_provisioned_throughputs():
    res = create(table_name='users', hash_key='username')
    ProvisionedThroughput = res['description']['ProvisionedThroughput']
    assert ProvisionedThroughput['ReadCapacityUnits'] == 1
    assert ProvisionedThroughput['WriteCapacityUnits'] == 1
