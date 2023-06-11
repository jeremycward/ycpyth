from flask import Flask, request
from flask_sse import sse
import schedule

app = Flask(__name__)

app.config["REDIS_URL"] = "redis://daphne174"
app.run()


def ping():
    sse.publish({"message": "Hello!"}, type='greeting')
    print("sent message")


schedule.every(1).seconds.do(ping)


if __name__ == "__main__":
    while True:
        schedule.run_pending()


