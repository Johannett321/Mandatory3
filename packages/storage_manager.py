import json


def load_data():
    try:
        with open("saved_data.json") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return False

    data = json.loads(lines)
    return data


def get_wares():
    print("getting wares")


def save_business(business):
    print("Business saved");
