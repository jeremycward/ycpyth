import QuantLib as ql
import datetime
import numpy as np
import math
from dataclasses import dataclass
import matplotlib
import matplotlib.pyplot as plt

import orjson
from yc.plot_utils import all_tenors_and_rates, tenor_to_period


@dataclass()
class Plot:
    x: list[datetime.date]
    y: list[float]


@dataclass()
class Point:
    tenor: str
    value: float
    maturityDate: datetime.date


@dataclass
class Handle:
    name: str
    description: str


@dataclass
class Instrument:
    name: str
    points: list[Point]


@dataclass
class MarketData:
    instruments: list[Instrument]


@dataclass
class YieldCurve:
    handle: Handle
    mktData: MarketData
    plot: Plot


def makeRandomInstrument(base_rate, maturities, drift, volatility, name):
    rates = [base_rate + np.random.normal(drift * n, volatility * math.sqrt(n)) for n in range(len(maturities) + 1)]
    points = []
    for x, y in zip(maturities, rates):
        tenor = "{}".format(x)
        qlTenorDate = ql.Date.todaysDate() + tenor_to_period(tenor)
        newPoint = Point(tenor=tenor, value=y,
                         maturityDate=datetime.date(qlTenorDate.year(), qlTenorDate.month(), qlTenorDate.dayOfMonth()))
        points.append(newPoint)
    instr = Instrument(name=name, points=points)
    return instr


def makeStochasticCurve(name, description, depo_base_rate, bond_base_rate):


    volatility = 0.01
    drift = 0.01
    depo_maturities = [tenor_to_period(x) for x in ["1D", "1W", "2W", "1M", "2M", "3M", "6M"]]
    depo_rates_instrument = makeRandomInstrument(depo_base_rate,
                                             depo_maturities, drift,
                                             volatility,
                                             "{}_{}".format(name,
                                                            "depo_rate"))
    bond_maturities = [tenor_to_period(x) for x in ["1Y", "2Y", "3Y", "5Y", "10Y", "30Y"]]
    bond_rates_instrument = makeRandomInstrument(bond_base_rate, bond_maturities, drift, volatility,
                                             "{}_{}".format(name, "bond_rate"))

    instruments = [depo_rates_instrument, bond_rates_instrument]

    handle = Handle(name=name, description=description)
    mktData = MarketData(instruments=instruments)

    (tenors, rates) = (all_tenors_and_rates(mktData))

    ql_today = ql.Date.todaysDate()
    ql_dates = [ql_today + tenor_to_period(tnr) for tnr in tenors]

    yield_curve = ql.MonotonicCubicZeroCurve([ql_today] + ql_dates, [0] + rates,
                                         ql.Actual360(),
                                         ql.Brazil(),
                                         ql.MonotonicCubic(),
                                         ql.Continuous)
    yield_curve.allowsExtrapolation()

    dates = [ql_today + ql.Period(i, ql.Days) for i in range((360 * 3))]
    rates = [yield_curve.zeroRate(dt, ql.Actual360(), ql.Continuous).rate() for dt in dates]
    x = []
    y = []
    for z in list(zip(dates, rates)):
        x.append(datetime.date(z[0].year(), z[0].month(), z[0].dayOfMonth()))
        y.append(z[1])
    plot = Plot(x=x, y=y)

    return YieldCurve(handle=handle,
                  mktData=mktData, plot=plot)

curve_repo = {
    "EUR-OUTRIGHT": makeStochasticCurve("EUR-OUTRIGHT", "Eur Vanilla Outright Curve", 1.0023, 1.445),
    "USD-OUTRIGHT": makeStochasticCurve("USD-FED-OUTRIGHT", "Fed Outright Curve", 3.0023, 4.19),

}

# print(str(orjson.dumps(curve_repo["EUR-OUTRIGHT"])))
