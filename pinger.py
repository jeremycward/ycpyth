import requests

import time
import os

hostname=format(os.getenv("REDIS_HOST","daphne174"))
def do_ping():
    r = requests.get("http://{}:5000/hello".format(hostname))
    print(r.status_code)



while 1:
    time.sleep(5)
    do_ping()



