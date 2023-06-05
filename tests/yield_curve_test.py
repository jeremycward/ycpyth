import datetime

import pytest
import json
from main import Main
import orjson

m = Main()
tomorrow = datetime.date.today() + datetime.timedelta(days=1)

@pytest.fixture()
def app():
    m.app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield m.app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_request_example(client):
    response = client.get("/ycHandles")
    print(response.data)
    assert response.status_code == 200
    handle_json = json.loads(response.data)
    assert len(handle_json["handles"]) == 2
    assert handle_json["handles"][0]["description"] == "Eur Vanilla Outright Curve"
    assert handle_json["handles"][0]["name"] == "EUR-OUTRIGHT"


def test_get_single_curve(client):

    response = client.get("/yc?ycName=EUR-OUTRIGHT")
    assert response.status_code == 200

    yc_json = orjson.loads(response.data)

    assert yc_json["mktData"]["instruments"][0]["points"][0]["tenor"] == "1D"
    assert yc_json["mktData"]["instruments"][0]["points"][0]["value"] == 1.0023
    assert len(yc_json["mktData"]["instruments"]) == 2
    assert len(yc_json["mktData"]["instruments"][0]["points"]) > 0
    assert len(yc_json["plot"]["x"]) == 1080
    assert yc_json["mktData"]["instruments"][0]["points"][0]["maturityDate"] == tomorrow.strftime("%Y-%m-%d")

