import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
import datetime as dt
import numpy as np
import pandas as pd
import math
from scipy.stats import gaussian_kde
from scipy.integrate import quad
import matplotlib.pyplot as plt
    
g_vix = pdr.get_data_yahoo(['^VIX'], dt.date(2000, 1, 1), dt.date.today())['Adj Close']

def query_option_chain(ticker: str) -> tuple:
    security = yf.Ticker(ticker)
    expiries = security.options
    option_chain = security.option_chain(date=expiries[0])
    return (option_chain.calls, option_chain.puts)

# creates PDF from KDE given samples
def generate_kde(data, show_plot=False):
    min_return = data.min()
    max_return = data.max()
    kde = gaussian_kde(data.dropna())
    xrange = np.linspace(min_return, max_return, data.size - 1)
    if show_plot:
        plt.plot(xrange, kde(xrange), color='k', label='KDE')
        plt.show()
    return kde

# creates profit function given distribution
def pdf_creator(kde: gaussian_kde, strike: float, spot: float):
    def pdf(x):
        return kde.evaluate(x) * max(0, spot * math.exp(x) - strike)
    return pdf

# buckets data by spot vix level
def vix_parametrize(data):
    start_date = data.index[0]
    vix = g_vix[start_date:]
    min_vix = int(vix.min() // 8)
    max_vix = int(vix.max() // 8 + 1)
    vix_parametrized_returns = [[] for _ in range(max_vix - min_vix)]
    for i in range(1, data.size):
        vix_parametrized_returns[int(vix[i] // 8) - min_vix].append(data[i])
    return vix_parametrized_returns

if __name__ == "__main__":
    svix = pdr.get_data_yahoo(['SVIX'], dt.date(2022, 3, 30), dt.date.today())['Adj Close']
    svix_daily_returns = np.log(svix/svix.shift(1))
    svxy = pdr.get_data_yahoo(['SVXY'], dt.date(2000, 1, 1), dt.date.today())['Adj Close']
    svxy_daily_returns = np.log(svxy/svxy.shift(1))
    generate_kde(svix_daily_returns, True)
    svix_vix_parametrized_returns = vix_parametrize(svix_daily_returns)
    svxy_kde = generate_kde(svxy_daily_returns)
    svxy_vix_parametrized_returns = vix_parametrize(svxy_daily_returns)
    svxy_kdes = []
    for group in svxy_vix_parametrized_returns:
        if (len(group) > 30):
            svxy_kdes.append(generate_kde(pd.Series(group)))
    svxy_pdf = pdf_creator(svxy_kdes[1], 79, 80.07)
    result, error = quad(svxy_pdf, -2, 2)
    print(result, error)