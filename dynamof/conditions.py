import collections
from dynamof import builder as ab

Attribute = collections.namedtuple("Attribute", [
    "equals",
    "gt",
    "lt"
    # "lt_or_eq",
    # "gt_or_eq"
])

Condition = collections.namedtuple("Condition", [
    "expression",
    "attr_values"
])

# condition and
def cand(*conditions):
    exp = ' AND '.join([cond.expression for cond in conditions])
    values = collections.ChainMap(*[cond.attr_values for cond in conditions])
    return Condition(exp, values)

# condition or
def cor(*conditions):
    exp = ' OR '.join([cond.expression for cond in conditions])
    values = collections.ChainMap(*[cond.attr_values for cond in conditions])
    return Condition(exp, values)


def attr(name):

    def equals(value):
        exp = f'{name} = :{name}'
        values = ab.value_type_tree({ f':{name}': value })
        return Condition(exp, values)

    def greater_than(value):
        exp = f'{name} > :{name}'
        values = ab.value_type_tree({ f':{name}': value })
        return Condition(exp, values)

    def less_than(value):
        exp = f'{name} < :{name}'
        values = ab.value_type_tree({ f':{name}': value })
        return Condition(exp, values)

    return Attribute(equals, greater_than, less_than)
