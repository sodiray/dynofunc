
from dynamof.core import builder as ab
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def update(table_name, key, attributes, conditions=None):
    build = ab.builder(
        table_name=table_name,
        key=key,
        attributes=attributes,
        conditions=conditions)
    description = shake(
        TableName=build(ab.TableName),
        Key=build(ab.Key),
        ConditionExpression=build(ab.ConditionExpression),
        UpdateExpression=build(ab.UpdateExpression),
        ExpressionAttributeNames=build(ab.ExpressionAttributeNames),
        ExpressionAttributeValues=build(ab.ExpressionAttributeValues),
        ReturnValues='ALL_NEW')
    return Operation(description, run)

def run(client, description):
    res = client.update_item(**description)
    return response(res)
