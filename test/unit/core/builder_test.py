import pytest
import json
from unittest.mock import patch
from unittest.mock import MagicMock

from test.utils.assertions import assertObjectsEqual

from dynamof.core import builder as ab
from dynamof.attribute import attr


def test_parse_key():

    result = ab.parse_key('uuid:int')

    assert result == {
        'name': 'uuid',
        'type': 'N'
    }


def test_builder_creates_data():
    build = ab.builder(
        table_name='products',
        key={ 'id': 13 },
        attributes={
            'items': [ 'glow', 'dust' ]
        },
        gsi=[{
            'name': 'global_index',
            'hash_key': 'state:int'
        }],
        conditions=attr('price').gt(10))

    result = build(lambda r: r)

    expected_item = {
        "alias": "#items",
        "func": None,
        "key": ":items",
        "original": "items",
        "value": {
            "L": [
                {
                    "S": "glow"
                },
                {
                    "S": "dust"
                }
            ]
        }
    }

    assert result.get('attributes').get('values')[0] == expected_item

    expected_gsi = {
        "hash_key": {
            "name": "state",
            "type": "N"
        },
        "name": "global_index"
    }

    assert result.get('gsi')[0] == expected_gsi
