

def assertIsOperation(obj):
    assert obj is not None
    assert 'description' in obj
    assert 'provider' in obj
    assert 'runner' in obj
