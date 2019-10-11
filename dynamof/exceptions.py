


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
    def maps_to(cls, err):
        key = 'Cannot create preexisting table'
        return key in str(err)

class DatabaseFindException(DynamofException):
    def __init__(self):
        message = "Could not find entity"
        super().__init__(message)

class UnknownException(DynamofException):
    def __init__(self):
        message = "Unknown error occured while communicating with dynamo"
        super().__init__(message)
