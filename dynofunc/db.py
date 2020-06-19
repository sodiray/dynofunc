from functools import partial

from dynofunc.core.executor import execute


def db(client):
    return partial(execute, client)
