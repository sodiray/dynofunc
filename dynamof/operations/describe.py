
from dynamof.core import builder as ab
from dynamof.core import args
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def describe(table_name: str):
    """Creates an Operation that will describe a table when run.

    Args:
        table_name (str): The name of the table to describe

    """
    build = ab.builder(
        table_name=table_name)
    description = shake(
        TableName=build(args.TableName))
    return Operation(description, run)

def run(client, description):
    res = client.describe_table(**description)
    return response(res)
