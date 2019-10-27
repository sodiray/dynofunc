import pytest
from boto3 import client
from unittest.mock import patch
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

from dynamof.exceptions import (
    UnknownDatabaseException,
    PreexistingTableException,
    ConditionNotMetException,
    BadGatewayException,
    TableDoesNotExistException
)
from dynamof.runners import (
    create,
    find,
    add,
    update,
    delete,
    query,
    describe
)


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


##
## CREATE
##

def test_create_success():

    mock_client = MagicMock()
    mock_client.create_table.return_value = {}

    res = create(mock_client, {})

    assert res is not None

def test_create_raises_preexisting_table_exc():

    def mock_create_table():
        raise mock_preexisting_table_exc

    mock_client = MagicMock()
    mock_client.create_table = mock_create_table

    with pytest.raises(PreexistingTableException):
        res = create(mock_client, {})

def test_create_raises_unknown_exc():

    def mock_create_table():
        raise mock_unknown_exc

    mock_client = MagicMock()
    mock_client.create_table = mock_create_table

    with pytest.raises(UnknownDatabaseException):
        res = create(mock_client, {})

##
## FIND
##

def test_find_success():
    mock_client = MagicMock()
    mock_client.get_item.return_value = {}

    res = find(mock_client, {})

    assert res is not None

def test_find_raises_bad_gateway_exc():

    def mock_get_item():
        raise mock_bad_gateway_exc

    mock_client = MagicMock()
    mock_client.get_item = mock_get_item

    with pytest.raises(BadGatewayException):
        res = find(mock_client, {})

def test_find_raises_table_does_not_exist_exc():

    def mock_get_item():
        raise mock_table_does_not_exist_exc

    mock_client = MagicMock()
    mock_client.get_item = mock_get_item

    with pytest.raises(TableDoesNotExistException):
        res = find(mock_client, {})

def test_find_raises_condition_not_met_exc():

    def mock_get_item():
        raise mock_condition_not_met_exc

    mock_client = MagicMock()
    mock_client.get_item = mock_get_item

    with pytest.raises(ConditionNotMetException):
        res = find(mock_client, {})

def test_find_raises_unknown_exc():

    def mock_get_item():
        raise mock_unknown_exc

    mock_client = MagicMock()
    mock_client.get_item = mock_get_item

    with pytest.raises(UnknownDatabaseException):
        res = find(mock_client, {})

##
## ADD
##

def test_add_success():
    mock_client = MagicMock()
    mock_client.put_item.return_value = {}

    res = add(mock_client, {})

    assert res is not None

def test_add_raises_bad_gateway_exc():

    def mock_put_item():
        raise mock_bad_gateway_exc

    mock_client = MagicMock()
    mock_client.put_item = mock_put_item

    with pytest.raises(BadGatewayException):
        res = add(mock_client, {})

def test_add_raises_table_does_not_exist_exc():

    def mock_put_item():
        raise mock_table_does_not_exist_exc

    mock_client = MagicMock()
    mock_client.put_item = mock_put_item

    with pytest.raises(TableDoesNotExistException):
        res = add(mock_client, {})

def test_add_raises_unknown_exc():

    def mock_put_item():
        raise mock_unknown_exc

    mock_client = MagicMock()
    mock_client.put_item = mock_put_item

    with pytest.raises(UnknownDatabaseException):
        res = add(mock_client, {})

##
## UPDATE
##

def test_update_success():
    mock_client = MagicMock()
    mock_client.update_item.return_value = {}

    res = update(mock_client, {})

    assert res is not None

def test_update_raises_unknown_exc():

    def mock_update_item():
        raise mock_unknown_exc

    mock_client = MagicMock()
    mock_client.update_item = mock_update_item

    with pytest.raises(UnknownDatabaseException):
        res = update(mock_client, {})

##
## DELETE
##

def test_delete_success():
    mock_client = MagicMock()
    mock_client.delete_item.return_value = {}

    res = delete(mock_client, {})

    assert res is not None

def test_delete_raises_unknown_exc():

    def mock_delete_item():
        raise mock_unknown_exc

    mock_client = MagicMock()
    mock_client.delete_item = mock_delete_item

    with pytest.raises(UnknownDatabaseException):
        res = delete(mock_client, {})

##
## QUERY
##

def test_query_success():
    mock_client = MagicMock()
    mock_client.delete_item.return_value = {}

    res = query(mock_client, {})

    assert res is not None

def test_query_raises_unknown_exc():

    def mock_query():
        raise mock_unknown_exc

    mock_client = MagicMock()
    mock_client.query = mock_query

    with pytest.raises(UnknownDatabaseException):
        res = query(mock_client, {})

##
## DESCRIBE
##

def test_describe_success():
    mock_client = MagicMock()
    mock_client.describe_table.return_value = {}

    res = describe(mock_client, {})

    assert res is not None

def test_describe_raises_unknown_exc():

    def mock_describe():
        raise mock_unknown_exc

    mock_client = MagicMock()
    mock_client.describe_table = mock_describe

    with pytest.raises(UnknownDatabaseException):
        res = describe(mock_client, {})
