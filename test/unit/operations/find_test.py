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
from dynamof.operations.find import find, run


def test_find_is_operation():
    res = find(table_name='users', key={ 'username': 'sunshie '})
    assertIsOperation(res)

def test_find_creates_description_with_table_name():
    res = find(table_name='users', key={ 'username': 'sunshie '})
    description = res.description
    assert description['TableName'] == 'users'


def test_find_success():
    mock_client = MagicMock()
    mock_client.get_item.return_value = {}

    res = find(mock_client, {})

    assert res is not None

def test_run_find_success():
    res = run(mock_dynamo_client, {})
    assertIsResponse(res)
