
# Dynamof
A small interface for more easily making calls to dynamo using boto. No bloated ORM - just functions that make creating boto3 dynamo action descriptions easy.

## Basic Features

- Simplifying `boto3` function APIs ([see an example](#examples))
> If you've ever used boto3 directly before you know the pain that can exist trying to write a dynamic `KeyCondition` or `ConditionExpression`. `dynamof` does these things for you.

- Standardizing `boto3` error handling ([see an example](#examples))
> If you've ever used boto3 directly you know that handling errors is the absolute worst... how much time I've spent googling how to catch this error or that error.... and they're all different! `dynamof` wraps the calls to boto3, catches all of its errors in all of their uniquely identifiable ways and exposes a concise error api that works with the standard `try ... except`.

- Customizable api
> Because doing it how I do it probably isn't for you.

`dynamof` wraps the `boto3.client('dynamodb')` ([docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#dynamodb)) functions exposing much easier to use api's. It's written in a functional style with the goal to be as useful to anyone in any way as possible. The wrappers around boto3 functions are split into two parts: `operations` and `runners`. A runner runs a specific operations. The operation contains all the necessary information for a dynamo action to be ran. This means, you don't have to use `dynamof` to actually interact with dynamo if you don't want to but you could still use it as a utility to more easily generate the complex objects that are passed to boto3 functions.

## Example: Create a table in dynamo
```
from boto3 import client
from dynamof.executor import execute
from dynamof.operations import create

client = client('dynamodb', endpoint_url='http://localstack:4569')

execute(client, create(table_name='users', hash_key='username'))
```
First thing to note... `execute(client, some_operation(...))` isn't _sexy_... and as engineers _sexy_ is important. Because `dynamof` is a simple functional utility library its very easy to bend it into any api you would like.

## Example: Customize the way you call dynamof
```
# Keep it functional

from functools import partial
from boto3 import client
from dynamof.executor import execute
from dynamof.operations import create

client = client('dynamodb', endpoint_url='http://localstack:4569')
db = partial(execute, client)

# Now calling looks like
db(create(...))
db(find(...))
db(update(...))

# Make it a class

class DB:
  def __init__(self):
    self.client = client('dynamodb', endpoint_url='http://localstack:4569')
  def find(*args, **kwargs):
    return execute(client, find(*args, **kwargs))

db = DB()
db.find(key={ 'id': 21 })

```

## Example: Catch errors from dynamof
```
from dynamof.exceptions import (
    UnknownDatabaseException,
    ConditionNotMetException,
    BadGatewayException,
    TableDoesNotExistException
)

try:
  db(update(
    table_name='users',
    key={ 'id': 43 },
    attributes={ 'username': 'sunshie' }))
except TableDoesNotExistException:
  # Handle case where table doesn't exist
except ConditionNotMetException:
  # Handle case where the condition wasn't met (the item you tried to update didn't exist)
except BadGatewayException:
  # Handle a network error
except UnknownDatabaseException:
  # Handle an unknown issue

```

## Example: Use dynamof as sugar to call boto3 yourself
```
from dynamof import operations
from dynamof.conditions import attr


query = operations.query(
  table_name='books',
  conditions=attr('title').equals('The Cost of Discipleship'))

result = client.query(**query.description)
```

## Why Dynamof?
If you're using python and dynamo you have 2 options: an ORM like PynamoDB or Boto3. Kudos to the people who made Pynamo, its great, but it really doesn't scale well. And your stuck with the ORM features even if you don't want them. Interacting with Boto3 directly is a pain. With things like `KeyCondition`s and `ConditionExpression`s being so difficult to easily grasp you end up duplicating a lot of code in your database/repository/DAL layer. This was my experience. In my early day's I used Pynamo. Once I got tired of trying to bend it to my will at scale I started using Boto3 directly. But... this was still annoying. I wanted a non-opinonated library that could sit on top of Botot3 and do the repetitive, annoying to code work for me. `dynamof` was born.

# API Documentation
[dynamof.operations](#operations)  
[dynamof.exceptions](#exceptions)  
[dynamof.conditions](#conditions)  
[dynamof.builder](#builder)  

## Operations
[See the code](dynamof/operations.py)  
[See the test](test/unit/operations_test.py)  

### create(table_name, hash_key, allow_existing=False)

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name to assign the table your creating | `'users'` |
| `hash_key` | yes | `str` | The hash key (primary key) for your table | `'user_id'` |
| `allow_existing` | no | `bool` | Creating a table that already exists will throw an error in boto3. Passing `True` here will ignore that error if its raised and ignore it. | `True` |

#### Limitations
- Cannot specify range key
- Cannot specify complex hash key (hash key and range key)
- Cannot specify indexes
- Other boto3 parameters not implemented (`BillingMode`, `ProvisionedThroughput`, `StreamSpecification`, `SSESpecification`, `Tags`)

### find(table_name, key)

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.get_item)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name of the table to find an item in | `'users'` |
| `key` | yes | `str`\|`dict` | The key (primary key) of the item to find. If a string is passed it is associated with `id` by default. If an object is passed the first key and value are used to find the item | `22` or ```{ 'username': 'sunshie' }``` |

#### Limitations
- Cannot use projection expressions
- Other boto3 parameters not implemented (`ConsistentRead`, `ReturnConsumedCapacity`)


### add(table_name, item, auto_inc=False)

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name of the table to add the item to | `'users'` |
| `item` | yes | `dict` | The item to be added to the table in key value pairs. If `auto_inc` is not set to true then this dict **must** include a valid key value pair for the table's hash key | ```{ 'username': 'sunshie', 'user_status': 'unleashed' }``` |

#### Limitations
- boto3 parameters not implemented: `ReturnItemCollectionMetrics`, `ReturnConsumedCapacity`, `ReturnValues`

### Known Issues
- When the table you're trying to add to does not exist the `put_item` function in boto3 does not throw the expected `ClientError` with the table not found code and message. Instead, it throws a bad gateway error. So, when calling `add` you cannot depend on the `TableDoesNotExistException`. In a future version you will be able to use an additonal method to check if the table exists if needed.


... more docs to come...





## Roadmap

- [x] only use client & kill resource
- [x] testing
- [x] linter
- [x] implement query
- [x] implement response object & destructure response Item tree
- [x] handle errors
- [x] documentation   
**version 1.0.0**
- [] implement scan
- [] query support pagination
- [] query support indexes
- [] support projection expressions
- [] support filter expressions   
**version 1.2.0**
- [] batch operations
- [] metadata operations
- [] update table operation
