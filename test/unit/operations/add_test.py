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
from dynofunc.operations.add import add, run


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

def test_add_success():
    mock_client = MagicMock()
    mock_client.put_item.return_value = {}

    res = add(mock_client, {})

    assert res is not None

def test_run_add_success():
    res = run(mock_dynamo_client, {})
    assertIsResponse(res)
