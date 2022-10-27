# Import required libraries/dependencies
from time import strftime
import requests
import datetime
from datetime import datetime, timedelta
from yahoo_fin import stock_info as si
import pandas as pd 
import numpy as np 
from excel_info import findColumns
from update_sheet import updateColumns
import time

# Specify column ranges for tickers
SYMBOL_RANGE = 'A2:A50'
# Specify column ranges for amount user wants to invest in corresponding stock/crypto
AMOUNT_RANGE = 'B2:B50'

def callAPI():
    # Calls excel_info script to read/store stock tickers
    symbol_list = findColumns(SYMBOL_RANGE)

    # Edge Case: No tickers found in Google Sheet
    if not symbol_list:
        print("No data found for stock tickers.")
        return ([], [])
    
    # Extract the current market price based on the ticker provided
    market_price_list = []
    for ticker in symbol_list[0]:
        # Call to the Yahoo Finance API
        livePrice = si.get_live_price(ticker)
        market_price_list.append(livePrice)
    
    amount_list = findColumns(AMOUNT_RANGE)
    
    # Edge Case: User did not provide investment amount
    if not amount_list:
        print("No data found for amount invested.")
        return ([], [])

    amount_invested_list = []
    for amount in amount_list[0]:
        amount_invested_list.append(amount)
    
    return (market_price_list, amount_invested_list)
        
if __name__ == '__main__':
    price_list, invested_list = callAPI()
    # Pass data retrieved from API calls to script responsible for updated the Google Sheet
    updateColumns(price_list, invested_list)
    # Sleep command to allow script to run once every 24 hours
    time.sleep(86400)