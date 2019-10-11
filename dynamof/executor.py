from boto3 import resource, client

def get_client(url):
    return client('dynamodb', endpoint_url=url)


def execute(url, operation):
    runner = operation.runner
    client = get_client(url)
    return runner(client)
