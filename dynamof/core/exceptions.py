
class DynamofException(Exception):
   def __init__(self, message):
       self.message = message
       super().__init__(message)
   def info(self, add_message):
       """ Adds details to the base error message"""
       self.message = f'{self.message}; {add_message}'
       return self

class PreexistingTableException(DynamofException):
    def __init__(self):
        message = "Attempted to create a table that already exists"
        super().__init__(message)
    @classmethod
    def matches(cls, err):
        message, _ = parse(err)
        key = 'Cannot create preexisting table'
        return message == key

class TableDoesNotExistException(DynamofException):
    def __init__(self):
        message = "Attempted to do operation on a table that does not exist"
        super().__init__(message)
    @classmethod
    def matches(cls, err):
        message, _ = parse(err)
        key = 'Cannot do operations on a non-existent table'
        return message == key

class ConditionNotMetException(DynamofException):
    def __init__(self):
        message = "Could not find an item that satisifed the given conditions"
        super().__init__(message)
    @classmethod
    def matches(cls, err):
        _, code = parse(err)
        return code == 'ConditionalCheckFailedException'

class BadGatewayException(DynamofException):
    def __init__(self):
        message = "Issue communicating with dynamo"
        super().__init__(message)
    @classmethod
    def matches(cls, err):
        message, _ = parse(err)
        return message == 'Bad Gateway'

class UnknownDatabaseException(DynamofException):
    def __init__(self):
        message = "An unkonwn exception occured when executing request to dynamo"
        super().__init__(message)

def factory(boto_client_err):
    if BadGatewayException.matches(boto_client_err):
        return BadGatewayException()
    if TableDoesNotExistException.matches(boto_client_err):
        return TableDoesNotExistException()
    if ConditionNotMetException.matches(boto_client_err):
        return ConditionNotMetException()
    if PreexistingTableException.matches(boto_client_err):
        return PreexistingTableException()
    return UnknownDatabaseException()

def parse(exc):
    """Takes in an exception and returns the boto
    `Message, Code` properties if they exist - else `None, None`
    """
    if exc is not None and hasattr(exc, 'response') and exc.response is not None:
      error = exc.response.get('Error', {})
      code = error.get('Code', None)
      message = error.get('Message', None)
      return message, code
    return None, None
