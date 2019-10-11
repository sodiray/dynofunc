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
    assert res[':owner'] == 'ray'
    assert res[':status'] == 'ON'

def test_build_key_uses_primitive():
    res = ab.build_key('abcd12')
    assert res['id'] == 'abcd12'

def test_build_key_uses_obj():
    res = ab.build_key({ 'myid': 'abcd12' })
    assert res['myid'] == 'abcd12'

def test_build_condition_expression_uses_primitive():
    res = ab.build_condition_expression('abcd13')
    assert res['name'] == 'id'
    assert res['value'] == 'abcd13'

def test_build_condition_expression_uses_obj():
    res = ab.build_condition_expression({
        'myid': 'abcd13'
    })
    assert res['name'] == 'myid'
    assert res['value'] == 'abcd13'
