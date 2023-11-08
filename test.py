import numpy as np
from scipy.ndimage import gaussian_filter1d

from ThetaDataClient import Security, Right, Req
from WrapperClient import WrapperClient
from breeden_litzenberger import pdf_from_IV, plot_pdf_and_prices, plot_vols
from black_scholes import bs_iv_bulk

if __name__ == "__main__":
    wrapper_client = WrapperClient()
    dates, strikes, options = wrapper_client.get_chains_over_time(root="SPY", exp=20230406, right=Right.CALL, points=["open"])
    underlying = wrapper_client.get_underlying_over_time(root="SPY", security_type=Security.EQUITY, points=["open"], dates=dates)
    print(dates)
    num_days = len(dates)
    strikes = np.array(strikes, dtype='float64')
    strikes /= 1000
    print(options["open"])
    for i in range(num_days):
        spot = underlying["open"][i]
        iv = bs_iv_bulk(prices=options["open"][i], strikes=strikes, S=spot, t=(num_days-1-i)/252)
        plot_vols(strikes, iv, spot)
        iv = gaussian_filter1d(iv, 3)
        plot_vols(strikes, iv, spot)
        Krange, pdf, prices = pdf_from_IV(strikes=strikes, vols=iv, S=spot, t=(num_days-1-i)/252, r=0)
        plot_pdf_and_prices(Krange=Krange, prices=prices, pdf=pdf, S=spot)
