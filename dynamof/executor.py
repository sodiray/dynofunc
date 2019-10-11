

def execute(client, operation):
    runner = operation.runner
    description = operation.description
    return runner(client, description)
