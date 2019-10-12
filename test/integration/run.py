#!/usr/bin/env python

import pytest

from test.integration.fixtures import db_func

from dynamof.operations import create


def setup_test_tables():

    print('####################################')
    print('Creating tables for integration test')
    print('####################################')
    db_func(create(
        table_name='users',
        hash_key='username',
        allow_existing=True))

if __name__ == '__main__':

    setup_test_tables()
    pytest.main(['test/integration'])
