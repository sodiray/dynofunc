from functools import partial

from dynamof.core.executor import execute


def db(client):
    return partial(execute, client)
