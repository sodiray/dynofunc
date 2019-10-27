
from dynamof.core import builder as ab
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def add(table_name, item, auto_id=None):
    build = ab.builder(
        table_name=table_name,
        attributes=item,
        auto_id=auto_id)
    description = shake(
        TableName=build(ab.TableName),
        Item=build(ab.Item),
        ReturnValues='ALL_OLD')
    return Operation(description, run)

def run(client, description):
    res = client.put_item(**description)
    return response(res)
