import datetime

from flask import Flask, request, render_template
import orjson
from flask_cors import CORS
from yc.Curve import curve_repo
from flask_sse import sse

import os
from datetime import datetime




class Main:
    app = Flask(__name__, template_folder=os.environ["TEMPLATE_DIR"])
    CORS(app, support_credentials=True)
    app.config["REDIS_URL"] = "redis://{}".format(os.environ["REDIS_HOST"])
    app.register_blueprint(sse, url_prefix='/stream')

    def __init__(self):
        @self.app.route('/ycHandles', methods=['GET'])
        def yc_handles():
            handles = [value.handle for key, value in curve_repo.items()]
            handles_dict = {
                "handles": handles
            }
            return orjson.dumps(handles_dict)

        @self.app.route("/yc")
        def yc_points():
            name = request.args.get("ycName")
            return orjson.dumps(curve_repo.get(name))

        @self.app.route("/hello")
        def publish_hello():
            now = datetime.now()
            timeMsg = now.strftime("%H:%M:%S")
            sse.publish({"message": "Hello!  time is now {}".format(timeMsg)}, type='greeting')
            return "Message sent!"

        @self.app.route('/')
        def index():
            return render_template("index.html")


if __name__ == "__main__":
    main = Main()
    main.app.run(debug=True)
else:
    app = Main().app
