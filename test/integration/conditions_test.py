import json
import pytest
import uuid
import random

from test.integration.fixtures import db

from dynamof import attr, cand
from dynamof import (
    create,
    add,
    query
)

def _analytic_item(state):
    return { 'id': 1, 'state': state }

def _owner_item(name):
    return { 'id': 1, 'owner': name }

def test_conditions(db):

    ##
    ##  POPULATE TEST DATA
    ##

    db(create(
        table_name='ownership',
        hash_key='id:int',
        range_key='owner'))

    db(add(table_name='ownership', item=_owner_item('ray-x28h')))
    db(add(table_name='ownership', item=_owner_item('ray-934x')))
    db(add(table_name='ownership', item=_owner_item('carl-28hx')))
    db(add(table_name='ownership', item=_owner_item('kobe-oi28')))

    db(create(
        table_name='analytics',
        hash_key='id:int',
        range_key='state:int'))

    db(add(table_name='analytics', item=_analytic_item(1)))
    db(add(table_name='analytics', item=_analytic_item(2)))
    db(add(table_name='analytics', item=_analytic_item(3)))
    db(add(table_name='analytics', item=_analytic_item(4)))
    db(add(table_name='analytics', item=_analytic_item(5)))
    db(add(table_name='analytics', item=_analytic_item(6)))
    db(add(table_name='analytics', item=_analytic_item(7)))
    db(add(table_name='analytics', item=_analytic_item(8)))
    db(add(table_name='analytics', item=_analytic_item(9)))
    db(add(table_name='analytics', item=_analytic_item(10)))

    ##
    ##  RUN TESTS
    ##

    ## TEST == EQUALS
    result = db(query(
        table_name='analytics',
        conditions=attr('id').equals(1)))
    assert len(result.items()) == 10

    ## TEST > GREATER THAN
    result = db(query(
        table_name='analytics',
        conditions=cand(
            attr('id').equals(1),
            attr('state').gt(7))))
    assert len(result.items()) == 3

    ## TEST < LESS THAN
    result = db(query(
        table_name='analytics',
        conditions=cand(
            attr('id').equals(1),
            attr('state').lt(7))))
    assert len(result.items()) == 6

    ## TEST >= GREATER THEAN OR EQUAL TO
    result = db(query(
        table_name='analytics',
        conditions=cand(
            attr('id').equals(1),
            attr('state').gt_or_eq(7))))
    assert len(result.items()) == 4

    ## TEST <= LESS THEAN OR EQUAL TO
    result = db(query(
        table_name='analytics',
        conditions=cand(
            attr('id').equals(1),
            attr('state').lt_or_eq(7))))
    assert len(result.items()) == 7

    ## TEST BETWEEN b AND c
    result = db(query(
        table_name='analytics',
        conditions=cand(
            attr('id').equals(1),
            attr('state').between(6, 8))))
    assert len(result.items()) == 3

    ## TEST begins_with
    result = db(query(
        table_name='ownership',
        conditions=cand(
            attr('id').equals(1),
            attr('owner').begins_with('ray-'))))
    assert len(result.items()) == 2
