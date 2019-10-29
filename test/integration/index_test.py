import json
import pytest
from functools import partial
from boto3 import client

from test.integration.fixtures import db

from dynamof import attr, table

def test_secondary_indexes(db):

    bookings = table(db, 'bookings')

    bookings.create(
        hash_key='id',
        range_key='type',
        lsi=[dict(
            name='rental_id_lsi',
            range_key='rental_type'
        )])

    classes = table(db, 'classes')

    classes.create(
        hash_key='id',
        range_key='school',
        gsi=[dict(
            name='class_code_gsi',
            hash_key='class_code',
            range_key='school'
        )])
