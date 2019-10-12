import pytest
from functools import partial

from boto3 import client
from botocore.config import Config

from dynamof.executor import execute


URL = 'http://localstack:4569'

client = client('dynamodb', endpoint_url=URL, config=Config(retries={
    'max_attempts': 2
}))

db_func = partial(execute, client)

@pytest.fixture
def db():
    return db_func
