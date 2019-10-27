
from botocore.exceptions import ClientError

from dynamof import response
from dynamof.exceptions import factory

def handle_exceptions(func):
    def wrapper(client, description):
        try:
            return func(client, description)
        except ClientError as err:
            raise factory(err)
    return wrapper

@handle_exceptions
def create(client, description):
    res = client.create_table(**description)
    return response.create_response(res)

@handle_exceptions
def find(client, description):
    res = client.get_item(**description)
    return response.find_response(res)

@handle_exceptions
def add(client, description):
    res = client.put_item(**description)
    return response.add_response(res)

@handle_exceptions
def update(client, description):
    res = client.update_item(**description)
    return response.update_response(res)

@handle_exceptions
def delete(client, description):
    res = client.delete_item(**description)
    return response.delete_response(res)

@handle_exceptions
def query(client, description):
    res = client.query(**description)
    return response.query_response(res)

@handle_exceptions
def describe(client, description):
    res = client.describe_table(**description)
    return response.query_response(res)
