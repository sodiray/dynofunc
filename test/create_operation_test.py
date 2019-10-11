import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from idynamo.operations import create

def test_create_is_operation():
    res = create(name='users', hash_key={
        'username': 'string'
    })
    assert res['description'] is not None
    assert res['provider'] is not None
