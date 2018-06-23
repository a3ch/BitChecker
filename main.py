import requests
import time
from pathlib import Path
from funcs import db_create, db_insert, db_select

timeToSleep = 30 # In seconds

if not Path("base.db").is_file():
    db_create("base")

try:
    while True:
        req = requests.get("https://api.coinmarketcap.com/v2/ticker/?limit=20&sort=rank")
        json = req.json()

        listkeys = json["data"].keys()
        for id in listkeys:
            data = [json["data"][id]["name"], json["data"]
                    [id]["quotes"]["USD"]["price"]]
            db_insert(data)
        
        print("Running.")
        time.sleep(timeToSleep)
except KeyboardInterrupt:
    print("Terminated")