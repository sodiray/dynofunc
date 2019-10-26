import uuid
import json
import decimal
from collections import ChainMap


def guid():
    return str(uuid.uuid4())

def shake(obj):
    """Removes none and empty object values"""
    return { k: v for k, v in obj.items() if bool(v) and v is not None }

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

class Immutable:

    def __init__(self, **kwargs):
        """Sets all values once given
        whatever is passed in kwargs
        """
        for k,v in kwargs.items():
            object.__setattr__(self, k, v)

    def __setattr__(self, *args):
        """Disables setting attributes via
        item.prop = val or item['prop'] = val
        """
        raise TypeError('Immutable objects cannot have properties set')

    def __delattr__(self, *args):
        """Disables deleting properties"""
        raise TypeError('Immutable objects cannot have properties deleted')

    def __getitem__(self, item):
        """Allows for dict like access of properties
        val = item['prop']
        """
        return self.__dict__[item]

    def keys(self):
        """Paired with __getitem__ supports **unpacking
        new = { **item, **other }
        """
        return self.__dict__.keys()

    def get(self, *args, **kwargs):
        """Allows for dict like property access
        item.get('prop')
        """
        return self.__dict__.get(*args, **kwargs)

    def pprint(self):
        """Helper method used for printing that
        formats in a dict like way
        """
        return json.dumps(self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

    def __repr__(self):
        """Print to repl in a dict like fashion"""
        return self.pprint()

    def __str__(self):
        """Convert to a str in a dict like fashion"""
        return self.pprint()

    def dict(self):
        """Helper method for getting the raw dict value
        of the immutable object"""
        return self.__dict__

    def __eq__(self, other):
        """Supports equality operator
        immutable({'a': 2}) == immutable({'a': 2})"""
        if other is None:
            return False
        return self.dict() == other.dict()

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
