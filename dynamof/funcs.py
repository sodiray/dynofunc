
import collections

Function = collections.namedtuple("Function", [
    "expression",
    "value"
])


def append(*values):
    """Generates a Function that will tell the builder the correct format
    for list appending for a specific item. The full update expression would
    look like...
        UpdateExpression="SET some_attr = list_append(some_attr, :i)"
    """
    def expression(attr):
        return f'{attr.alias} = list_append({attr.alias}, {attr.key})'

    def value():
        return list(values)

    return Function(expression, value)

def prepend(*values):
    """Same as append - in reverse"""
    def expression(attr):
        return f'{attr.alias} = list_append({attr.key}, {attr.alias})'

    def value():
        return list(values)

    return Function(expression, value)
