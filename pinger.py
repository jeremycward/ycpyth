import requests

import time
import os
import random

hostname = format(os.getenv("REDIS_HOST", "daphne174"))
firstInt = 144893
ids = [str(x) for x in range(firstInt, firstInt+20)]
stati = ['pending', 'accepted', 'rejected', 'closed']


def do_ping():
    r = requests.get("http://{}:5000/hello?id={}&status={}".format(hostname, random.choice(ids), random.choice(stati)))
    print(r.status_code)


while 1:
    time.sleep(1)
    do_ping()
