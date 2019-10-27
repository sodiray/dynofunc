
from dynamof.core import builder as ab
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def delete(table_name, key, conditions=None):
    build = ab.builder(
        table_name=table_name,
        key=key,
        conditions=conditions)
    description = shake(
        TableName=build(ab.TableName),
        Key=build(ab.Key),
        ConditionExpression=build(ab.ConditionExpression),
        ExpressionAttributeValues=build(ab.ExpressionAttributeValues))
    return Operation(description, run)

def run(client, description):
    res = client.delete_item(**description)
    return response(res)
