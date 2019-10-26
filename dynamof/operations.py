
from dynamof.core.utils import shake, immutable
from dynamof import runners
from dynamof.core import builder as ab


def operation(name, description, runner):
    return immutable(
        name=name,
        description=description,
        runner=runner)

def create(table_name, hash_key, allow_existing=False):
    build = ab.builder('create', table_name,
        hash_key=hash_key)
    description = shake(dict(
        TableName=build(ab.TableName),
        KeySchema=build(ab.KeySchema),
        AttributeDefinitions=build(ab.AttributeDefinitions),
        ProvisionedThroughput=build(ab.ProvisionedThroughput)
    ))
    return operation(
        'create',
        description,
        runners.create(
            allow_existing=allow_existing
        ))

def find(table_name, key):
    build = ab.builder('find', table_name,
        key=key)
    description = shake(dict(
        TableName=build(ab.TableName),
        Key=build(ab.Key)
    ))
    return operation(
        'find',
        description,
        runners.find())

def add(table_name, item, auto_id=None):
    build = ab.builder('add', table_name,
        attributes=item,
        auto_id=auto_id)
    description = shake(dict(
        TableName=build(ab.TableName),
        Item=build(ab.Item),
        ReturnValues='ALL_OLD'
    ))
    return operation(
        'add',
        description,
        runners.add())

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
    return operation(
        'update',
        description,
        runners.update())

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
    return operation(
        'delete',
        description,
        runners.delete())

def query(table_name, conditions):
    build = ab.builder('query', table_name,
        conditions=conditions)
    description = shake(dict(
        TableName=build(ab.TableName),
        KeyConditionExpression=build(ab.KeyConditionExpression),
        ExpressionAttributeNames=build(ab.ExpressionAttributeNames),
        ExpressionAttributeValues=build(ab.ExpressionAttributeValues)
    ))
    return operation(
        'query',
        description,
        runners.query())

def describe(table_name):
    build = ab.builder('describe', table_name)
    description = shake(dict(
        TableName=build(ab.TableName)
    ))
    return operation('describe', description, runners.describe())
