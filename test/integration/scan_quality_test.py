import json
import pytest
from functools import partial
from boto3 import client

from test.integration.fixtures import db

from dynamof import attr
from dynamof import (
    create,
    find,
    add,
    update,
    delete,
    query,
    scan,
    describe
)

def test_scan_gets_all_items(db):

    db(create(table_name='it_companies', hash_key='name'))

    add_company = lambda name: db(add(table_name='it_companies', item={ 'name': name }))

    scanners = [ 'Apple', 'Microsoft', 'Google', 'Tesla', 'IBM', 'GM' ]

    for x in scanners:
        add_company(x)

    results = db(scan(table_name='it_companies')).items()

    assert len(results) == len(scanners)
