import json
import pytest
from decimal import Decimal
from functools import partial
from boto3 import client

from test.integration.fixtures import db

from dynamof import attr
from dynamof import table

def test_secondary_index(db):

    orders = table(db, 'orders')

    orders.create(hash_key='order_id')
    orders.describe()

    orders.add(item={
        'order_id': 'a',
        'total': Decimal(str(24.22)),
        'products': [
            { 'name': 'Unicorn Glitter Headband' }
        ]
    })

    orders.find(key={
        'order_id': 'a'
    })

    orders.update(
        key={
            'order_id': 'a'
        },
        attributes={
            'total': 0,
            'notes': 'comped'
        })

    orders.query(
        conditions=attr('order_id').equals('a')
    )

    orders.delete(key={
        'order_id': 'a'
    })
