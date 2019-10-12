import pytest
import json
import sys
import traceback
from unittest.mock import patch
from unittest.mock import MagicMock
from functools import partial
from boto3 import client

from test.integration.fixtures import db

from dynamof.conditions import attr
from dynamof.operations import (
    create,
    find,
    add,
    update,
    delete,
    query
)
from dynamof.exceptions import (
    UnknownDatabaseException,
    PreexistingTableException,
    ConditionNotMetException,
    BadGatewayException,
    TableDoesNotExistException
)

def test_add_throws_bad_gateway(db):
    with pytest.raises(BadGatewayException) as exc:
        db(add(
            table_name='does_not_exist_table',
            item={'id': 'aaaaaa'}))
    assert exc is not None

def test_find_throws_bad_gateway(db):
    with pytest.raises(TableDoesNotExistException) as exc:
        db(find(
            table_name='does_not_exist_table',
            key={'id': 'aaaaaa'}))
    assert exc is not None

def test_update_throws_bad_gateway(db):
    with pytest.raises(TableDoesNotExistException) as exc:
        db(update(
            table_name='does_not_exist_table',
            key={'id': 'aaaaaa'},
            attributes={'prop': 'val'}))
    assert exc is not None

def test_query_throws_bad_gateway(db):
    with pytest.raises(TableDoesNotExistException) as exc:
        db(query(
            table_name='does_not_exist_table',
            conditions=attr('name').equals('sunshie')))
    assert exc is not None
