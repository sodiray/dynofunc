import uuid
import decimal
from collections import ChainMap

import pydash as _


def new_id():
    return str(uuid.uuid4())

def shake(obj):
    """Removes none and empty object values"""
    return { k: v for k, v in obj.items() if bool(v) and v is not None }

def merge(list_of_dicts):
    return dict(ChainMap(*list_of_dicts))

def update(obj, **kwargs):
    """Returns a new instance of the given object with
    all key/val in kwargs set on it
    """
    return {
        **_.clone_deep(obj),
        **kwargs
    }

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

# class obj:
#     def __init__(self, attrs=None):
#         self.__dict__ = attrs if attrs is not None else {}
#     def pprint(self):
#         return json.dumps(self,
#             default=lambda o: o.__dict__,
#             sort_keys=True,
#             indent=4)
#     def __repr__(self):
#         return self.pprint()
#     def __str__(self):
#         return self.pprint()
