
from dynamof.core import builder as ab
from dynamof.core import args
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def find(table_name: str, key: dict):
    """Creates an Operation that will find an item in a table when run.

    Args:
        table_name (str): The name of the table to find the item in
        key (dict): An object with a key, value that will be used as the identifier for the item
            Examples:
                - { 'username': 'sunshie' }
                - { 'id': '9snw82h', 'type': 'car' } -> when table uses hash key and range key

    """
    build = ab.builder(
        table_name=table_name,
        key=key)
    description = shake(
        TableName=build(args.TableName),
        Key=build(args.Key))
    return Operation(description, run)

def run(client, description):
    res = client.get_item(**description)
    return response(res)
