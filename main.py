import requests
import sched
import time
from datetime import datetime, timedelta
from funcs import db_create, db_insert, db_select

db_create("base")

scheduler = sched.scheduler(timefunc=time.time)

# Zera os segundos de agora e some mais 2 minuto
def reschedule():
    target = datetime.now().replace(second=0, microsecond=0)
    #Delay de 2 minutos
    target += timedelta(minutes=2)

    # Printa a hora programada
    print(target)

    scheduler.enterabs(target.timestamp(), priority=0, action=reGet)

def reGet():
    req = requests.get("https://api.coinmarketcap.com/v2/ticker/?limit=20&sort=rank")
    json = req.json()

    #Pega os IDs de cada cryptomoeda
    listkeys = json["data"].keys()
    for id in listkeys:
        data = [json["data"][id]["name"],json["data"][id]["quotes"]["USD"]["price"]]
        db_insert(data)


    reschedule()

reschedule()

try:
    scheduler.run(blocking=True)
except KeyboardInterrupt:
    print("\nParei")
