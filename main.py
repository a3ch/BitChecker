import requests
import time
from pathlib import Path
from funcs import db_create, db_insert, db_select, db_update

timeToSleep = 30  # In seconds

if not Path("base.db").is_file():
    db_create("base")
    db_create("base_reg", False)

try:
    while True:

        apilink = "https://api.coinmarketcap.com/v2/ticker/?limit=20&sort=rank"
        req = requests.get(apilink)
        json = req.json()

        listkeys = json["data"].keys()
        for id in listkeys:
            data = [id, json["data"][id]["name"], json["data"]
                    [id]["quotes"]["USD"]["price"]]

            res = str(db_select("id", id))
            if res in data:
                db_update(data[2], id)
            else:
                db_insert(data)

            db_insert(data[0::2], False)

        print("Running.")
        time.sleep(timeToSleep)
except KeyboardInterrupt:
    print("\nTerminated")
