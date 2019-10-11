from boto3 import resource, client

def resource_provider(url):
    return resource('dynamodb', endpoint_url=url)

def operation(description, provider):
    return {
        'description': description,
        'provider': provider
    }

def create(name, hash_key):
    description = {

    }
    return operation(description, resource_provider)
