from __future__ import print_function

import os.path
from tkinter.tix import COLUMN

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pygsheets
import pandas as pd
import datetime
from datetime import datetime, timedelta
from excel_info import findColumns
from yahoo_fin import stock_info as si
import decimal

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1CWZWHVS9yfGvuP0_rT9LJkcqQoTrV4CjS8D0hX7t2k8'
COL_RANGE = 'C2:C10'

def calculateShares(price_list, invested_list):
    N = len(price_list)

    output = []
    for i in range(N):
        shares = float(invested_list[i]) / float(price_list[i])
        output.append(shares)
    
    return output

def calculateCurrentPrice(price_list, shares_list):
    output = []
    N = len(shares_list)
    runningSum = 0

    print(price_list)
    print(shares_list)

    for i in range(N):
        currentPrice = price_list[i]
        market_value = currentPrice * float(shares_list[i])
        #print((currentPrice, shares_list[i], market_value))
        output.append(market_value)
        runningSum += market_value

    output.append('SUM = {}'.format(runningSum))
    return output

def findNextCol():
    col_num = 4
    num = 68
    col_string = '{}2:{}50'.format(chr(num), chr(num))

    while findColumns(col_string) != []:
        num += 1
        col_num += 1
        col_string = '{}2:{}50'.format(chr(num), chr(num))

    return col_num


def updateColumns(price_list, invested_list):

    df = pd.DataFrame()
    gc = pygsheets.authorize(service_file = 'tokens/creds.json')
    DATE = (datetime.today()).strftime('%Y-%m-%d')
    sh = gc.open('Mock Investing Tool')
    wks = sh[0]
    shares_list = findColumns('C2:C50')

    if shares_list == []:
        print("Calculating # of Shares...")
        shares_list.append(calculateShares(price_list, invested_list))
        df["# of Shares"] = shares_list[0]
        wks.set_dataframe(df, (1, 3))
    
    elif len(shares_list[0]) != len(invested_list):
        for x in range(len(shares_list[0]), len(invested_list)):
            shares_list[0].append(float(invested_list[x]) / float(price_list[x]))
        
        print("Adding new Shares...")
        df["# of Shares"] = shares_list[0]
        wks.set_dataframe(df, (1, 3))
    
    df = pd.DataFrame()
    print(type(shares_list[0]))
    df[DATE] = calculateCurrentPrice(price_list, shares_list[0])
    next_col = findNextCol()
    wks.set_dataframe(df, (1, next_col))