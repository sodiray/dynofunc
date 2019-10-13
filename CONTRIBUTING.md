# How to contribute

I'm really glad you're reading this, because we need volunteer developers to help this project reach its full potential.

Here are some important resources:

  * [DynamoDB Guide](https://www.dynamodbguide.com/what-is-dynamo-db/)
  * [Boto3 Dynamo Client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html)

## Testing & Linting

There are `unit` and `integration` tests in the project.

* `unit` tests can be run with `make test`. If you haven't already, create a virtual env and activate it before running the tests. 100% coverage is required.

* `integration` tests are run through docker. a `localstack` is spun up and actual tables are created and interacted with. Run `docker-compose up` at the command line. _NOTE:_ errors will show up from the `localstack` service but that's expected because some of our testing is on how to handle error. Just ensure the `integration_tests` service ends with all passing tests.

* `lint` can be run by `make lint`
