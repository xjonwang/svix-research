from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', port=7496, clientId=1)

btc = Crypto(symbol='BTC', exchange='PAXOS', currency='USD')
bars = ib.reqHistoricalData(contract=btc, endDateTime='', durationStr='30 D', barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

print(bars)
# ib.qualifyContracts(svix)

print(btc)