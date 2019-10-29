import json
import pytest
from functools import partial
from boto3 import client

from test.integration.fixtures import db

from dynamof import attr, table, cand

def test_local_secondary_index(db):

    bookings = table(db, 'bookings')

    bookings.create(
        hash_key='id',
        range_key='type',
        lsi=[dict(
            name='rental_id_lsi',
            range_key='rental_type'
        )])

    bookings.add(item={
        'id': 'ba',
        'type': 'onetime',
        'rental_type': 'weekly'
    })

    bookings.add(item={
        'id': 'bb',
        'type': 'reocurring',
        'rental_type': 'monthly'
    })

    bookings.add(item={
        'id': 'bc',
        'type': 'onetime',
        'rental_type': 'annual'
    })

    books = bookings.query(
        index_name='rental_id_lsi',
        conditions=attr('id').equals('ba')
    )

    assert len(books.items()) == 1


def test_global_secondary_index(db):

    classes = table(db, 'classes')

    classes.create(
        hash_key='id',
        range_key='school',
        gsi=[dict(
            name='class_code_gsi',
            hash_key='class_code',
            range_key='school'
        )])

    classes.add(item={
        'id': 'ca',
        'school': 'osu',
        'class_code': 'TS340',
    })

    classes.add(item={
        'id': 'cb',
        'school': 'usc',
        'class_code': 'TS340',
    })

    classes.add(item={
        'id': 'cc',
        'school': 'harvard',
        'class_code': 'CS50',
    })

    classes.add(item={
        'id': 'cd',
        'school': 'usc',
        'class_code': 'RM201',
    })

    result = classes.query(
        index_name='class_code_gsi',
        conditions=cand(
            attr('class_code').equals('CS50'),
            attr('school').equals('harvard')
        )
    )

    assert len(result.items()) == 1
