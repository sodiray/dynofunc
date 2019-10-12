
from dynamof import exceptions
from dynamof import response

def create(allow_existing):
    def run(client, description):
        try:
            res = client.create_table(**description)
            return response.create_response(res)
        except Exception as err:  # pylint: disable=broad-except
            if exceptions.PreexistingTableException.maps_to(err):
                if allow_existing is False:
                    table_name = description.get('TableName')
                    raise exceptions.PreexistingTableException().info(f'table={table_name}')
                return response.create_response(None, skipped=True)

    return run

def find():
    def run(client, description):
        res = client.get_item(**description)
        return response.find_response(res)
    return run

def add():
    def run(client, description):
        res = client.put_item(**description)
        return response.add_response(res)
    return run

def update():
    def run(client, description):
        res = client.update_item(**description)
        return response.update_response(res)
    return run

def delete():
    def run(client, description):
        res = client.delete_item(**description)
        return response.delete_response(res)
    return run

def query():
    def run(client, description):
        res = client.query(**description)
        return response.query_response(res)
    return run
