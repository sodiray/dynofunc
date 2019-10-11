


class DynamofError(Exception):
   def __init__(self, message):
       super().__init__(message)
   def info(self, add_message):
       """ Adds details to the base error message"""
       self.message = f'{self.message}; {add_message}'
       return self

class DatabaseFindError(DynamofError):
    def __init__(self):
        message = "Could not find entity"
        super().__init__(message)

class UnknownError(DynamofError):
    def __init__(self):
        message = "Unknown error occured while communicating with dynamo"
        super().__init__(message)
