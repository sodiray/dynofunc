
from dynamof.core.utils import immutable


def Attr(equals, gt, lt, lt_or_eq, gt_or_eq, between, begins_with):
    return immutable({
        'equals': equals,
        'gt': gt,
        'lt': lt,
        'lt_or_eq': lt_or_eq,
        'gt_or_eq': gt_or_eq,
        'between': between,
        'begins_with': begins_with
    })

def Operation(description, runner):
    return immutable({
        'description': description,
        'runner': runner
    })

def Condition(expression, attributes, references=None):
    references = references or []
    return immutable({
        'expression': expression,
        'attributes': attributes,
        'references': references
    })

def Function(expression, value):
    return immutable({
        'expression': expression,
        'value': value
    })

def RequestTree(attributes, table_name, index_name, hash_key, range_key, conditions, gsi, lsi):
    return immutable({
        'attributes': attributes,
        'table_name': table_name,
        'index_name': index_name,
        'hash_key': hash_key,
        'range_key': range_key,
        'conditions': conditions,
        'gsi': gsi,
        'lsi': lsi
    })

def AttributeGroup(keys, values, conditions):
    return immutable({
        'keys': keys,
        'values': values,
        'conditions': conditions
    })

def Attribute(original, key, value, alias, func):
    """
    Parameters
    ----------
    original : str
        The orignial name the client passed us for the attribute.
        Should never change for later references

        Ex. { 'item': 'a' } => 'item'


    key : str
        The key we should use in expressions to refer to the value
        of this attribute

        Ex. { 'item': 'a' } => ':item'

    value : dict
        The typed value of the attribute. NOTE: The attribute name should
        be stripped out so only the object defining the value/type is stored
        here. Different operations will use this and some will need to set a
        custom key so here were only storing the value of the value/type tree

        Ex. { 'item': 'a' } => { 'S': 'a' }

    alias : str
        The name we should use when refering to the dynamodb _column_. Typically
        this will be the same as `original`. However, in the case of reserved attr
        names it will be updated to something dynamodb friendly

        Ex. { 'item': 'a' } => '#item'

    func : Function
        A func from `dynamof.funcs` that should be called to modify the attr
    """
    return immutable({
        'original': original,
        'key': key,
        'value': value,
        'alias': alias,
        'func': func
    })
