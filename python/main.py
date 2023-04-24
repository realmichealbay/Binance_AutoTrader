# regular imports
import requests #pip
import asyncio #not pip
import time #not pip
import os #not pip
import logging # ?
import aiohttp # not pip
import json #not pip
import websocket #pip
import keyboard #pipimport matplotlib as plt
import urllib
import hmac
import hashlib
# from imports
from datetime import datetime #not pip
from dotenv import load_dotenv #pip
from binance.enums import * # pip
#application imports


HEAT = 100
api_url = "https://api.binance.us"
uri_path = "/api/v3/order"
short_period = 12
long_period = 26
signal_period = 9
price_history = []
data_points_received = 0
data_points_to_update_plot = 50
max_data_points = 100
last_action = None
macd_line = None
prev_macd_signal_diff = None
signal_line = None

key_seq = ["t","r"]
pressed_keys = []

def plot_data(price_history, macd_line, signal_line):
    plt.figure(figsize=(12, 6))
    plt.plot(price_history, label="Price")
    plt.plot(macd_line, label="MACD Line", linestyle="--")
    plt.plot(signal_line, label="Signal Line", linestyle="--")
    plt.legend(loc="upper left")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title("MACD Indicator")
    plt.grid()
    plt.show()
def calc_ema(price_history, period, smoothing=0):
    ema = [sum(price_history[:period]) / period]
    for price in price_history[period:]:
        ema.append((price * (smoothing / (1 + period))) + ema[-1] * (1 - (smoothing / (1 + period))))
    return ema
def get_binanceus_signature(data, secret):
    postdata = urllib.parse.urlencode(data)
    message = postdata.encode()
    byte_key = bytes(secret, 'UTF-8')
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return mac
def check_key(pressed_keys):
    return pressed_keys[-len(key_seq):] == key_seq
def on_key_event(e):
    global pressed_keys
    if  e.event_type == keyboard.KEY_DOWN:
        pressed_keys.append(e.name)
        if check_key(pressed_keys):
            print("key detected")
def on_open(ws):
    print("WebSocket connection opened.")
def on_message(ws, message):
    global price_history, prev_macd_signal_diff,data_points_received,macd_line,signal_line,last_action
    data = json.loads(message)
    close_price = float(data['k']['c'])
    print(len(price_history))
    price_history.append(close_price)
    if len(price_history) > max_data_points:
        price_history = price_history[-(max_data_points):]
        short_ema = calc_ema(price_history, short_period)
        long_ema = calc_ema(price_history, long_period)
        macd_line = [short - long for short, long in zip(short_ema[-long_period:], long_ema)]
        signal_line = calc_ema(macd_line, signal_period)
        macd_signal_diff = macd_line[-1] - signal_line[-1]
        print(macd_line[-1])
        if prev_macd_signal_diff is not None:
            # Buy signal
            if macd_signal_diff > 0 and prev_macd_signal_diff <= 0 and last_action != "buy":
                last_action = "buy"
                print(f"Buy signal at price {price_history[-1]}")
        # Sell signal
            elif macd_signal_diff < 0 and prev_macd_signal_diff >= 0 and last_action != "sell":
                last_action = "sell"
                print(f"Sell signal at price {price_history[-1]}")
        prev_macd_signal_diff = macd_signal_diff
        data_points_received += 1       
def on_close(ws):
    print("WebSocket connection closed.")
def on_error(ws, error):
    print(f"Error: {error}")
async def buy_position(uri_path, api_key, api_sec):
    data = {
        "symbol": trade_symbol,
        "side": "BUY",
        "type": "MARKET",
        "quoteOrderQty": str(base_amt),
        "timestamp": int(time.time() * 1000)
    }
    headers = {}
    headers['X-MBX-APIKEY'] = api_key
    signature = get_binanceus_signature(data, api_sec)
    payload = {
        **data,
        "signature": signature,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post((api_url + uri_path), headers=headers, data=payload) as req:
            logging.warning(f"Buy Succeeded {req}")
            return await req.text()
async def sell_position(uri_path, api_key, api_sec):
    data = {
        "symbol": trade_symbol,
        "side": "SELL",
        "type": "MARKET",
        "quoteOrderQty": str(base_amt),
        "timestamp": int(time.time() * 1000)
    }
    headers = {}
    headers['X-MBX-APIKEY'] = api_key
    signature = get_binanceus_signature(data, api_sec)
    payload = {
        **data,
        "signature": signature,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post((api_url + uri_path), headers=headers, data=payload) as req:
            logging.warning(f"Sell Succeeded {req}")
            return await req.text()
async def main():
    logging.basicConfig(filename="main.log", level=logging.INFO)
    load_dotenv()
    global trade_symbol, api_key, api_secret, base_amt, add_profit, wss_url
    trade_symbol = os.getenv("TRADE_SYMBOL")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    base_amt = float(os.getenv("BASE_AMOUNT"))
    add_profit = bool(os.getenv("ADD_PROFIT_TO_BASE_AMOUNT"))
    wss_url = f"wss://stream.binance.us:9443/ws/{trade_symbol.lower()}@kline_15m"
    logging.info(f"Trade Symbol: {trade_symbol}")
    logging.info(f"API Key: {api_key}")
    logging.info(f"API Secret: {api_secret}")
    logging.warning(f"Base Amount: {base_amt}")
    logging.warning(f"Add Profit To Base Amount: {add_profit}")
async def loop_function():
    print("running")
    keyboard.hook(on_key_event)
    if data_points_received % data_points_to_update_plot == 0:
       plot_data(price_history, macd_line, signal_line)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(loop_function()), loop.create_task(main())]
    loop.run_until_complete(asyncio.gather(*tasks))
    ws = websocket.WebSocketApp(wss_url, on_open=on_open, on_message=on_message, on_close=on_close, on_error=on_error)
    ws.run_forever()
