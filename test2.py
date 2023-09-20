import requests
from access_tokens import access_tokens

# Replace 'YOUR_STOCK_SYMBOLS' with a comma-separated list of symbols you want to query
symbols = "AAPL"
# Replace 'YOUR_TIMEFRAME' with the desired timeframe, e.g., '1D' for daily bars
timeframe = "1D"

# keys required
API_KEY = access_tokens['key']
SECRET_KEY = access_tokens['secret']

# Define the start and end date for the historical data
start_date = "2023-09-18"
end_date = "2023-09-19"

url = f"https://data.alpaca.markets/v2/stocks/bars?symbols={symbols}&timeframe={timeframe}&start={start_date}&end={end_date}"

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    # Process the historical bars data as needed
    print(data)
else:
    print(f"Failed to retrieve historical bars data. Status code: {response.status_code}")
