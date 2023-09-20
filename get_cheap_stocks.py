import requests
from access_tokens import access_tokens
from datetime import datetime, timedelta
from pandas import read_csv
import time
import csv 

# keys required
API_KEY = access_tokens['key']
SECRET_KEY = access_tokens['secret']

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY
}

url_base_point = f"https://data.alpaca.markets/v2/stocks/bars?"

# Start and end datetimes
end_datetime = datetime.now() - timedelta(days=1)
start_datetime = end_datetime - timedelta(days=1)

# Conversion to strings for dates
end_date = end_datetime.strftime("%Y-%m-%d")
start_date = start_datetime.strftime("%Y-%m-%d")


# Time frame
timeframe = "1D"

# Define the output CSV file name
Ticker_csv_file = "stocks_data.csv"

data = read_csv(Ticker_csv_file)
ticker_list = data['Stock'].tolist()

# Batch size for processing 10 symbols at a time
batch_size = 10

# Initialize the index to 0
index = 0

# List to store tradable and cheap stocks
tradable_cheap_stocks = []

while index < len(ticker_list):
    # Get a batch of 10 symbols using slicing
    batch_symbols = ticker_list[index:index + batch_size]
    url_sub_part = f"symbols={','.join(batch_symbols)}&timeframe={timeframe}&start={end_date}&end={end_date}"
    url = url_base_point + url_sub_part

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Process the historical bars data as needed
        # Extract relevant information and filter based on price criteria
        # Example: filter stocks with closing price <= $100
        for symbol, bars in data['bars'].items():
            for bar in bars:
                if bar['c'] <= 100:
                    tradable_cheap_stocks.append((symbol, bar))
        print("data:", data)
    else:
        print(f"Failed to retrieve historical bars data. Status code: {response.status_code}")
        break

    index += batch_size
    time.sleep(4)

# Now tradable_cheap_stocks contains filtered stock data (symbol, bar)
#print(tradable_cheap_stocks)

    
# field names 
fields = ['symbol', 'open','high', 'low', 'close', 'volume', 'numberOfTrades', 'vwap'] 
    

    
# name of csv file 
filename = "cheap_stocks.csv"
try:
    # Writing to the CSV file
    with open(filename, 'w', newline='') as csvfile:  # Use newline='' to avoid extra line breaks
        # Creating a CSV writer object
        csvwriter = csv.writer(csvfile)

        # Writing the header row
        csvwriter.writerow(fields)

        # Writing the data rows
        csvwriter.writerows(tradable_cheap_stocks)
except Exception as e:
    print(f"Error while writing file: {e}")