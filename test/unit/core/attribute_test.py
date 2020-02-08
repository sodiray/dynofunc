import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from dynamof.core.utils import immutable
from dynamof.attribute import attr, cand, cor
from dynamof.core.builder import parse_attr

def test_attribute_equals_condition():
    cond = attr('username').equals('sunshie')
    mock_attributes = [
        immutable({
            'original': 'username',
            'key': ':username',
            'value': { "S": "sunshie" },
            'alias': 'username',
            'func': None
        })
    ]

    result = cond.expression(mock_attributes)

    # username = :username
    # { ":username": { "S": "sunshie" } }
    assert result == 'username = :username'

def test_attribute_between_adds_attributes():
    cond = attr('state').between(4, 9)

    assert 'state_a' in cond.attributes
    assert 'state_b' in cond.attributes

def test_attribute_between_condition():
    cond = attr('state').between(4, 9)
    mock_attributes = [
        immutable({
            'original': 'state',
            'key': ':state',
            'value': { "N": 7 },
            'alias': 'state',
            'func': None
        }),
        *[parse_attr(k, v) for k, v in cond.attributes.items()]
    ]

    result = cond.expression(mock_attributes)

    assert result == 'state BETWEEN :state_a AND :state_b'

def test_condition_composition():

    cond = cand(
        attr('username').equals('sunshie'),
        cor(
            cand(
                attr('rank').gt(12),
                attr('rank').lt(20)),
            cand(
                attr('kills').gt_or_eq(100),
                attr('kills').lt_or_eq(1000))))

    mock_attributes = [
        immutable({
            'original': 'rank',
            'key': ':rank',
            'value': { "N": 12 },
            'alias': 'rank',
            'func': None
        }),
        immutable({
            'original': 'kills',
            'key': ':kills',
            'value': { "N": 300 },
            'alias': 'kills',
            'func': None
        }),
        immutable({
            'original': 'username',
            'key': ':username',
            'value': { "S": "sunshie" },
            'alias': 'username',
            'func': None
        })
    ]

    expected = '(username = :username) AND (((rank > :rank) AND (rank < :rank)) OR ((kills >= :kills) AND (kills <= :kills)))'

    result = cond.expression(mock_attributes)

    assert result == expected
