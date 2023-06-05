from flask import Flask, request
import orjson
from flask_cors import CORS
from yc.Curve import curve_repo


class Main:
    app = Flask(__name__)
    CORS(app, support_credentials=True)

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


if __name__ == "__main__":
    main = Main()
    main.app.run(debug=True)
