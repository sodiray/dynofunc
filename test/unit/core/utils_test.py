import json
import decimal

import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from test.utils.assertions import assertObjectsEqual

from dynamof.core.utils import guid, update, strip_Decimals, immutable


def test_guid_generates_guid():
    res = guid()
    assert res is not None
    assert isinstance(res, str)
    assert len(res) == 36

def test_update_returns_new_instance():

    original = immutable({
        'alpha': 1,
        'beta': 2,
        'dalet': 4
    })

    result = update(original)

    assert original == result
    assert original is not result

def test_update_returns_with_updates():

    original = immutable({
        'alpha': 1,
        'beta': 2,
        'dalet': 4
    })

    result = update(original, alpha=10)

    assert original is not result
    assert result.get('alpha') == 10

def test_update_handles_deep_objects():

    original = immutable({
        'alpha': {
            'color': 23
        },
        'beta': 2,
        'dalet': 4
    })

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

def test_immutable_raises_when_set():
    obj = immutable(x=2, y=23)

    with pytest.raises(TypeError):
        obj['x'] = 5

    with pytest.raises(TypeError):
        obj.x = 5

    with pytest.raises(TypeError):
        del obj['x']

    with pytest.raises(TypeError):
        del obj.x

def test_immutable_none_comparison():
    obj = immutable(x=2, y=23)
    isEqual = obj == None
    assert isEqual is not True

def test_immutable_repr_dumps_json():
    obj = immutable(x=2, y=23)
    r = repr(obj)
    json.loads(r)

def test_immutable_str_dumps_json():
    obj = immutable(x=2, y=23)
    s = str(obj)
    json.loads(s)
