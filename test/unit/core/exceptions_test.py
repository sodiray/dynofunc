import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from test.utils.mocks import (
    mock_table_does_not_exist_exc,
    mock_condition_not_met_exc,
    mock_preexisting_table_exc,
    mock_bad_gateway_exc,
    mock_unknown_exc
)

from dynamof.core.exceptions import (
    parse,
    factory,
    DynamofException,
    PreexistingTableException,
    TableDoesNotExistException,
    ConditionNotMetException,
    BadGatewayException,
    UnknownDatabaseException
)


def test_base_exception_adds_info():
    res = DynamofException('').info('zzz')
    assert 'zzz' in res.message

def test_parses_handles_whatever_we_pass():

    mock_err = MagicMock()
    mock_err.response = {
        'Error': {
            'Code': 'THIS_DOPE_CODE'
        }
    }

    message, code = parse({})
    message, code = parse(None)
    message, code = parse(mock_err)

    assert code == 'THIS_DOPE_CODE'

def test_factory():

    exc = factory(mock_bad_gateway_exc)
    assert isinstance(exc, BadGatewayException)

    exc = factory(mock_table_does_not_exist_exc)
    assert isinstance(exc, TableDoesNotExistException)

    exc = factory(mock_condition_not_met_exc)
    assert isinstance(exc, ConditionNotMetException)

    exc = factory(mock_preexisting_table_exc)
    assert isinstance(exc, PreexistingTableException)

    exc = factory(None)
    assert isinstance(exc, UnknownDatabaseException)

def test_unknown_exc_logs_message_and_code():
    mock_err = MagicMock()
    mock_err.response = {
        'Error': {
            'Code': 'XX_CODE_XX',
            'Message': 'XX_MESSAGE_XX'
        }
    }

    exc = factory(mock_err)

    assert 'XX_CODE_XX' in exc.message
    assert 'XX_MESSAGE_XX' in exc.message
