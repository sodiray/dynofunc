import pytest
from boto3 import client
from unittest.mock import patch
from unittest.mock import MagicMock

dynamo_client = client('dynamodb')

from dynamof.exceptions import PreexistingTableException
from dynamof.runners import (
    create,
    find,
    add,
    update,
    delete
)

def test_create_success():

    mock_client = MagicMock()
    mock_client.create_table.return_value = 'success'

    run = create(True)
    res = run(mock_client, {})

    assert res == 'success'

def test_create_ignores_table_created_exc():

    def mock_create_table():
        raise Exception('Cannot create preexisting table')

    mock_client = MagicMock()
    mock_client.create_table = mock_create_table

    # Allow existing
    run = create(True)
    res = run(mock_client, {})

    assert res == None

def test_create_raises_preexisting_table_exc():

    def mock_create_table():
        raise Exception('Cannot create preexisting table')

    mock_client = MagicMock()
    mock_client.create_table = mock_create_table

    with pytest.raises(PreexistingTableException):
        run = create(False)
        res = run(mock_client, {})

def test_find_success():
    mock_client = MagicMock()
    mock_client.get_item.return_value = 'success'

    run = find()
    res = run(mock_client, {})

    assert res == 'success'

def test_add_success():
    mock_client = MagicMock()
    mock_client.put_item.return_value = 'success'

    run = add()
    res = run(mock_client, {})

    assert res == 'success'

def test_update_success():
    mock_client = MagicMock()
    mock_client.update_item.return_value = 'success'

    run = update()
    res = run(mock_client, {})

    assert res == 'success'

def test_delete_success():
    mock_client = MagicMock()
    mock_client.delete_item.return_value = 'success'

    run = delete()
    res = run(mock_client, {})

    assert res == 'success'
