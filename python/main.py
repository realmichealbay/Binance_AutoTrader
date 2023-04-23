import requests
import asyncio
import time
import os
import logging
import urllib
import hmac
import hashlib
import aiohttp  # Required for async requests
from datetime import datetime
from dotenv import load_dotenv
from binance.enums import *

HEAT = 100
api_url = "https://api.binance.us"
uri_path = "/api/v3/order"


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

def get_binanceus_signature(data, secret):
    postdata = urllib.parse.urlencode(data)
    message = postdata.encode()
    byte_key = bytes(secret, 'UTF-8')
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return mac

async def main():
    logging.basicConfig(filename="main.log", level=logging.INFO)
    load_dotenv()
    global trade_symbol, api_key, api_secret, base_amt, add_profit
    trade_symbol = os.getenv("TRADE_SYMBOL")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    base_amt = float(os.getenv("BASE_AMOUNT"))
    add_profit = bool(os.getenv("ADD_PROFIT_TO_BASE_AMOUNT"))

    logging.info(f"Trade Symbol: {trade_symbol}")
    logging.info(f"API Key: {api_key}")
    logging.info(f"API Secret: {api_secret}")
    logging.warning(f"Base Amount: {base_amt}")
    logging.warning(f"Add Profit To Base Amount: {add_profit}")

async def loop_function():
    print("loop")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(loop_function()), loop.create_task(main())]
    loop.run_until_complete(asyncio.gather(*tasks))
