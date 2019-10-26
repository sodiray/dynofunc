
import dynamof
from dynamof.core.utils import immutable


def test_db_passes_args():

    mock_client = {}
    mock_runner = lambda r, x: r
    mock_operation = immutable(name='mock', description={}, runner=mock_runner)

    db = dynamof.db(mock_client, debug=True)

    db(mock_operation)
