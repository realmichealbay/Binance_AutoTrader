import urllib.parse
import hashlib
import hmac
import base64
import requests
import calendar
import asyncio
import time
import os
from datetime import datetime
import logging
from dotenv import load_dotenv
from binance import AsyncClient, BinanceSocketManager

logging.basicConfig(filename="main.log", level=logging.WARNING)
#client = await AsyncClient.create()

load_dotenv()

client = AsyncClient(os.getenv("API_KEY"),os.getenv("API_SECRET"),tld="us")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
logging.WARNING(f"Api Key:{api_key} Api Secret:{api_secret}")

print(client)


api_url = "https://api.binance.us"



# get binanceus signature
def get_binanceus_signature(data, secret):
    postdata = urllib.parse.urlencode(data)
    message = postdata.encode()
    byte_key = bytes(secret, 'UTF-8')
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return mac

# Attaches auth headers and returns results of a POST request
def binanceus_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['X-MBX-APIKEY'] = api_key
    signature = get_binanceus_signature(data, api_sec)
    payload={
        **data,
        "signature": signature,
        }
    req = requests.post((api_url + uri_path), headers=headers, data=payload)
    return req.text


uri_path = "/api/v3/order"
data = {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "LIMIT",
    "timeInForce": "GTC",
    "quantity": 1,
    "price": 0.1,
    "timestamp": int(round(time.time() * 1000))
}

#binanceus_request(uri_path, data, api_key, secret_key)