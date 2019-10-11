import sys

from dynamof import exceptions

def create(allow_existing):
    def run(client, description):
        try:
            return client.create_table(**description)
        except Exception as err:
            if exceptions.PreexistingTableException.maps_to(err):
                if allow_existing is False:
                    table_name = description.get('TableName')
                    raise exceptions.PreexistingTableException().info(f'table={table_name}')
    return run

def find():
    def run(client, description):
        return client.get_item(**description)
    return run

def add():
    def run(client, description):
        return client.put_item(**description)
    return run

def update():
    def run(client, description):
        return client.update_item(**description)
    return run

def delete():
    def run(client, description):
        return client.delete_item(**description)
    return run
