import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from dynamof import exceptions

def test_base_exception_adds_info():
    res = exceptions.DynamofException('my message').info('zzz')
    assert 'zzz' in res.message

# def test_exceptions():
#     exceptions.PreexistingTableException()
#     exceptions.DatabaseFindException()
#     exceptions.UnknownException()
