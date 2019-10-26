import decimal

import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from test.utils.assertions import assertObjectsEqual

from dynamof.utils import new_id, update, strip_Decimals

def test_new_id_generates_guid():
    res = new_id()
    assert res is not None
    assert isinstance(res, str)
    assert len(res) == 36

def test_update_returns_new_instance():

    original = {
        'alpha': 1,
        'beta': 2,
        'dalet': 4
    }

    result = update(original)

    assert original == result
    assert original is not result

def test_update_returns_with_updates():

    original = {
        'alpha': 1,
        'beta': 2,
        'dalet': 4
    }

    result = update(original, alpha=10)

    assert original is not result
    assert result.get('alpha') == 10

def test_update_handles_deep_objects():

    original = {
        'alpha': {
            'color': 23
        },
        'beta': 2,
        'dalet': 4
    }

    result = update(original, alpha={
        'color': 10
    })

    assert original is not result
    assert result.get('alpha').get('color') == 10

def test_deep_strip_Decimals():

    result = strip_Decimals({
        'a': decimal.Decimal(30),
        'b': None,
        'c': [ decimal.Decimal(30), 'x' ],
        'd': { 'r': decimal.Decimal(30.30) }
    })

    expected = {
        'a': 30,
        'b': None,
        'c': [ 30, 'x' ],
        'd': { 'r': 30.30 }
    }

    assertObjectsEqual(result, expected)
