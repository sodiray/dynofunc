

def create(allow_existing):
    def run(client, description):
        try:
            return client.create_table(**description)
        except client.exceptions.ResourceInUseException as err:
            if allow_existing is False:
                raise err
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
        client.delete_item(**description)
    return run
