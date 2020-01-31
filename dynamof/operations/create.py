
from dynamof.core import builder as ab
from dynamof.core import args
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def create(table_name: str, hash_key: str, range_key: str = None, gsi: str = None, lsi: str = None):
    """Creates an Operation that will create a table when run.

    Args:
        table_name (str): The name of the table to create
        hash_key (str): The name of the hash key to use for the table
        range_key (str, optional): If provided, will be used as the name of the range key attribute for the table
        gsi (str, optional): If provided, will be used as the name for a global secondary index
        lsi (str, optional): If provided, will be used as the name for a local secondary index

    """
    build = ab.builder(
        table_name=table_name,
        hash_key=hash_key,
        range_key=range_key,
        gsi=gsi,
        lsi=lsi)
    description = shake(
        TableName=build(args.TableName),
        KeySchema=build(args.KeySchema),
        AttributeDefinitions=build(args.AttributeDefinitions),
        ProvisionedThroughput=build(args.ProvisionedThroughput),
        LocalSecondaryIndexes=build(args.LocalSecondaryIndexes),
        GlobalSecondaryIndexes=build(args.GlobalSecondaryIndexes))
    return Operation(description, run)

def run(client, description):
    res = client.create_table(**description)
    return response(res)
