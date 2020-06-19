
from dynofunc.core import builder as ab
from dynofunc.core import args
from dynofunc.core.utils import shake
from dynofunc.core.model import Operation
from dynofunc.core.response import response


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
