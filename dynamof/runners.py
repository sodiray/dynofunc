
from botocore.exceptions import ClientError

from dynamof import response
from dynamof.exceptions import (
    UnknownDatabaseException,
    PreexistingTableException,
    ConditionNotMetException,
    BadGatewayException,
    TableDoesNotExistException
)

def handle_exceptions(allow_existing=False):
    def decorator(func):
        def wrapper(client, description):
            try:
                return func(client, description)
            except ClientError as err:
                if BadGatewayException.matches(err): raise BadGatewayException()
                if TableDoesNotExistException.matches(err): raise TableDoesNotExistException().info(description.get('TableName'))
                if ConditionNotMetException.matches(err): raise ConditionNotMetException().info(description.get('ConditionExpression'))
                if PreexistingTableException.matches(err):
                    if allow_existing is False:
                        table_name = description.get('TableName')
                        raise PreexistingTableException().info(f'table={table_name}')
                    return response.create_response(None, skipped=True)
                raise UnknownDatabaseException()
        return wrapper
    return decorator

def create(allow_existing):

    @handle_exceptions(allow_existing=allow_existing)
    def run(client, description):
        res = client.create_table(**description)
        return response.create_response(res)
    return run

def find():
    @handle_exceptions()
    def run(client, description):
        res = client.get_item(**description)
        return response.find_response(res)
    return run

def add():
    @handle_exceptions()
    def run(client, description):
        res = client.put_item(**description)
        return response.add_response(res)
    return run

def update():
    @handle_exceptions()
    def run(client, description):
        res = client.update_item(**description)
        return response.update_response(res)
    return run

def delete():
    @handle_exceptions()
    def run(client, description):
        res = client.delete_item(**description)
        return response.delete_response(res)
    return run

def query():
    @handle_exceptions()
    def run(client, description):
        res = client.query(**description)
        return response.query_response(res)
    return run

def describe():
    @handle_exceptions()
    def run(client, description):
        res = client.describe_table(**description)
        return response.query_response(res)
    return run
