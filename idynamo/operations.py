from boto3 import resource, client

from idynamo import arg_builder as ab

def resource_provider(url):
    return resource('dynamodb', endpoint_url=url)

def operation(description, provider):
    return {
        'description': description,
        'provider': provider
    }

def create(name, hash_key):
    description = dict(
        TableName=name,
        KeySchema=ab.build_key_schema(hash_key),
        AttributeDefinitions=ab.build_attribute_definitions([hash_key]),
        ProvisionedThroughput=ab.build_provisioned_throughput()
    )
    return operation(description, resource_provider)
