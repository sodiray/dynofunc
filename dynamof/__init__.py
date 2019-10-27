from functools import partial

from dynamof.operations.add import add
from dynamof.operations.create import create
from dynamof.operations.delete import delete
from dynamof.operations.describe import describe
from dynamof.operations.find import find
from dynamof.operations.query import query
from dynamof.operations.update import update

from dynamof.attribute import attr, cand, cor

from dynamof.core.executor import execute

db = lambda client: partial(execute, client)
