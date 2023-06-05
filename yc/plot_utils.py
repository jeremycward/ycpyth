from datetime import datetime
import math
import numpy as np
import pandas as pd
import QuantLib as ql
import matplotlib
import matplotlib.pyplot as plt

tenor_period_dict = {
    "D" : ql.Days,
    "W": ql.Weeks,
    "M": ql.Months,
    "Y": ql.Years
}


def all_tenors_and_rates(mkt_data):
    all_tenors = []
    all_rates = []
    for instrument in mkt_data.instruments:
        all_tenors += [point.tenor for point in instrument.points]
        all_rates += [point.value for point in instrument.points]
    return (all_tenors, all_rates)



def tenor_to_period(tenor):
    amount = tenor[0:len(tenor) - 1]
    period = tenor[-1]
    return ql.Period(int(amount), tenor_period_dict[period])
