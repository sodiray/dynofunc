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
from dynamof.operations.update import update, run


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

def test_run_update_success():
    res = run(mock_dynamo_client, {})
    assertIsResponse(res)
