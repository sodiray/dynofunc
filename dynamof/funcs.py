
import collections

Function = collections.namedtuple("Function", [
    "make_expression",
    "make_value"
])


def append(*values):
    """Generates a Function that will tell the builder the correct format
    for list appending for a specific item. The full update expression would
    look like...
        UpdateExpression="SET some_attr = list_append(some_attr, :i)"
    """
    def make_expression(name, key):
        return f'{name} = list_append({name}, {key})'

    def make_value():
        return list(values)

    return Function(make_expression, make_value)
