#!/usr/bin/env python

from boto3 import resource, client
import idynamo



create = idynamo.operations.create(name='users', hash_key={
    'id': 'string'
})



res = idynamo.execute(create, url)




def setup_test_tables():
    idynamo.

def run_tests():
    dynamo.table('users')
        .add({
            'name': 'repps',
            'status': 'active'
        })


if __name__ == '__main__':
    setup_test_tables()
    run_tests()
