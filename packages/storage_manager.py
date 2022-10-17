import json


def load_business_from_storage():
    from packages.business import Business
    saved_data = load_string_from_file("SaveFile.json")
    if saved_data is not None:
        json_converted = json.loads(saved_data)
        return Business(json_converted["name"], int(json_converted["balance"]))
    else:
        return False


def load_string_from_file(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except:
        return None
    finally:
        f.close()


def write_string_to_file(filepath, content):
    print("Attemting to write to file: " + filepath + ". Content: " + content)
    try:
        with open(filepath, "w") as f:
            f.write(content)
            return True
    except:
        print("Could not save to file")
        return False
    finally:
        f.close()
