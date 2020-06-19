from dynofunc.operations.add import add
from dynofunc.operations.create import create
from dynofunc.operations.delete import delete
from dynofunc.operations.describe import describe
from dynofunc.operations.find import find
from dynofunc.operations.query import query
from dynofunc.operations.update import update
from dynofunc.operations.scan import scan

from dynofunc.core.utils import immutable


def table(db, table_name):

    def wrap_op(op):
        def call_op(*args, **kwargs):
            return db(op(table_name, *args, **kwargs))
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
