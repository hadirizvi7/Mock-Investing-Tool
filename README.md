# Mock Investing Tool

This project serves to automate investing workflows by programatically populating a Google Sheets Document with stock data on a daily basis. This is achieved through Python 3.6, the Yahoo Finance API, and the Google Sheets API. The application allows users to input an arbitrary number of stock/crypto tickers to their personal spreadsheet, and track the status of their portfolio over an extended period of time.

## Installation

**NOTE**: The Google Sheets API requires credentialing in order access spreadsheet functionality. This project uses OAuth 2.0 in order to perform reading/writing operations on the correspoding documents. Visit the [Official Google Sheets API Dcumentation](https://developers.google.com/sheets/api/quickstart/python) to see more information about credentialing.

You can find the necessary JSON files under the `sampleTokens` directory. For privacy reasons, I have removed the confidential information that I used to run the application. Feel free to populate these fields for your project or download and replace the files using the quickstart documentation provided above. You must create a Google Cloud Project in order to utilize API keys, OAuth 2.0 Client IDs, or service accounts.

A sample spreadsheet ('sample_sheet.xlsx') is provided. Upload this to your Google Drive and be sure to insert your spreadsheet ID in line 20 of `src/excel_info.py`.

Once the credentialing portion is handled, you can execute the application as follows:

### 1. Download the repository to your Local Device

```bash
git clone https://github.com/hadirizvi7/Mock-Investing-Tool.git
```

### 2. Install the necessary libraries/dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Execute the included Shell Script (MacOS/Linux)

```bash
sh run.sh
```

If everything goes as expected, you should see the Number of Shares field populated based on the amount the user chose to invest. You should also see the following column populated with the portfolio's value for the current day.

## API Considerations

There are a number of APIs that allow developers to fetch live market prices in a quick manner. The project was implemented with efficiency, reliability, and throughput in mind. 

With that being said, here are a few other APIs that were taken into consideration, along with why they were not selected for this project:

1. **Coinbase**

This was initally the default API choice prior to implementation. However, there were a number of technical issues with their web platform when trying to create a new API key. This issue persisted over a number of days and ultimately served as the reason why this platform was not chosen. It is also worth noting that Coinbase only provides crypto data, while we want our application to support stocks as well.

2. **Robinhood**

The `robin_stocks` library in Python allows users to interact with stock information. However, there is no official API for Robinhood. This creates issues with the reliability of the data, making it an impractical choice for our application.

3. **Polygon**

Polygon provides a number of different tiers to their users for API usage. While the free tier does provide up-to-date data, it limits the number of endpoint calls to 5 per minute. This does not bode well for scalibility, as this factor significantly increases the runtime of our application.

Ultimately, the Yahoo Finance API was chosen for this project. A sample of how the the API call works for live stock prices is shown below:

```python
from yahoo_fin import stock_info as si
ticker = 'META'
live_price = si.get_live_price(ticker)
```

## Next Steps

1. **Scheduling**

The application currently uses Crontab to run the shell script on a daily basis. A more scalable approach would be to utilize a cloud platform such as GCP to ensure that any issues with my local machine do not impact job runs. GCP even provides a job scheduler (Cloud Scheduler) that supports cron formatting.

2. **Caching**

There are a number of stocks that users will have in common within their respective portfolios. For example, almost every user that invests in crypto will include Bitcoin or Ethereum to some extent. For this reason, it may be useful to cache common stock data in order to reduce load on the script responsible for making API calls. It also ensures that a failure in this script does not cause the entire application to fail. We could implement a cache policy such as Least Recently Used.

3. **Database Utilization**

There is currently an excel sheet stored on my local device that keeps track of the portfolio spreadsheets that need to be updated. We could potentially store this information in a database to allow for faster querying of document data. This would most likely be a relational database (ex. PostgreSQL) as our data is highly structured.