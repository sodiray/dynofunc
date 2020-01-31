
from dynamof.core import builder as ab
from dynamof.core import args
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def add(table_name: str, item: dict, auto_id: bool = None):
    """Creates an Operation that will add an item to a table when run.

    Args:
        table_name (str): The name of the table to add the item to.
        item (dict): The item to add to the table.

    """
    build = ab.builder(
        table_name=table_name,
        attributes=item,
        auto_id=auto_id)
    description = shake(
        TableName=build(args.TableName),
        Item=build(args.Item),
        ReturnValues='ALL_OLD')
    return Operation(description, run)

def run(client, description):
    res = client.put_item(**description)
    return response(res)
