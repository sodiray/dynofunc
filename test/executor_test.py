import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from dynamof.executor import execute
from dynamof.operations import Operation

def test_execute_calls_runner():
    mock_client = 'MOCK_CLIENT'
    mock_description = {}
    mock_runner = MagicMock()

    mock_operation = Operation(mock_description, mock_runner)

    res = execute(mock_client, mock_operation)

    assert mock_runner.called is True
