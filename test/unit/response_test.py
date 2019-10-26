
from dynamof import response


def test_destructure_handles_none():

    assert response.destructure_type_tree(None) == None
