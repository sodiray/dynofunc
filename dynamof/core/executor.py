import json

def execute(client, operation, debug=False):
    runner = operation.runner
    description = operation.description
    if debug is True:
        print(f'############\n{operation.name}\n############')
        print(json.dumps(description, indent=2))
    return runner(client, description)
