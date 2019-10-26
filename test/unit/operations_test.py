import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from test.utils.assertions import assertIsOperation, assertObjectsEqual

from dynamof.attribute import attr, cand, cor
from dynamof.core.utils import immutable
from dynamof.operations import (
    create,
    find,
    add,
    update,
    delete,
    query
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

def test_create_description_provisioned_throughputs():
    res = create(table_name='users', hash_key='username')
    ProvisionedThroughput = res.description['ProvisionedThroughput']
    assert ProvisionedThroughput['ReadCapacityUnits'] == 1
    assert ProvisionedThroughput['WriteCapacityUnits'] == 1

def test_find_is_operation():
    res = find(table_name='users', key={ 'username': 'sunshie '})
    assertIsOperation(res)

def test_find_creates_description_with_table_name():
    res = find(table_name='users', key={ 'username': 'sunshie '})
    description = res.description
    assert description['TableName'] == 'users'

def test_add_is_operation():
    res = add(table_name='users', item={ 'username': 'sunshie '})
    assertIsOperation(res)

def test_add_creates_description_with_table_name():
    res = add(table_name='users', item={ 'username': 'sunshie '})
    description = res.description
    assert description['TableName'] == 'users'

def test_add_creates_description_auto_id():
    res = add(table_name='users', item={ 'username': 'sunshie '}, auto_id='id')
    description = res.description
    assert description['Item']['id'] is not None

def test_update_is_operation():
    res = update(table_name='users', key={ 'username': 'sunshie '}, attributes={ 'role': 'admin' })
    assertIsOperation(res)

def test_update_creates_description_with_table_name():
    res = update(table_name='users', key={ 'username': 'sunshie '}, attributes={ 'role': 'admin' })
    description = res.description
    assert description['TableName'] == 'users'

def test_update_creates_description_with_Function():
    res = update(
        table_name='users',
        key={ 'username': 'sunshie' },
        attributes={
            'roles': attr.append('admin'),
            'friends': attr.prepend('rainbo')
        })
    assert 'list_append(#roles, :roles)' in res.description['UpdateExpression']

def test_update_with_conditions():
    res = update(
        table_name='users',
        key={ 'username': 'sunshie' },
        conditions=attr('rank').lt(2),
        attributes={ 'rank': 10 })
    condition_expression = res.description['ConditionExpression']
    assert condition_expression is not None
    assert condition_expression == '#rank < :rank'


def test_delete_is_operation():
    res = delete(table_name='users', key={ 'username': 'sunshie '})
    assertIsOperation(res)

def test_delete_creates_description_with_table_name():
    res = delete(table_name='users', key={ 'username': 'sunshie '})
    description = res.description
    assert description['TableName'] == 'users'


def test_query_is_operation():
    res = query(
        table_name='users',
        conditions=attr('username').equals('sunshie')
    )
    assertIsOperation(res)

def test_query_builds_basic_description():
    result = query(
        table_name='users',
        conditions=attr('username').equals('sunshie')
    )
    expected = {
        'TableName': 'users',
        'KeyConditionExpression': 'username = :username',
        'ExpressionAttributeValues': {
            ':username': {
                'S': 'sunshie'
            }
        }
    }
    assertObjectsEqual(result.description, expected)

def test_query_builds_aliased_attr_description():
    result = query(
        table_name='users',
        conditions=attr('item').equals('carl')
    )
    expected = {
        'TableName': 'users',
        'KeyConditionExpression': '#item = :item',
        'ExpressionAttributeNames': {
            '#item': 'item'
        },
        'ExpressionAttributeValues': {
            ':item': {
                'S': 'carl'
            }
        }
    }
    assertObjectsEqual(result.description, expected)

def test_query_handles_none_condition():
    result = query(table_name='users', conditions=None)
