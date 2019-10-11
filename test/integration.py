#!/usr/bin/env python

from functools import partial
from boto3 import resource, client

from dynamof.executor import execute
from dynamof.operations import (
    create,
    find,
    add,
    update,
    delete
)

url = 'http://localstack:4569'
db = partial(execute, url)

debug = lambda msg: print(f'###########\n{msg}\n###########\n')

def setup_test_tables():
    debug('Create Users Table')
    db(create(table_name='users', hash_key='username', allow_existing=True))


def run_tests():

    debug('Adding User')
    db(add(table_name='users', item={
        'username': 'sunshie'
    }))

    debug('Finding User')
    db(find(table_name='users', key={
        'username': 'sunshie'
    }))

    debug('Updating User')
    db(update(
        table_name='users',
        key={
            'username': 'sunshie'
        },
        attributes={
            'user_status': 'unleashed'
        }))

    debug('Deleting User')
    db(delete(table_name='users', key={
        'username': 'sunshie'
    }))



if __name__ == '__main__':
    setup_test_tables()
    run_tests()
