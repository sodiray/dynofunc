import json
import logging

from botocore.exceptions import ClientError

from dynofunc.core.exceptions import factory


logger = logging.getLogger('dynofunc')

def execute(client, operation):

    runner = operation.runner
    description = operation.description

    logger.debug('Executing Operation:')
    logger.debug(json.dumps(description, indent=2))

    try:
        return runner(client, description)
    except ClientError as err:
        raise factory(err)
