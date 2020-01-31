
from dynamof.core import builder as ab
from dynamof.core import args
from dynamof.core.utils import shake
from dynamof.core.model import Operation, Condition
from dynamof.core.response import response


def query(table_name: str, conditions: Condition, index_name: str = None):
    """Creates an Operation that will query a table for items that match the given
    conditions when run.

    Args:
        table_name (str): The name of the table to query
        conditions (Condition): A condition object that should be used to determine which items to return
            Examples:
                - query('products', conditions: attr('title').equals('Old Buggy'))
                - query('products', conditions: cand(attr('type').equals('car'), attr('color').equals('red'))

    """
    build = ab.builder(
        table_name=table_name,
        index_name=index_name,
        conditions=conditions)
    description = shake(
        TableName=build(args.TableName),
        IndexName=build(args.IndexName),
        KeyConditionExpression=build(args.KeyConditionExpression),
        ExpressionAttributeNames=build(args.ExpressionAttributeNames),
        ExpressionAttributeValues=build(args.ExpressionAttributeValues))
    return Operation(description, run)

def run(client, description):
    res = client.query(**description)
    return response(res)
