
from functools import wraps
from boto3 import resource, client


def new_id():
    return str(uuid.uuid4())

def use_resource(func):
    @wraps(func)
    def wrapper(url, table_name):
        r = resource('dynamodb', endpoint_url=url)
        t = r.Table(table_name)
        return func(t)
    return wrapper

@handle_errors
@use_resource
def find(self, id):
    return get_resource(self.url)
        .table(self.table_name)
        .get_item()
    return response['Item']

@handle_errors
@use_resource
def add(self, item):
    if not hasattr(item, 'id'):
        item['id'] = new_id()
    self.table().put_item(Item=item)
    return item

@handle_errors
@use_resource
def update(self, id, data):
    condition_expression_obj = ab.build_condition_expression(id)
    kwargs = dict(
        Key=ab.build_key(id),
        ConditionExpression=Key(condition_expression_obj['name']).eq(condition_expression_obj['value']),
        UpdateExpression=ab.build_update_expression(data),
        ExpressionAttributeValues=ab.build_expression_attribute_values(data)
    )
    self.table().update_item(**kwargs)

@handle_errors
@use_resource
def delete(self, id):
    condition_expression_obj = ab.build_condition_expression(id)
    kwargs = dict(
        Key = ab.build_key(id),
        ConditionExpression = Key(condition_expression_obj['name']).eq(condition_expression_obj['value']),
    )
    self.table().delete_item(**kwargs)
