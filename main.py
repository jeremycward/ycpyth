from flask import Flask, request, render_template
import orjson
from flask_cors import CORS
from yc.Curve import curve_repo
from flask_sse import sse
import schedule


def ping():
    sse.publish({"message": "Hello!"}, type='greeting')
    print("sent message")


schedule.every(1).seconds.do(ping)


class Main:
    app = Flask(__name__, template_folder='C:\\Users\\jerem\\PycharmProjects\\pythonProject\\yc\\templates')
    CORS(app, support_credentials=True)
    app.config["REDIS_URL"] = "redis://daphne174"
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
            sse.publish({"message": "Hello!"}, type='greeting')
            return "Message sent!"

        @self.app.route('/')
        def index():
            return render_template("index.html")


if __name__ == "__main__":
    main = Main()
    main.app.run(debug=True)
else:
    if __name__ == '__main__':
        app = Main().app
