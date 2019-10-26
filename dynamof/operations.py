import copy
import json
import collections

from dynamof.utils import new_id, shake, merge
from dynamof import runners
from dynamof import builder as ab


Operation = collections.namedtuple("Operation", [
    "description",
    "runner"
])

def create(table_name, hash_key, allow_existing=False, debug=False):
    build = ab.builder('create', table_name,
        hash_key=hash_key)
    description = shake(dict(
        TableName=build(ab.TableName),
        KeySchema=build(ab.KeySchema),
        AttributeDefinitions=build(ab.AttributeDefinitions),
        ProvisionedThroughput=build(ab.ProvisionedThroughput)
    ))
    if debug is True:
        print('############\nCREATE\n############')
        print(json.dumps(description, indent=2))
    return Operation(description, runners.create(
        allow_existing=allow_existing
    ))


def find(table_name, key, debug=False):
    build = ab.builder('find', table_name,
        key=key)
    description = shake(dict(
        TableName=build(ab.TableName),
        Key=build(ab.Key)
    ))
    if debug is True:
        print('############\nFIND\n############')
        print(json.dumps(description, indent=2))
    return Operation(description, runners.find())


def add(table_name, item, auto_id=None, debug=False):
    build = ab.builder('add', table_name,
        attributes=item,
        auto_id=auto_id)
    description = shake(dict(
        TableName=build(ab.TableName),
        Item=build(ab.Item),
        ReturnValues='ALL_OLD'
    ))
    if debug is True:
        print('############\nADD\n############')
        print(json.dumps(description, indent=2))
    return Operation(description, runners.add())


def update(table_name, key, attributes, conditions=None, debug=False):
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
    if debug is True:
        print('############\nUPDATE\n############')
        print(json.dumps(description, indent=2))
    return Operation(description, runners.update())


def delete(table_name, key, conditions=None, debug=False):
    build = ab.builder('delete', table_name,
        key=key,
        conditions=conditions)
    description = shake(dict(
        TableName=build(ab.TableName),
        Key=build(ab.Key),
        ConditionExpression=build(ab.ConditionExpression),
        ExpressionAttributeValues=build(ab.ExpressionAttributeValues)
    ))
    if debug is True:
        print('############\nDELETE\n############')
        print(json.dumps(description, indent=2))
    return Operation(description, runners.delete())

def query(table_name, conditions, debug=False):
    build = ab.builder('query', table_name,
        conditions=conditions)
    description = shake(dict(
        TableName=build(ab.TableName),
        KeyConditionExpression=build(ab.KeyConditionExpression),
        ExpressionAttributeNames=build(ab.ExpressionAttributeNames),
        ExpressionAttributeValues=build(ab.ExpressionAttributeValues)
    ))
    if debug is True:
        print('############\nQUERY\n############')
        print(json.dumps(description, indent=2))
    return Operation(description, runners.query())
