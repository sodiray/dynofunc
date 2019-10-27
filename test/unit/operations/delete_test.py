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
from dynamof.operations.delete import delete, run


def test_delete_is_operation():
    res = delete(table_name='users', key={ 'username': 'sunshie '})
    assertIsOperation(res)

def test_delete_creates_description_with_table_name():
    res = delete(table_name='users', key={ 'username': 'sunshie '})
    description = res.description
    assert description['TableName'] == 'users'


def test_run_delete_success():
    res = run(mock_dynamo_client, {})
    assertIsResponse(res)
