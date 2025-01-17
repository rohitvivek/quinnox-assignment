import json


def load_config(filename="config.json"):
    with open(filename, "r") as f:
        config_data = json.load(f)
    return config_data
