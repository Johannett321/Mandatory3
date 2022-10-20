import json
import os
import shutil

from packages.tools import debug_mode

business_name = ""


def load_business_from_storage(name_of_business):
    global business_name
    business_name = name_of_business

    from packages.business import Business

    if debug_mode:
        print("Attempting to load business from: " + business_name + os.sep + "SaveFile.json")
    saved_data = load_string_from_file("SaveFile.json")
    if saved_data is not None:
        json_converted = json.loads(saved_data)
        business = Business(json_converted["name"], int(json_converted["balance"]))
        for element in json_converted["products"]:
            business.add_product_from_json(json_converted["products"][element])
        return business
    else:
        print("Failed to load business")
        return False


def create_business(name_of_business):
    global business_name
    business_name = name_of_business

    # create business directory
    os.mkdir(name_of_business)

    # add business to businessList
    try:
        if os.path.exists("businesses.csv") is False:
            open("businesses.csv", "w+").close()

        with open("businesses.csv", "r+") as f:
            file_content = f.read()
            if file_content != "":
                file_content += ", "
            file_content += business_name
            f.seek(0)
            f.write(file_content)
            f.truncate()
    except ValueError:
        print("Error: Could not save business")
        return


def business_exists(name_of_business):
    return os.path.exists(name_of_business + "/SaveFile.json")


def delete_business(business_to_delete):
    # remove directory
    shutil.rmtree(business_to_delete)

    # remove from businesses CSV
    try:
        with open("businesses.csv", "r+") as f:
            file_content = f.read()

            file_content = file_content.replace(", " + business_to_delete, "")
            file_content = file_content.replace(business_to_delete + ", ", "")
            file_content = file_content.replace(business_to_delete, "")

            f.seek(0)
            f.write(file_content)
            f.truncate()
    except FileNotFoundError:
        print("File not found")
    finally:
        try:
            f.close()
        except UnboundLocalError:
            return False

    print("Business was deleted!")
    return True


def load_string_from_file(filepath):
    global business_name
    try:
        with open(business_name + os.sep + filepath, "r") as f:
            return f.read()
    except:
        return None
    finally:
        try:
            f.close()
        except UnboundLocalError:
            return


def write_string_to_file(filepath, content):
    global business_name

    if debug_mode:
        print("Attemting to write to file: " + business_name + os.sep + filepath + ". Content: " + content)
    try:
        with open(business_name + os.sep + filepath, "w") as f:
            f.write(content)
            return True
    except:
        print("Could not save to file")
        return False
    finally:
        try:
            f.close()
        except UnboundLocalError:
            return False