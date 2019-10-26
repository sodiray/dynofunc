import collections

from dynamof.utils import merge, find

Attribute = collections.namedtuple("Attribute", [
    "equals",
    "gt",
    "lt",
    "lt_or_eq",
    "gt_or_eq"
])

Condition = collections.namedtuple("Condition", [
    "expression",
    "attributes"
])

# condition and
def cand(*conditions):
    def build(attrs):
        return ' AND '.join([f'({cond.expression(attrs)})' for cond in conditions])
    attributes = merge([cond.attributes for cond in conditions])
    return Condition(build, attributes)

# condition or
def cor(*conditions):
    def build(attrs):
        return ' OR '.join([f'({cond.expression(attrs)})' for cond in conditions])
    attributes = merge([cond.attributes for cond in conditions])
    return Condition(build, attributes)


def attr(name):

    def find_attr(attrs):
        return find(attrs, lambda a: a.get('original') == name)

    def equals(value):
        def build(attrs):
            attr = find_attr(attrs)
            alias = attr.get('alias')
            key = attr.get('key')
            return f'{alias} = {key}'
        return Condition(build, { name: value })

    def greater_than(value):
        def build(attrs):
            attr = find_attr(attrs)
            alias = attr.get('alias')
            key = attr.get('key')
            return f'{alias} > {key}'
        return Condition(build, { name: value })

    def less_than(value):
        def build(attrs):
            attr = find_attr(attrs)
            alias = attr.get('alias')
            key = attr.get('key')
            return f'{alias} < {key}'
        return Condition(build, { name: value })

    def less_than_or_equal(value):
        def build(attrs):
            attr = find_attr(attrs)
            alias = attr.get('alias')
            key = attr.get('key')
            return f'{alias} <= {key}'
        return Condition(build, { name: value })

    def greater_than_or_equal(value):
        def build(attrs):
            attr = find_attr(attrs)
            alias = attr.get('alias')
            key = attr.get('key')
            return f'{alias} >= {key}'
        return Condition(build, { name: value })

    return Attribute(equals, greater_than, less_than, less_than_or_equal, greater_than_or_equal)
