#!/usr/bin/env python

from boto3 import resource, client
from idynamo.executor import execute
from idynamo.operations import (
    create
)

url = 'http://localstack:4569'


def setup_test_tables():
    op = create(name='users', hash_key='id')
    res = execute(op, url)


def run_tests():
    pass

if __name__ == '__main__':
    setup_test_tables()
    run_tests()
