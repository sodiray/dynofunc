import copy
from boto3.dynamodb.conditions import Key
from dynamof import arg_builder as ab
from dynamof.utils import new_id


def operation(description, provider, runner):
    return {
        'description': description,
        'provider': provider,
        'runner': runner
    }


def create(table_name, hash_key, allow_existing=False):
    description = dict(
        TableName=table_name,
        KeySchema=ab.build_key_schema(hash_key),
        AttributeDefinitions=ab.build_attribute_definitions([hash_key]),
        ProvisionedThroughput=ab.build_provisioned_throughput()
    )
    def run(client):
        try:
            return client.create_table(**description)
        except client.exceptions.ResourceInUseException as err:
            if allow_existing is False:
                raise err
    return operation(description, 'client', run)


def find(table_name, key):
    description = dict(
        Key=ab.build_key(key)
    )
    def run(resource):
        return resource.Table(table_name).get_item(**description)
    return operation(description, 'resource', run)


def add(table_name, item, auto_inc=False):
    attributes = copy.deepcopy(item)
    if auto_inc is True:
        attributes['id'] = new_id()
    description = dict(
        Item=attributes
    )
    def run(resource):
        return resource.Table(table_name).put_item(**description)
    return operation(description, 'resource', run)


def update(table_name, key, attributes):
    condition_expression_obj = ab.build_condition_expression(key)
    description = dict(
        Key=ab.build_key(key),
        ConditionExpression=Key(condition_expression_obj['name']).eq(condition_expression_obj['value']),
        UpdateExpression=ab.build_update_expression(attributes),
        ExpressionAttributeValues=ab.build_expression_attribute_values(attributes)
    )
    def run(resource):
        resource.Table(table_name).update_item(**description)
    return operation(description, 'resource', run)


def delete(table_name, key):
    condition_expression_obj = ab.build_condition_expression(key)
    description = dict(
        Key = ab.build_key(key),
        ConditionExpression = Key(condition_expression_obj['name']).eq(condition_expression_obj['value']),
    )
    def run(resource):
        resource.Table(table_name).delete_item(**description)
    return operation(description, 'resource', run)
