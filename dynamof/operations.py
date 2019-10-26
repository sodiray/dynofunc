import copy
import collections

from dynamof.utils import new_id, shake, merge
from dynamof import runners
from dynamof import builder as ab


Operation = collections.namedtuple("Operation", [
    "description",
    "runner"
])

def create(table_name, hash_key, allow_existing=False):
    build = ab.builder('create', table_name,
        hash_key=hash_key)
    description = shake(dict(
        TableName=build(ab.TableName),
        KeySchema=build(ab.KeySchema),
        AttributeDefinitions=build(ab.AttributeDefinitions),
        ProvisionedThroughput=build(ab.ProvisionedThroughput)
    ))
    return Operation(description, runners.create(
        allow_existing=allow_existing
    ))


def find(table_name, key):
    build = ab.builder('find', table_name,
        key=key)
    description = shake(dict(
        TableName=build(ab.TableName),
        Key=build(ab.Key)
    ))
    return Operation(description, runners.find())


def add(table_name, item, auto_id=None):
    build = ab.builder('add', table_name,
        attributes=item,
        auto_id=auto_id)
    description = shake(dict(
        TableName=build(ab.TableName),
        Item=build(ab.Item),
        ReturnValues='ALL_OLD'
    ))
    return Operation(description, runners.add())


def update(table_name, key, attributes, conditions=None):
    build = ab.builder('update', table_name,
        key=key,
        attributes=attributes,
        conditions=conditions)
    description = shake(dict(
        TableName=build(ab.TableName),
        Key=build(ab.Key),
        ConditionExpression=build(ab.ConditionExpression),
        UpdateExpression=build(ab.UpdateExpression),
        ExpressionAttributeNames=build(ab.ExpressionAttributeNames),
        ExpressionAttributeValues=build(ab.ExpressionAttributeValues),
        ReturnValues='ALL_NEW'
    ))
    return Operation(description, runners.update())


def delete(table_name, key, conditions=None):
    build = ab.builder('delete', table_name,
        key=key,
        conditions=conditions)
    description = shake(dict(
        TableName=build(ab.TableName),
        Key=build(ab.Key),
        ConditionExpression=build(ab.ConditionExpression),
        ExpressionAttributeValues=build(ab.ExpressionAttributeValues)
    ))
    return Operation(description, runners.delete())

def query(table_name, conditions):
    build = ab.builder('query', table_name,
        conditions=conditions)
    description = shake(dict(
        TableName=build(ab.TableName),
        KeyConditionExpression=build(ab.KeyConditionExpression),
        ExpressionAttributeValues=build(ab.ExpressionAttributeValues)
    ))
    return Operation(description, runners.query())
