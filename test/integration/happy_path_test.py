import json
import pytest
from functools import partial
from boto3 import client

from test.integration.fixtures import db

from dynamof.attribute import attr
from dynamof.operations import (
    create,
    find,
    add,
    update,
    delete,
    query
)

def test_happy_path(db):

    db(add(table_name='users', item={
        'id': 'aaaaaa',
        'username': 'sunshie'
    }))

    db(find(table_name='users', key={
        'username': 'sunshie'
    }))

    db(update(
        table_name='users',
        key={
            'username': 'sunshie'
        },
        attributes={
            'user_status': 'unleashed'
        }))

    db(query(
        table_name='users',
        conditions=attr('username').equals('sunshie')
    ))

    db(delete(table_name='users', key={
        'username': 'sunshie'
    }))
