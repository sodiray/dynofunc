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

from dynofunc.core import exceptions

from dynofunc.attribute import attr, cand, cor
from dynofunc.operations.query import query, run

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

def test_run_query_success():
    res = run(mock_dynamo_client, {})
    assertIsResponse(res)
