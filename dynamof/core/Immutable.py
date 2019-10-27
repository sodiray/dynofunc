import json

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
