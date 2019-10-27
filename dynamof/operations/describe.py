
from dynamof.core import builder as ab
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def describe(table_name):
    build = ab.builder(
        table_name=table_name)
    description = shake(
        TableName=build(ab.TableName))
    return Operation(description, run)

def run(client, description):
    res = client.describe_table(**description)
    return response(res)
