
from dynamof.core import builder as ab
from dynamof.core import args
from dynamof.core.utils import shake
from dynamof.core.model import Operation, Condition
from dynamof.core.response import response


def update(table_name: str, key: dict, attributes: dict, conditions: Condition = None):
    """Creates an Operation that will update any items that match the given key with the given
    attributes when run.

    Args:
        table_name (str): The name of the table to update items in
        key (dict): The key that represents an identifier for the item/s to update
            Examples:
                - { 'username': 'sunshie' }
                - { 'id': '9snw82h', 'type': 'car' } -> when table uses hash key and range key
        attributes (dict): An arbitrary object of key values to set on the item when updating
            Examples:
                - { 'color': 'red', 'size': 'large' }
                - { 'username': 'sunshie12' }
        conditions (Condition, optional): A condition object that should be used to filter which items are updated
            Examples:
                - query('products', conditions: attr('title').equals('Old Buggy'))
                - query('products', conditions: cand(attr('type').equals('car'), attr('color').equals('red'))

    """
    build = ab.builder(
        table_name=table_name,
        key=key,
        attributes=attributes,
        conditions=conditions)
    description = shake(
        TableName=build(args.TableName),
        Key=build(args.Key),
        ConditionExpression=build(args.ConditionExpression),
        UpdateExpression=build(args.UpdateExpression),
        ExpressionAttributeNames=build(args.ExpressionAttributeNames),
        ExpressionAttributeValues=build(args.ExpressionAttributeValues),
        ReturnValues='ALL_NEW')
    return Operation(description, run)

def run(client, description):
    res = client.update_item(**description)
    return response(res)
