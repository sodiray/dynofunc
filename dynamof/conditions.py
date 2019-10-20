import collections

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
    exp = ' AND '.join([cond.expression for cond in conditions])
    values = collections.ChainMap(*[cond.attributes for cond in conditions])
    return Condition(exp, values)

# condition or
def cor(*conditions):
    exp = ' OR '.join([cond.expression for cond in conditions])
    values = collections.ChainMap(*[cond.attributes for cond in conditions])
    return Condition(exp, values)


def attr(name):

    def equals(value):
        exp = f'{name} = :{name}'
        return Condition(exp, { name: value })

    def greater_than(value):
        exp = f'{name} > :{name}'
        return Condition(exp, { name: value })

    def less_than(value):
        exp = f'{name} < :{name}'
        return Condition(exp, { name: value })

    def less_than_or_equal(value):
        exp = f'{name} <= :{name}'
        return Condition(exp, { name: value })

    def greater_than_or_equal(value):
        exp = f'{name} >= :{name}'
        return Condition(exp, { name: value })

    return Attribute(equals, greater_than, less_than, less_than_or_equal, greater_than_or_equal)
