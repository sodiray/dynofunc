
# Dynamof

![Travis (.org](https://img.shields.io/travis/rayepps/dynamof)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e8c1e3cf175c007a591a/test_coverage)](https://codeclimate.com/github/rayepps/dynamof/test_coverage)
![PyPI - License](https://img.shields.io/pypi/l/dynamof)

A small :fire: interface for more easily making calls to dynamo using boto. No bloated ORM - just functions that make creating the complex objects needed to pass to boto3 quick and easy.

## Basic Features

- Simplifying `boto3` function APIs ([see an example](#example-create-a-table-in-dynamo))
> If you've ever used boto3 directly before you know the pain that can exist trying to write a dynamic `KeyCondition` or `ConditionExpression`. `dynamof` does these things for you.

- Standardizing `boto3` error handling ([see an example](#example-catch-errors-from-dynamof))
> If you've ever used boto3 directly you know that handling errors is the absolute worst... how much time I've spent googling how to catch this error or that error.... and they're all different! `dynamof` wraps the calls to boto3, catches all of its errors in all of their uniquely identifiable ways and exposes a concise error api that works with the standard `try ... except`.

- Customizable api ([see an example](#example-create-a-table-in-dynamo))
> Because doing it how I do it probably isn't for you.

`dynamof` wraps the `boto3.client('dynamodb')` ([docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#dynamodb)) functions exposing much easier to use api's. It's written in a functional style with the goal to be as useful to anyone in any way as possible. The wrappers around boto3 functions are split into two parts: `operations` and `runners`. A runner runs a specific operations. The operation contains all the necessary information for a dynamo action to be ran. This means, you don't have to use `dynamof` to actually interact with dynamo if you don't want to but you could still use it as a utility to more easily generate the complex objects that are passed to boto3 functions.

## Example: Create a table in dynamo
```py
from boto3 import client
from dynamof.executor import execute
from dynamof.operations import create

client = client('dynamodb', endpoint_url='http://localstack:4569')

execute(client, create(table_name='users', hash_key='username'))
```
First thing to note... `execute(client, some_operation(...))` isn't _sexy_... and as engineers _sexy_ is important. Because `dynamof` is a simple functional utility library its very easy to bend it into any api you would like.

## Example: Customize the way you call dynamof
```py
##
## Keep it functional
##

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

##
## Make it a class
##

class DB:
  def __init__(self):
    self.client = client('dynamodb', endpoint_url='http://localstack:4569')
  def find(*args, **kwargs):
    return execute(self.client, find(*args, **kwargs))

db = DB()
db.find(table_name='users', key={ 'id': 21 })

##
## Make it a table specific class
##

class Table:
  def __init__(self, table_name):
    client = client('dynamodb', endpoint_url='http://localstack:4569')
    self.table_name = table_name
    self.db = partial(execute, client)
  def find(*args, **kwargs):
    return self.db(find(self.table_name, *args, **kwargs))
  def update(*args, **kwargs):
    return self.db(update(self.table_name, *args, **kwargs))
  def delete(*args, **kwargs):
    return self.db(delete(self.table_name, *args, **kwargs))


users = Table('users')

users.find(key={ 'id': 21 })
users.update(key={ 'id': 21 }, attributes={ 'username': 'new_username_1993_bro' })
users.delete(key={'id': 21 })

```

## Example: Catch errors from dynamof
```py
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
```py
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
[dynamof.conditions](#conditions)  
[dynamof.exceptions](#exceptions)   
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

#### :orange_book: Limitations
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

#### :orange_book: Limitations
- Cannot use projection expressions
- Other boto3 parameters not implemented (`ConsistentRead`, `ReturnConsumedCapacity`)


### add(table_name, item, auto_inc=False)

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name of the table to add the item to | `'users'` |
| `item` | yes | `dict` | The item to be added to the table in key value pairs. If `auto_inc` is not set to true then this dict **must** include a valid key value pair for the table's hash key | ```{ 'username': 'sunshie', 'user_status': 'unleashed' }``` |

#### :orange_book: Limitations
- boto3 parameters not implemented: `ReturnItemCollectionMetrics`, `ReturnConsumedCapacity`, `ReturnValues`

#### :closed_book: Known Issues
- When the table you're trying to add to does not exist the `put_item` function in boto3 does not throw the expected `ClientError` with the table not found code and message. Instead, it throws a bad gateway error. So, when calling `add` you cannot depend on the `TableDoesNotExistException`. In a future version you will be able to use an additonal method to check if the table exists if needed.


### update(table_name, key, attributes)

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_item)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name of the table to update the item on | `'users'` |
| `key` | yes | `str`\|`dict` | The key (primary key) of the item to find for updating. If a string is passed it is associated with `id` by default. If an object is passed the first key and value are used to find the item | `22` or ```{ 'username': 'sunshie' }``` |
| `attributes` | yes | `dict` | The key values patch/set on the record | ```{ 'rank': 23 }``` |

#### :orange_book: Limitations
- Cannot allow setting parameters for `ReturnValues`, `ReturnConsumedCapacity`, `ReturnItemCollectionMetrics`


### delete(table_name, key)

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.delete_item)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name of the table to delete the item from | `'users'` |
| `key` | yes | `str`\|`dict` | The key (primary key) of the item to delete. If a string is passed it is associated with `id` by default. If an object is passed the first key and value are used to find the item | `22` or ```{ 'username': 'sunshie' }``` |

#### :orange_book: Limitations
- Cannot allow setting parameters for `ReturnValues`, `ReturnConsumedCapacity`, `ReturnItemCollectionMetrics`


### query(table_name, conditions)

[See boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `table_name`  | yes  | `str` | The name of the table to execute the query on | `'users'` |
| `conditions ` | yes | `dynamof.conditions.Condition` | This value should be built using the `dynamof.conditions` module. See the docs on that module. | `attr('username').equals('sunshie')` will build a proper Condition to pass. |

#### :orange_book: Limitations
- Cannot do pagination
- Cannot set limits
- Cannot query indexes
- Cannot allow setting parameters for `ReturnValues`, `ReturnConsumedCapacity`, `ReturnItemCollectionMetrics`


## Conditions

The `dynamof.conditions` module provides utility methods that make it simple to generate the complex data object boto3 needs when specifying conditions for querying, scanning, and other operations. Looking at the [docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query) for the query function you'll see `KeyConditionExpression`. This is the parameter this module was created to build.

**Example**

```py
from dynamof.conditions import attr

cond = attr('username').equals('sunshie')

cond.expression
# 'username = :username'

cond.attr_values
# { ":username": { "S": "sunshie" } }

```



### attr(name)

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `name`  | yes  | `str` | The name of the attribute to begin using on a condition. Could be a column you want to match exactly or if its a number type then it could be a column you want to check for `>` or `<` on | `'username'` |


The `attr` function returns a `dynamof.conditions.Attribute` that contains three methods

* `equals(value)`
* `greater_than(value)`
* `less_than(value)`

Where value is always the value to use in the conditional comparison you build.

### cand(*conditions)

Takes any number of condition expressions and combines them using the _and_ rule.

| Parameter  | Required | Data Type | Description | Example |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `conditions`  | yes  | `*dynamof.conditions.Condition` | Takes any number of `Condition` instances  | `cand(attr('points').less_than(50)` |



## Roadmap

- :white_check_mark: only use client & kill resource
- :white_check_mark: testing
- :white_check_mark: linter
- :white_check_mark: implement query
- :white_check_mark: implement response object & destructure response Item tree
- :white_check_mark: handle errors
- :white_check_mark: documentation
 setup travis
 move builder to `core` module
- :checkered_flag: `version 1.0.0`
- implement scan
- query support pagination
- query support indexes
- support projection expressions
- support filter expressions   
- :checkered_flag: `version 1.2.0`
- batch operations
- metadata operations
- update table operation
- ...
- :checkered_flag: `version 2.0.0`
