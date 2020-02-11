from dynamof.operations.add import add
from dynamof.operations.create import create
from dynamof.operations.delete import delete
from dynamof.operations.describe import describe
from dynamof.operations.find import find
from dynamof.operations.query import query
from dynamof.operations.update import update
from dynamof.operations.scan import scan

from dynamof.core.utils import immutable


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
