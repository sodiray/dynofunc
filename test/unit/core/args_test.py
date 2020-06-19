import pytest
import json
from unittest.mock import patch
from unittest.mock import MagicMock

from test.utils.assertions import assertObjectsEqual

from dynofunc.core import args
from dynofunc.core.utils import immutable

def test_GlobalSecondaryIndexes_result():
    mock_request = immutable(
        gsi=[dict(
            name='gs_index',
            hash_key={
                'name': 'other',
                'type': 'S'
            },
            range_key={
                'name': 'type',
                'type': 'S'
            },
        )])

    expected = [{
        'IndexName': 'gs_index',
        'KeySchema': [
            {
                'AttributeName': 'other',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'type',
                'KeyType': 'RANGE'
            }
        ],
        'Projection': {
            'ProjectionType': 'ALL'
        },
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    }]

    result = args.GlobalSecondaryIndexes(mock_request)

    assertObjectsEqual(result, expected)

def test_LocalSecondaryIndexes_result():
    mock_request = immutable(
        hash_key={
            'name': 'main_hash_key',
            'type': 'S'
        },
        lsi=[dict(
            name='gs_index',
            range_key={
                'name': 'type',
                'type': 'S'
            },
        )])

    expected = [{
        'IndexName': 'gs_index',
        'KeySchema': [
            {
                'AttributeName': 'main_hash_key',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'type',
                'KeyType': 'RANGE'
            }
        ],
        'Projection': {
            'ProjectionType': 'ALL'
        }
    }]

    result = args.LocalSecondaryIndexes(mock_request)

    assertObjectsEqual(result, expected)

def test_AttributeDefinitions_gets_all_keys():
    mock_request = immutable(
        hash_key={
            'name': 'id',
            'type': 'S'
        },
        range_key={
            'name': 'country',
            'type': 'S'
        },
        lsi=[dict(
            name='gs_index',
            range_key={
                'name': 'type',
                'type': 'S'
            },
        )],
        gsi=[dict(
            name='gs_index',
            hash_key={
                'name': 'username',
                'type': 'S'
            },
            range_key={
                'name': 'status',
                'type': 'S'
            }
        )])

    expected = [ 'id', 'type', 'username', 'status', 'country' ]

    result = [item.get('AttributeName') for item in args.AttributeDefinitions(mock_request)]

    assert set(expected) == set(result)

def test_AttributeDefinitions_does_not_duplicate_keys():
    mock_request = immutable(
        hash_key={
            'name': 'id',
            'type': 'S'
        },
        range_key={
            'name': 'contry',
            'type': 'S'
        },
        lsi=[dict(
            name='gs_index',
            range_key={
                'name': 'type',
                'type': 'S'
            }
        )],
        gsi=[dict(
            name='gs_index',
            hash_key={
                'name': 'country',
                'type': 'S'
            },
            range_key={
                'name': 'status',
                'type': 'S'
            }
        )])

    result = [item.get('AttributeName') for item in args.AttributeDefinitions(mock_request)]

    assert len([1 for key in result if key == 'country']) == 1

def test_KeySchema_uses_hash_and_range():
    mock_request = immutable(
        hash_key={
            'name': 'id',
            'type': 'S'
        },
        range_key={
            'name': 'type',
            'type': 'S'
        })

    expected = [
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'type',
            'KeyType': 'RANGE'
        }
    ]

    result = args.KeySchema(mock_request)

    assertObjectsEqual(result, expected)

def test_ExpressionAttributeNames_appends_references():

    mock_request = immutable(
        attributes=immutable({
            'keys': [],
            'values': [],
            'conditions': []
        }),
        conditions=immutable({
            'references': [ 'state' ]
        }))

    result = args.ExpressionAttributeNames(mock_request)

    assert result == { '#state': 'state' }
