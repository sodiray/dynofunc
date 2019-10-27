#!/usr/bin/env python

import time

import pytest

from test.integration.fixtures import db_func

from dynamof.core.exceptions import TableDoesNotExistException
from dynamof import create, describe

DATABASE_UPTIME_WAIT = 3 # seconds
DATABASE_UPTIME_RETRIES = 6 # times

def wait_for_test_db():
    """Pings the localstack db with describe requests
    for {some time} waiting for it to come up...
    """
    print('####################################')
    print('Waiting for database to start.......')
    print('####################################')

    def try_request(retries):
        try:
            db_func(describe(table_name='users'))
        except TableDoesNotExistException:
            print('** ------>')
            print('Beep Boop Beep Boop DYNAMO ready....')
            print('** ------>')
            return
        except Exception:
            if retries < DATABASE_UPTIME_RETRIES:
                time.sleep(DATABASE_UPTIME_WAIT)
                return try_request(retries + 1)
            raise Exception('Integration tests FAILED - could not connect to dynamo in time')

    return try_request(0)


def setup_test_tables():
    print('####################################')
    print('Creating tables for integration test')
    print('####################################')
    db_func(create(
        table_name='users',
        hash_key='username'))

if __name__ == '__main__':
    wait_for_test_db()
    setup_test_tables()
    pytest.main(['test/integration'])
