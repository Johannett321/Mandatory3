from packages import storage_manager
from packages.business import Business
from packages.storage_manager import load_business_from_storage, business_exists
from packages.tools import clear_console, press_enter_to_continue, maybe_exit


def get_business_from_menu():
    clear_console()
    global business

    print("WELCOME TO BWMS (Business Warehouse Management System)")
    print("1) Create a new business")
    if list_businesses() is not None:
        print("2) Open existing business")
        print("3) Delete business")
    print("x) Exit")
    chosen_option = input("Please choose an option: ").lower()

    if chosen_option == "x":
        maybe_exit()
        return get_business_from_menu()
    if chosen_option == "1":  # create a new business
        create_a_business()
        return get_business_from_menu()
    elif chosen_option == "2":  # open existing business
        clear_console()
        print("Please type the name of the business you would like to open")
        print()
        print("Available businesses:")
        print(list_businesses())
        print()
        print("Type 'x' to cancel")
        name_of_business = input("Name of business: ")
        if name_of_business.lower() == "x":
            return get_business_from_menu()
        business = load_business_from_storage(name_of_business)
        if business is False:
            press_enter_to_continue()
            return get_business_from_menu()
        return business
    elif chosen_option == "3":
        clear_console()
        print("------------------- DELETE BUSINESS -------------------")
        print(list_businesses())
        print("Type 'x' to cancel")
        delete_business = input("Name of business you would like to delete: ")
        clear_console()
        if delete_business.lower() == "x":
            return get_business_from_menu()
        print("WARNING! THIS WILL DELETE ALL INFORMATION ABOUT THIS BUSINESS, AND ALL PRODUCTS LINKED TO THIS BUSINESS!")
        print("Business to delete: " + delete_business)
        sure = input("Are you sure? Deleting a business cannot be undone! (y/n): ").lower()
        if sure == "y":  # delete business
            storage_manager.delete_business(delete_business)
            press_enter_to_continue()
    else:
        print("'" + chosen_option + "' is not an option")
        press_enter_to_continue()

    return get_business_from_menu()


def create_a_business():
    global business_name
    global business

    clear_console()
    print("------------------- CREATE BUSINESS -------------------")

    print("Type 'x' to cancel")
    business_name = input("Name of business: ")

    # let the user exit
    if business_name == "x":
        return

    # don't let the user use ',' in business name. This will break CSV file
    if "," in business_name:
        print("',' is not allowed in business name")
        press_enter_to_continue()
        create_a_business()
        return

    if business_name == "":
        print("The business must have a name!")
        press_enter_to_continue()
        create_a_business()
        return

    # make sure business not already exists
    if business_exists(business_name):
        print("Business already exists!")
        press_enter_to_continue()
        create_a_business()
        return

    initial_balance = input("Initial balance: ")
    try:
        if int(initial_balance) < 0:
            print("Initial balance cannot be a negative number")
            press_enter_to_continue()
            create_a_business()
            return
    except ValueError:
        print("Initial balance must be a number")
        press_enter_to_continue()
        create_a_business()
        return

    business = Business(business_name, int(initial_balance))
    storage_manager.create_business(business_name)
    storage_manager.business_name = business_name
    business.save()
    print("Business created!")
    press_enter_to_continue()


def list_businesses():
    try:
        with open("businesses.csv") as f:
            businesses = f.read()
            businesses.replace(", ", "\n")
            return businesses
    except FileNotFoundError:
        return False
    finally:
        try:
            f.close()
        except UnboundLocalError:
            return