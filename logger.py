# This file is for logging trades, profit and etc.
# Each trade will be added to a log file.
from datetime import datetime
import json, os

from ta import momentum

def addOrder(order):
    parsed_order = parseOrder(order)
    log_path = f"LogFiles/{datetime.today().strftime('%Y-%m-%d')}.json"
    
    # Check if log file already exists
    if os.path.isfile(log_path):
        with open(log_path, "r+") as log_file:
            file = json.load(log_file)
            file["Orders"].append(parsed_order)
            log_file.seek(0)
            json.dump(file, log_file, indent = 4)
    else:
        with open(log_path, "w") as log_file:
            data = {"Orders": [parsed_order]}
            json.dump(data, log_file, indent = 4)


def parseOrder(order):
    
    # datetime = order['datetime']
    # side = order["side"]
    # price = order["price"]
    # amount = order["amount"]
    # fee = order["fee"]["cost"]
    # feeCurrency = order["fee"]["currency"]

    parsed = {
        "Time of order": "datetime",
        "Type of order": "side",
        "Price of asset": "price",
        "Amount traded": "amount",
        "Fees paid": "fee + feeCurrency",
    }
    
    return parsed