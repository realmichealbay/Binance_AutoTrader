import requests
import pandas as pd
import time
import webinterface
import matplotlib.pyplot as plt
import mplfinance  as mpf

# Binance API credentials
api_key = 'PUrKb7XrH7svUWinjOabWUni0svd8rKWG1rRpxUEg6bqWxOjIKMMO4BclQGvFHBb'
api_secret = 'SNCIeKfh282jJOBFdX8W2e9jCdnRnqReI6F9rNcWyPXRDLgurRxHbfJqpKoxVavH'

# Binance API base URL
base_url = 'https://api.binance.us'  # for Binance US

endpoint = '/api/v3/klines'

# Define the trading pair, interval, and other parameters
symbol = 'RNDRUSD'
interval = '5m'
limit = 228 # Maximum allowed by Binance API

# Build the request URL
url = f"{base_url}{endpoint}?symbol={symbol}&interval={interval}&limit={limit}"

# Add the API key to the request headers
headers = {
    'X-MBX-APIKEY': api_key
}

# Send the request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    historical_data = response.json()
    # Convert the data to a pandas DataFrame
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume',
               'close_time', 'quote_asset_volume', 'trades', 'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore']
    df = pd.DataFrame(historical_data, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.sort_values(by='timestamp')
    
else:
    print(f"Error fetching historical data: {response.status_code} - {response.text}")

# Plot the data
#fig, ax = plt.subplots()
# Format the plot
plt.xlabel('Time')
plt.ylabel('Price (USD)')
plt.title(f"{symbol} Price over Time")
plt.plot(df[],df['open'])
plt.show()
