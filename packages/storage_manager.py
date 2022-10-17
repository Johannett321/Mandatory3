import json


def load_business_from_storage():
    from packages.business import Business
    saved_data = load_string_from_file("SaveFile.json")
    if saved_data is not None:
        json_converted = json.loads(saved_data)
        business = Business(json_converted["name"], int(json_converted["balance"]))
        for element in json_converted["products"]:
            business.add_product_from_json(json_converted["products"][element])
        return business
    else:
        return False


def load_string_from_file(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except:
        return None
    finally:
        try:
            f.close()
        except UnboundLocalError:
            return


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
