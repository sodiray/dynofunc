
from dynamof.core import builder as ab
from dynamof.core import args
from dynamof.core.utils import shake
from dynamof.core.model import Operation, Condition
from dynamof.core.response import response


def delete(table_name: str, key: dict, conditions: Condition = None):
    """Creates an Operation that will create a table when run.

    Args:
        table_name (str): The name of the table to delete an item from
        key (dict): An object with a key, value that will be used as the identifier of the item to delete
            Examples:
                - { 'username': 'sunshie' }
                - { 'id': '9snw82h', 'type': 'car' } -> when table uses hash key and range key
        conditions (Condition, optional): If provided, will be used to create a condition for the delete
            Example:
                - delete('products', { 'id': 12 }, conditions: attr('title').equals('Old Buggy'))

    """
    build = ab.builder(
        table_name=table_name,
        key=key,
        conditions=conditions)
    description = shake(
        TableName=build(args.TableName),
        Key=build(args.Key),
        ConditionExpression=build(args.ConditionExpression),
        ExpressionAttributeValues=build(args.ExpressionAttributeValues))
    return Operation(description, run)

def run(client, description):
    res = client.delete_item(**description)
    return response(res)
