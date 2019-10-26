
from dynamof.core.executor import execute

from dynamof import conditions
from dynamof import funcs
from dynamof import operations

def db(client, debug=False):
    return lambda operation: execute(client, operation, debug)
