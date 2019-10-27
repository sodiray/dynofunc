
from dynamof.core import builder as ab
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def query(table_name, conditions):
    build = ab.builder(
        table_name=table_name,
        conditions=conditions)
    description = shake(
        TableName=build(ab.TableName),
        KeyConditionExpression=build(ab.KeyConditionExpression),
        ExpressionAttributeNames=build(ab.ExpressionAttributeNames),
        ExpressionAttributeValues=build(ab.ExpressionAttributeValues))
    return Operation(description, run)

def run(client, description):
    res = client.query(**description)
    return response(res)
