# Import required libraries/dependencies
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

# Insert the SpreadSheet ID of your Google Sheets Document
SPREADSHEET_ID = ''
# The column range responsible for storing the number of shares owned
COL_RANGE = 'C2:C50'

# Function to calculate the number of shares a user owns (based on how much the user chooses to invest)
def calculateShares(price_list, invested_list):
    N = len(price_list)

    output = []
    for i in range(N):
        shares = float(invested_list[i]) / float(price_list[i])
        output.append(shares)
    
    return output

# Function to calculate the current value of specified shares
def calculateCurrentPrice(price_list, shares_list):
    output = []
    N = len(shares_list)
    runningSum = 0

    for i in range(N):
        currentPrice = price_list[i]
        market_value = currentPrice * float(shares_list[i])
        output.append(market_value)
        runningSum += market_value
   
    # Total portfolio value is also included for the current day column
    output.append('SUM = {}'.format(runningSum))
    return output

# Function to find the next available column for inserting the current day portfolio value
def findNextCol():
    col_num = 4
    num = 68
    # Utilizes ASCII values to ensure proper syntax for column assignment
    col_string = '{}2:{}50'.format(chr(num), chr(num))

    # Iterate thru the columns using the function defined in 'excel_info.py'
    while findColumns(col_string) != []:
        num += 1
        col_num += 1
        col_string = '{}2:{}50'.format(chr(num), chr(num))

    return col_num


def updateColumns(price_list, invested_list):

    df = pd.DataFrame()
    # Credentialing required to make calls to Google Sheets API
    gc = pygsheets.authorize(service_file = 'sampleTokens/creds.json')
    DATE = (datetime.today()).strftime('%Y-%m-%d')
    sh = gc.open('Mock Investing Tool')
    wks = sh[0]
    # Determine if shares list is already present in Google Sheet
    shares_list = findColumns(COL_RANGE)

    # If the number of shares is not specified, calculate this info and insert it into the sheet
    if shares_list == []:
        print("Calculating # of Shares...")
        shares_list.append(calculateShares(price_list, invested_list))
        df["# of Shares"] = shares_list[0]
        wks.set_dataframe(df, (1, 3))
    
    # If the user has decided to add more stocks to invest in, calculate the shares for these new additions
    elif len(shares_list[0]) != len(invested_list):
        for x in range(len(shares_list[0]), len(invested_list)):
            shares_list[0].append(float(invested_list[x]) / float(price_list[x]))
        
        print("Adding new Shares...")
        df["# of Shares"] = shares_list[0]
        wks.set_dataframe(df, (1, 3))
    
    # Find the next available column and insert the share values for the current day
    df = pd.DataFrame()
    df[DATE] = calculateCurrentPrice(price_list, shares_list[0])
    next_col = findNextCol()
    wks.set_dataframe(df, (1, next_col))