import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from dynamof import exceptions

def test_base_exception_adds_info():
    res = exceptions.DynamofException('my message').info('zzz')
    assert 'zzz' in res.message

def test_ConditionNotMetException_check():

    mock_err = MagicMock()
    mock_err.response = {
        'Error': {
            'Code': 'ConditionalCheckFailedException'
        }
    }

    assert True == exceptions.ConditionNotMetException.matches(mock_err)
    assert False == exceptions.ConditionNotMetException.matches({})
    assert False == exceptions.ConditionNotMetException.matches(None)

# def test_exceptions():
#     exceptions.PreexistingTableException()
#     exceptions.DatabaseFindException()
#     exceptions.UnknownException()
