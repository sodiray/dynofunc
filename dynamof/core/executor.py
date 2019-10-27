import json

from botocore.exceptions import ClientError

from dynamof.core.exceptions import factory


def execute(client, operation):

    runner = operation.runner
    description = operation.description

    print(f'############\n  CALLING  \n############')
    print(json.dumps(description, indent=2))

    try:
        return runner(client, description)
    except ClientError as err:
        raise factory(err)
