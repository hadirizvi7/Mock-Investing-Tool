'''
 This script uses sample code from the Google Sheets API Documentation. (https://developers.google.com/sheets/api/quickstart/python)

It has been modified to reflect the intended purpose of the application.
'''

# Import required libraries/dependencies
from __future__ import print_function
import os.path
from tkinter.tix import COLUMN
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Insert your spreadsheet ID
SPREADSHEET_ID = ''

#Function to find the values associated with a specified column in Google Sheets
def findColumns(COL_RANGE):
    creds = None
    # Validate credentials (if the token file exists)
    if os.path.exists('sampleTokens/token.json'):
        creds = Credentials.from_authorized_user_file('sampleTokens/token.json', SCOPES)
    # Otherwise, create valid credentialing
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'sampleTokens/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('sampleTokens/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        # Access the requested Column
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=COL_RANGE, majorDimension = "COLUMNS").execute()
        symbols = result.get('values', [])

        # Edge Case: No Data within specified column
        if not symbols:
            print('No data found.')
            return []

        return symbols
    # Exception handler to catch errors when trying to call Sheets API
    except HttpError as err:
        print(err)