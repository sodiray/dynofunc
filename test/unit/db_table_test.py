
import dynofunc
from dynofunc.core.utils import immutable


def test_db_passes_args():

    mock_client = {}
    mock_runner = lambda r, x: r
    mock_operation = immutable(name='mock', description={}, runner=mock_runner)

    db = dynofunc.db(mock_client)

    db(mock_operation)

def test_table_contains_operations():

    mock_db = lambda x: None
    mock_table_name = ''
    sut = dynofunc.table(mock_db, mock_table_name)

    assert sut.add is not None
    assert sut.delete is not None
    assert sut.query is not None

    sut.add(item={})
