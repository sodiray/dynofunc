import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from test.utils.mocks import mock_unknown_exc

from dynamof.core.executor import execute
from dynamof.core.model import Operation
from dynamof.core.exceptions import DynamofException

def test_execute_calls_runner():
    mock_client = 'MOCK_CLIENT'
    mock_description = {}
    mock_runner = MagicMock()

    mock_operation = Operation(mock_description, mock_runner)

    res = execute(mock_client, mock_operation)

    assert mock_runner.called is True

def test_execute_converts_exc_to_custom_exc():
    mock_runner = MagicMock(side_effect=mock_unknown_exc)

    mock_operation = Operation({}, mock_runner)

    try:
        execute(None, mock_operation)
    except DynamofException as exc:
        pass
    else:
        pytest.fail('Execute did not raise expected exception')
