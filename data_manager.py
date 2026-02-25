import json


def save_to_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)


def load_from_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)
