import pandas as pd
import numpy as np
import pandas_market_calendars as mcal
import yfinance as yf
import pandas_datareader as pdr
yf.pdr_override()
import datetime as dt
import bisect

# https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-vix-futures-indices.pdf
# rebalancing methodology

vix_futures_expiries = [dt.date(2023, 10, 18), dt.date(2023, 11, 15), dt.date(2023, 12, 20)]

def count_trading_days(start, end, market='CBOE_Futures'):
    calendar = mcal.get_calendar(market)
    trading_days = calendar.valid_days(start_date=start, end_date=end)
    return len(trading_days)

def get_contracts(date):
    idx = bisect.bisect_right(vix_futures_expiries, date)
    return (vix_futures_expiries[idx-1], vix_futures_expiries[idx], vix_futures_expiries[idx+1])

def roll_yield(date: dt.date, prev_month: dt.date, front_month: dt.date, second_month: dt.date):
    crw_front = (count_trading_days(date, front_month) - 2) / (count_trading_days(prev_month, front_month) - 1)
    front_month_price = 21
    second_month_price = 21.05


def collateral_yield(benchmark_rate: float, duration: float):
    return np.log((1 + benchmark_rate) ** (duration / 365))

if __name__ == '__main__':
    print(count_trading_days(dt.date(2023, 3, 3), dt.date(2023, 3, 3)))
    print(get_contracts(dt.date(2023, 11, 13)))
    print(collateral_yield(0.0531, 5))