
from dynamof.executor import execute

def db(client, debug=False):
    return lambda operation: execute(client, operation, debug)
