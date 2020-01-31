
from dynamof.core import builder as ab
from dynamof.core import args
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def scan(table_name: str):
    """Creates an Operation that will scan through every item in a table when run.

    Args:
        table_name (str): The name of the table to scan

    """
    build = ab.builder(
        table_name=table_name)
    description = shake(
        TableName=build(args.TableName))
    return Operation(description, run)

def run(client, description):
    res = client.scan(**description)
    return response(res)
