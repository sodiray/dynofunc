
from dynamof.core import builder as ab
from dynamof.core.utils import shake
from dynamof.core.model import Operation
from dynamof.core.response import response


def create(table_name, hash_key):
    build = ab.builder(
        table_name=table_name,
        hash_key=hash_key)
    description = shake(
        TableName=build(ab.TableName),
        KeySchema=build(ab.KeySchema),
        AttributeDefinitions=build(ab.AttributeDefinitions),
        ProvisionedThroughput=build(ab.ProvisionedThroughput))
    return Operation(description, run)

def run(client, description):
    res = client.create_table(**description)
    return response(res)
