import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from dynamof import arg_builder as ab

def test_build_update_expression():
    res = ab.build_update_expression({
        'owner': 'ray',
        'status': 'ON'
    })
    assert res == 'SET owner = :owner, status = :status'

def test_build_expression_attribute_values():
    res = ab.build_expression_attribute_values({
        'owner': 'ray',
        'status': 'ON'
    })
    assert res[':owner']['S'] == 'ray'
    assert res[':status']['S'] == 'ON'

def test_build_key_uses_primitive():
    res = ab.build_key('abcd12')
    assert res['id'] == 'abcd12'

def test_build_key_uses_obj():
    res = ab.build_key({ 'myid': 'abcd12' })
    assert res['myid'] == 'abcd12'

def test_build_condition_expression_uses_primitive():
    res = ab.build_condition_expression('abcd13')
    assert res == 'id = :id'

def test_build_condition_expression_uses_obj():
    res = ab.build_condition_expression({
        'myid': 'abcd13'
    })
    assert res == 'myid = :myid'

def test_build_value_type_tree():
    res = ab.build_value_type_tree({
        'username': 'rayepps',
        'user_id': 23,
        'roles': set([ 'admin', 'user' ]),
        'timming': [ 23, 56, 22, 11 ],
        'position': None,
        'extra': {
            'food': [ 'american', 43 ]
        }
    })

    # Assert string type is built
    assert res['username'] is not None
    assert res['username']['S'] == 'rayepps'

    # Assert number type is built
    assert res['user_id'] is not None
    assert res['user_id']['N'] == 23

    # Assert string set type is built
    assert res['roles'] is not None
    assert 'user' in res['roles']['SS']
    assert 'admin' in res['roles']['SS']

    # Assert list type is built
    assert res['timming'] is not None
    assert res['timming']['L'] is not None
    assert res['timming']['L'][0]['N'] == 23
    assert res['timming']['L'][1]['N'] == 56
    assert res['timming']['L'][2]['N'] == 22

    # Assert null type is built
    assert res['position'] is not None
    assert res['position']['NULL'] is True

    # Assert dict type is built
    assert res['extra'] is not None
    assert res['extra']['M'] is not None
    assert res['extra']['M']['food']['L'][0]['S'] == 'american'
    assert res['extra']['M']['food']['L'][1]['N'] == 43
