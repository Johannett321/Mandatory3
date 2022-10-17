from packages.warehouse import *
from packages.storage_manager import *
from packages.business import *

def readCmd():
    command = input("Command: ")
    command_parts = command.split(" ")
    if command_parts[0] == "product":
        if command_parts[1] == "add":
            print("Added product")

    readCmd()

def run_setup():
    print("Running setup")
    businessName = input("Name of business: ")
    initialBalance = input("Initial balance (money): ")
    business = Business(businessName, initialBalance)
    save_business(business)

if load_data() is False:
    print("No data could be found")
    run_setup()
    exit(0)

readCmd()