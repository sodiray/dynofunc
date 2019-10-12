#!/usr/bin/env python

import json
from functools import partial
from boto3 import client

from dynamof.conditions import attr
from dynamof.executor import execute
from dynamof.operations import (
    create,
    find,
    add,
    update,
    delete,
    query
)

url = 'http://localstack:4569'
client = client('dynamodb', endpoint_url=url)
db = partial(execute, client)

debug = lambda msg: print(f'###########\n{msg}\n###########\n')
pprint = lambda data: print(json.dumps(data, indent=2))

def setup_test_tables():
    debug('Create Users Table')
    res = db(create(table_name='users', hash_key='username', allow_existing=True))
    pprint(res)


def run_tests():

    debug('Adding User')
    res = db(add(table_name='users', item={
        'id': 'aaaaaa',
        'username': 'sunshie'
    }))
    pprint(res)

    debug('Adding User')
    res = db(add(table_name='users', item={
        'id': 'aaaaaa',
        'username': 'sunshie'
    }))
    pprint(res)

    debug('Adding User')
    res = db(add(table_name='users', item={
        'id': 'aaaaaa',
        'username': 'sunshie'
    }))
    pprint(res)

    debug('Finding User')
    res = db(find(table_name='users', key={
        'username': 'sunshie'
    }))
    pprint(res)

    debug('Updating User')
    res = db(update(
        table_name='users',
        key={
            'username': 'sunshie'
        },
        attributes={
            'user_status': 'unleashed'
        }))
    pprint(res)

    debug('Querying users')
    res = db(query(
        table_name='users',
        conditions=attr('username').equals('sunshie')
    ))
    pprint(res)

    debug('Deleting User')
    res = db(delete(table_name='users', key={
        'username': 'sunshie'
    }))
    pprint(res)



if __name__ == '__main__':
    setup_test_tables()
    run_tests()
