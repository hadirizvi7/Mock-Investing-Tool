from time import strftime
import requests
import datetime
from datetime import datetime, timedelta
from yahoo_fin import stock_info as si
import pandas as pd 
import numpy as np 
from excel_info import findColumns
from update_sheet import updateColumns

SYMBOL_RANGE = 'A2:A50'
AMOUNT_RANGE = 'B2:B50'

def callAPI():
    symbol_list = findColumns(SYMBOL_RANGE)

    if not symbol_list:
        print("No data found for stock tickers.")
        return
    
    market_price_list = []
    for ticker in symbol_list[0]:
        livePrice = si.get_live_price(ticker)
        market_price_list.append(livePrice)
    
    amount_list = findColumns(AMOUNT_RANGE)

    if not amount_list:
        print("No data found for amount invested.")
        return

    amount_invested_list = []
    for amount in amount_list[0]:
        amount_invested_list.append(amount)
    
    return (market_price_list, amount_invested_list)
        
if __name__ == '__main__':
    price_list, invested_list = callAPI()
    updateColumns(price_list, invested_list)