from boto3.dynamodb.types import TypeSerializer

from dynamof.core.utils import guid, merge, update, pipe, find
from dynamof.core.model import AttributeGroup, Attribute, RequestTree
from dynamof.core.dynamo import get_safe_alias
from dynamof.core.Immutable import Immutable


def parse_attr(key, value):

    def make_attr(k, v):
        return Attribute(k, k, v, k, None)

    def replace_reserved_key(attr):
        """Finds reserved dynamo keywords in the attribute
        names and sets an alias the is safe to use instead"""
        return update(attr, alias=get_safe_alias(attr.original))

    def build_key(attr):
        """Builds the key that can be used to reference
        the attribute's value in an expression"""
        return update(attr, key=f':{attr.key}')

    def apply_function_values(attr):
        """Allows us to support passing a special Function as the
        value of the attribute. Here, if the value property is a
        Function we move it to the func property to be used later
        and call it to get the real value"""
        is_function = lambda val: isinstance(val, Immutable) and val.expression is not None and val.value is not None
        if is_function(attr.value):
            fn = attr.value
            return update(attr,
                func=fn,
                value=fn.value())
        return attr

    def build_value_type_tree(attr):
        """Last step in parsing pipeline, reads the value of the
        attribute and uses boto's serializer to convert it to that
        freaky tree with type indicators that dynamo requires"""
        return update(attr,
            value=TypeSerializer().serialize(attr.value))

    @pipe(make_attr)
    @pipe(replace_reserved_key)
    @pipe(build_key)
    @pipe(apply_function_values)
    @pipe(build_value_type_tree)
    def parse(a):
        return a

    return parse(key, value)

def parse_key(key_name):

    if key_name is None:
        return None

    annotation = key_name[-4:]
    key_type = 'N' if annotation == ':int' else 'S'
    key_name = key_name[:-4] if annotation in [':int', ':str'] else key_name

    return {
        'name': key_name,
        'type': key_type
    }


def builder(
    table_name,
    index_name=None,
    key=None,
    attributes=None,
    conditions=None,
    hash_key=None,
    auto_id=None,
    range_key=None,
    gsi=None,
    lsi=None):

    key = key or {}
    attributes = attributes or {}
    condition_attrs = conditions.attributes if conditions is not None else {}

    if auto_id is not None:
        attributes = {
            **attributes,
            auto_id: guid()
        }

    attrs = AttributeGroup(
        keys=[parse_attr(k, v) for k, v in key.items()],
        values=[parse_attr(k, v) for k, v in attributes.items()],
        conditions=[parse_attr(k, v) for k, v in condition_attrs.items()])

    def update_dicts_in_list(list_of_dicts, keys=None, with_fn=None):
        if list_of_dicts is None or keys is None or with_fn is None:
            return list_of_dicts
        return [{
            k: v if k not in keys else with_fn(v) for k, v in obj.items()
        } for obj in list_of_dicts]

    hash_key = parse_key(hash_key)
    range_key = parse_key(range_key)
    gsi = update_dicts_in_list(gsi, keys=['range_key', 'hash_key'], with_fn=parse_key)
    lsi = update_dicts_in_list(lsi, keys=['range_key'], with_fn=parse_key)

    return lambda fn: fn(RequestTree(attrs, table_name, index_name, hash_key, range_key, conditions, gsi, lsi))
