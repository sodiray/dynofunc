import pytest
import json
from unittest.mock import patch
from unittest.mock import MagicMock

from test.utils.assertions import assertObjectsEqual

from dynamof.core import builder as ab
from dynamof.attribute import attr


def test_builder_creates_data():
    build = ab.builder(
        'query',
        table_name='products',
        key={ 'id': 13 },
        attributes={
            'items': [ 'glow', 'dust' ]
        },
        conditions=attr('price').gt(10))

    result = build(lambda r: r)

    expected_item = {
      "original": "items",
      "key": ":items",
      "value": {
        ":items": {
          "L": [
            { "S": "glow" },
            { "S": "dust" }
          ]
        }
      },
      "alias": "#items"
    }

    item = result.get('attributes').get('values')[0]

    assert item.get('original') == expected_item.get('original')
    assert item.get('key') == expected_item.get('key')
    assert item.get('alias') == expected_item.get('alias')
