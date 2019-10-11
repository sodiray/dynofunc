from idynamo import arg_builder as ab

def operation(description, provider, runner):
    return {
        'description': description,
        'provider': provider,
        'runner': runner
    }

def create(name, hash_key):
    description = dict(
        TableName=name,
        KeySchema=ab.build_key_schema(hash_key),
        AttributeDefinitions=ab.build_attribute_definitions([hash_key]),
        ProvisionedThroughput=ab.build_provisioned_throughput()
    )
    def run(resource):
        resource.create_table(**description)
    return operation(description, 'resource', run)
