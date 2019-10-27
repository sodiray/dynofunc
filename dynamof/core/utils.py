import uuid
import json
import decimal
import functools
from collections import ChainMap

from dynamof.core.Immutable import Immutable


def guid():
    return str(uuid.uuid4())

def shake(**kwargs):
    """Removes none and empty object values"""
    return { k: v for k, v in kwargs.items() if bool(v) and v is not None }

def merge(list_of_dicts):
    return dict(ChainMap(*list_of_dicts))

def strip_Decimals(obj):

    if isinstance(obj, list):
        return [strip_Decimals(item) for item in obj]
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = strip_Decimals(v)
        return obj
    if isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        return float(obj)
    return obj

def find(a_list, fn, default=None):
    return next((item for item in a_list if fn(item)), default)

def update(obj, **kwargs):
    """Returns a new instance of the given object with
    all key/val in kwargs set on it
    """
    return immutable({
        **obj,
        **kwargs
    })

def immutable(obj=None, **kwargs):
    if obj is not None:
        return Immutable(**obj)
    return Immutable(**kwargs)

def pipe(transform):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(transform(*args, **kwargs))
        return wrapper
    return decorator
