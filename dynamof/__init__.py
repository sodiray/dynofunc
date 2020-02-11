from functools import partial

from dynamof.version import VERSION

from dynamof.operations.add import add
from dynamof.operations.create import create
from dynamof.operations.delete import delete
from dynamof.operations.describe import describe
from dynamof.operations.find import find
from dynamof.operations.query import query
from dynamof.operations.update import update
from dynamof.operations.scan import scan

from dynamof.attribute import attr, cand, cor

from dynamof.core.executor import execute
from dynamof.core.utils import immutable

db = lambda client: partial(execute, client)

def table(a_db, table_name):

    def wrap_op(op):
        def call_op(*args, **kwargs):
            return a_db(op(table_name, *args, **kwargs))
        return call_op

    return immutable(
        add=wrap_op(add),
        create=wrap_op(create),
        delete=wrap_op(delete),
        describe=wrap_op(describe),
        find=wrap_op(find),
        query=wrap_op(query),
        update=wrap_op(update),
        scan=wrap_op(scan))
