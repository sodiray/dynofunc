
from botocore.exceptions import ClientError

from dynamof import response
from dynamof.exceptions import (
    UnknownDatabaseException,
    PreexistingTableException,
    ConditionNotMetException,
    BadGatewayException,
    TableDoesNotExistException
)

def create(allow_existing):
    def run(client, description):
        try:
            res = client.create_table(**description)
        except Exception as err:  # pylint: disable=broad-except
            if BadGatewayException.matches(err): raise BadGatewayException()
            if PreexistingTableException.matches(err):
                if allow_existing is False:
                    table_name = description.get('TableName')
                    raise PreexistingTableException().info(f'table={table_name}')
                return response.create_response(None, skipped=True)
            raise UnknownDatabaseException()
        return response.create_response(res)

    return run

def find():
    def run(client, description):
        try:
            res = client.get_item(**description)
        except ClientError as err:
            if BadGatewayException.matches(err): raise BadGatewayException()
            if TableDoesNotExistException.matches(err): raise TableDoesNotExistException().info(description.get('TableName'))
            if ConditionNotMetException.matches(err): raise ConditionNotMetException().info(description.get('ConditionExpression'))
            raise UnknownDatabaseException()
        return response.find_response(res)
    return run

def add():
    def run(client, description):
        try:
            res = client.put_item(**description)
        except ClientError as err:
            if BadGatewayException.matches(err): raise BadGatewayException()
            if TableDoesNotExistException.matches(err): raise TableDoesNotExistException().info(description.get('TableName'))
            raise UnknownDatabaseException()
        return response.add_response(res)
    return run

def update():
    def run(client, description):
        try:
            res = client.update_item(**description)
        except ClientError as err:
            if BadGatewayException.matches(err): raise BadGatewayException()
            if TableDoesNotExistException.matches(err): raise TableDoesNotExistException().info(description.get('TableName'))
            if ConditionNotMetException.matches(err): raise ConditionNotMetException().info(description.get('ConditionExpression'))
            raise UnknownDatabaseException()
        return response.update_response(res)
    return run

def delete():
    def run(client, description):
        try:
            res = client.delete_item(**description)
        except ClientError as err:
            if BadGatewayException.matches(err): raise BadGatewayException()
            if TableDoesNotExistException.matches(err): raise TableDoesNotExistException().info(description.get('TableName'))
            if ConditionNotMetException.matches(err): raise ConditionNotMetException().info(description.get('ConditionExpression'))
            raise UnknownDatabaseException()
        return response.delete_response(res)
    return run

def query():
    def run(client, description):
        try:
            res = client.query(**description)
        except ClientError as err:
            if BadGatewayException.matches(err): raise BadGatewayException()
            if TableDoesNotExistException.matches(err): raise TableDoesNotExistException().info(description.get('TableName'))
            if ConditionNotMetException.matches(err): raise ConditionNotMetException().info(description.get('ConditionExpression'))
            raise UnknownDatabaseException()
        return response.query_response(res)
    return run
