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
    # username = :username
    # { ":username": { "S": "sunshie" } }
    assert cond.expression == 'username = :username'
    assert cond.attr_values[':username']['S'] == 'sunshie'

def test_attribute_greater_than_condition():
    cond = attr('rank').gt(12)
    # rank > :rank
    # { ":rank": { "N": 12 } }
    assert cond.expression == 'rank > :rank'
    assert cond.attr_values[':rank']['N'] == 12

def test_attribute_less_than_condition():
    cond = attr('rank').lt(12)
    # rank < :rank
    # { ":rank": { "N": 12 } }
    assert cond.expression == 'rank < :rank'
    assert cond.attr_values[':rank']['N'] == 12

def test_and_condition():
    cond_a = attr('username').equals('sunshie')
    cond_b = attr('rank').lt(12)

    res = cand(cond_a, cond_b)

    answer = 'username = :username AND rank < :rank'
    assert res.expression == answer
    assert res.attr_values[':username']['S'] == 'sunshie'
    assert res.attr_values[':rank']['N'] == 12

def test_or_condition():
    cond_a = attr('username').equals('sunshie')
    cond_b = attr('rank').lt(12)

    res = cor(cond_a, cond_b)

    answer = 'username = :username OR rank < :rank'
    assert res.expression == answer
    assert res.attr_values[':username']['S'] == 'sunshie'
    assert res.attr_values[':rank']['N'] == 12
