
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
        name = attr.get('alias')
        key = attr.get('key')
        return f'{name} = list_append({name}, {key})'

    def value():
        return list(values)

    return Function(expression, value)
