import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from dynamof.utils import new_id

def test_new_id_generates_guid():
    res = new_id()
    assert res is not None
    assert isinstance(res, str)
    assert len(res) == 36
