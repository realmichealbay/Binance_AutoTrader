import requests
import pandas as pd
import time
import websocket
import json
from datetime import datetime

symbol = "BTCusd"

url = f"wss://stream.binance.us:9443/ws/{symbol.lower()}@kline_5m"

# Define the WebSocket connection event handlers
def on_open(ws):
    print("WebSocket connection opened.")

def on_message(ws, message):
    data = json.loads(message)
    with open("data.json", "w") as datafile:
        json.dump(data, datafile)
        datafile.close()

def on_close(ws):
    print("WebSocket connection closed.")

def on_error(ws, error):
    print(f"Error: {error}")

# Create and start the WebSocket connection
ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)
ws.run_forever()
