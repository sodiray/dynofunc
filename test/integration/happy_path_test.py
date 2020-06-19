import json
import pytest
from functools import partial
from boto3 import client

from test.integration.fixtures import db

from dynofunc import attr
from dynofunc import (
    create,
    find,
    add,
    update,
    delete,
    query,
    describe
)

def test_happy_path(db):

    db(add(table_name='users', item={
        'id': 'aaaaaa',
        'username': 'sunshie'
    }))

    db(describe(table_name='users'))

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
