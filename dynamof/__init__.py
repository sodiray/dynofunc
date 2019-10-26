
from dynamof.core.executor import execute

from dynamof.attribute import attr, cand, cor
from dynamof import operations
from dynamof import exceptions

def db(client, debug=False):
    return lambda operation: execute(client, operation, debug)
