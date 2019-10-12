

def assertIsOperation(op):
    assert op is not None
    assert hasattr(op, 'description')
    assert hasattr(op, 'runner')
