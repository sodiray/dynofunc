

def assertIsOperation(op):
    assert op is not None
    assert hasattr(op, 'description')
    assert hasattr(op, 'runner')

def assertObjectsEqual(obj_a, obj_b):

    def _assert(a, b):
        if a == b:
            return
        raise AssertionError(f'{a} !== {b} inside assertObjectsEqual')

    def _check(a, b):
        if a is None or b is None:
            _assert(a, b)
        for k,v in a.items():
            if isinstance(v, dict):
                assertObjectsEqual(v, b[k])
            else:
                _assert(v, b[k])

    # Asserting both directions is more work
    # but it ensures no dangling values on
    # on either object
    _check(obj_a, obj_b)
    _check(obj_b, obj_a)
