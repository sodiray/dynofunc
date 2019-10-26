import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from dynamof.conditions import (
    attr,
    cand,
    cor
)

def test_attribute_equals_condition():
    cond = attr('username').equals('sunshie')
    mock_attributes = [
        {
            'original': 'username',
            'key': ':username',
            'value': { "S": "sunshie" },
            'alias': 'username',
            'func': None
        }
    ]


    result = cond.expression(mock_attributes)

    # username = :username
    # { ":username": { "S": "sunshie" } }
    assert result == 'username = :username'

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
        {
            'original': 'rank',
            'key': ':rank',
            'value': { "N": 12 },
            'alias': 'rank',
            'func': None
        },
        {
            'original': 'kills',
            'key': ':kills',
            'value': { "N": 300 },
            'alias': 'kills',
            'func': None
        },
        {
            'original': 'username',
            'key': ':username',
            'value': { "S": "sunshie" },
            'alias': 'username',
            'func': None
        }
    ]

    expected = '(username = :username) AND (((rank > :rank) AND (rank < :rank)) OR ((kills >= :kills) AND (kills <= :kills)))'

    result = cond.expression(mock_attributes)

    print('#### result')
    print(result)

    assert result == expected
