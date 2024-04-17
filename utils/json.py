import json


def open_task(filepath):
    with open(filepath, 'r') as f:
        task = json.load(f)

    if not task:
        raise Exception("No task provided. Please include a task.json file in the root directory.")

    return task