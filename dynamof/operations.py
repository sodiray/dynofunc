import copy
import collections
from dynamof import builder as ab
from dynamof import runners


Operation = collections.namedtuple("Operation", [
    "description",
    "runner"
])


def create(table_name, hash_key, allow_existing=False):
    description = dict(
        TableName=table_name,
        KeySchema=ab.key_schema(hash_key),
        AttributeDefinitions=ab.attribute_definitions([hash_key]),
        ProvisionedThroughput=ab.provisioned_throughput()
    )
    return Operation(description, runners.create(
        allow_existing=allow_existing
    ))


def find(table_name, key):
    request = ab.build_request_tree(
        table_name=table_name,
        key=key)
    description = dict(
        TableName=table_name,
        Key=ab.build_key_arg(request)
    )
    return Operation(description, runners.find())


def add(table_name, item, auto_id=None):
    attributes = copy.deepcopy(item)
    request = ab.build_request_tree(
        table_name=table_name,
        attributes=attributes,
        auto_id=auto_id)
    description = dict(
        TableName=table_name,
        Item=ab.build_expression_attribute_values(request),
        ReturnValues='ALL_OLD'
    )
    return Operation(description, runners.add())


def update(table_name, key, attributes, conditions=None):
    request = ab.build_request_tree(
        table_name=table_name,
        key=key,
        attributes=attributes,
        conditions=conditions)
    description = dict(
        TableName=table_name,
        Key=ab.build_key_arg(request),
        ConditionExpression=ab.build_condition_expression(request),
        UpdateExpression=ab.build_update_expression(request),
        ExpressionAttributeNames=ab.build_expression_attribute_names(request),
        ExpressionAttributeValues=ab.build_expression_attribute_values(request),
        ReturnValues='ALL_NEW'
    )
    return Operation(description, runners.update())


def delete(table_name, key):
    request = ab.build_request_tree(
        table_name=table_name,
        key=key)
    description = dict(
        TableName=table_name,
        Key=ab.build_key_arg(request),
        ConditionExpression=ab.build_condition_expression(request),
        ExpressionAttributeValues=ab.build_expression_attribute_values(request)
    )
    return Operation(description, runners.delete())

def query(table_name, conditions):
    request = ab.build_request_tree(
        table_name=table_name,
        conditions=conditions)
    description = dict(
        TableName=table_name,
        KeyConditionExpression=ab.build_condition_expression(request),
        ExpressionAttributeValues=ab.build_expression_attribute_values(request)
    )
    return Operation(description, runners.query())
