import pytest
import orjson
from yc.Curve import curve_repo
import datetime

@pytest.fixture()
def yc():
    return curve_repo["EUR-OUTRIGHT"]


def test_request_example(yc):
    assert len(yc.plot.x) == 1080
    assert len(yc.plot.y)
    dumped = orjson.dumps(yc)
    assert len(dumped) > 100

