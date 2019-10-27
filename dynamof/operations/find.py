
from dynamof.core import builder as ab
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def find(table_name, key):
    build = ab.builder(
        table_name=table_name,
        key=key)
    description = shake(
        TableName=build(ab.TableName),
        Key=build(ab.Key))
    return Operation(description, run)

def run(client, description):
    res = client.get_item(**description)
    return response(res)
