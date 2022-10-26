from __future__ import print_function

import os.path
from tkinter.tix import COLUMN

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1CWZWHVS9yfGvuP0_rT9LJkcqQoTrV4CjS8D0hX7t2k8'

def findColumns(COL_RANGE):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    if os.path.exists('tokens/token.json'):
        creds = Credentials.from_authorized_user_file('tokens/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'tokens/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tokens/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=COL_RANGE, majorDimension = "COLUMNS").execute()
        symbols = result.get('values', [])

        if not symbols:
            print('No data found.')
            return []

        return symbols
    except HttpError as err:
        print(err)