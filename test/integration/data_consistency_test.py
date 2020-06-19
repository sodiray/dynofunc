import json
import pytest
from functools import partial
from boto3 import client

from test.integration.fixtures import db

from dynofunc import (
    create,
    find,
    add,
    update,
    delete,
    query
)

def test_numbers_are_not_changed(db):
    """Asserts that numbers inserted into dynamo are not converted
    to another type - **namely Decimals**. See https://github.com/boto/boto3/issues/369
    This test is to assert that dynofunc correctly handles this by converting
    any Decimals that dynamo returns back to a default json parsable property.
    """

    db(create(
        table_name='data_const',
        hash_key='id'))

    db(add(table_name='data_const', item={
        'id': 'aaaaaa',
        'prefrences': {
            'volume': 9
        }
    }))

    user = db(find(table_name='data_const', key={
        'id': 'aaaaaa'
    }))

    volume = user.item().get('prefrences').get('volume')

    assert volume == 9
    assert isinstance(volume, int)
