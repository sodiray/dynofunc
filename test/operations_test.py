import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from test.assertions import assertIsOperation

from dynamof.operations import (
    create,
    find,
    add,
    update,
    delete
)

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

def test_create_description_sets_attribute_definitions():
    res = create(table_name='users', hash_key='username')
    AttributeDefinitions = res.description['AttributeDefinitions']
    assert len(AttributeDefinitions) == 1
    definition_item = AttributeDefinitions[0]
    assert definition_item['AttributeName'] == 'username'
    assert definition_item['AttributeType'] == 'S'

def test_create_description_provisioned_throughputs():
    res = create(table_name='users', hash_key='username')
    ProvisionedThroughput = res.description['ProvisionedThroughput']
    assert ProvisionedThroughput['ReadCapacityUnits'] == 1
    assert ProvisionedThroughput['WriteCapacityUnits'] == 1



def test_find_is_operation():
    res = find(table_name='users', key={ 'username': 'rayepps '})
    assertIsOperation(res)

def test_find_creates_description_with_table_name():
    res = find(table_name='users', key={ 'username': 'rayepps '})
    description = res.description
    assert description['TableName'] == 'users'



def test_add_is_operation():
    res = add(table_name='users', item={ 'username': 'rayepps '})
    assertIsOperation(res)

def test_add_creates_description_with_table_name():
    res = add(table_name='users', item={ 'username': 'rayepps '})
    description = res.description
    assert description['TableName'] == 'users'

def test_add_creates_description_auto_incraments():
    res = add(table_name='users', item={ 'username': 'rayepps '}, auto_inc=True)
    description = res.description
    assert description['Item']['id'] is not None



def test_update_is_operation():
    res = update(table_name='users', key={ 'username': 'rayepps '}, attributes={ 'role': 'admin' })
    assertIsOperation(res)

def test_update_creates_description_with_table_name():
    res = update(table_name='users', key={ 'username': 'rayepps '}, attributes={ 'role': 'admin' })
    description = res.description
    assert description['TableName'] == 'users'



def test_delete_is_operation():
    res = delete(table_name='users', key={ 'username': 'rayepps '})
    assertIsOperation(res)

def test_delete_creates_description_with_table_name():
    res = delete(table_name='users', key={ 'username': 'rayepps '})
    description = res.description
    assert description['TableName'] == 'users'
