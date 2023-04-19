import urllib
import hmac
import hashlib
import requests
import asyncio
import time
import os
from datetime import datetime
import logging
from dotenv import load_dotenv   
from binance.enums import *

HEAT = 100
api_url = "https://api.binance.us"
uri_path = "/api/v3/order"


async def main():
    logging.basicConfig(filename="main.log", level=logging.INFO)
    load_dotenv()
    global trade_symbol, api_key, api_secret,base_amt,add_profit
    trade_symbol = os.getenv("TRADE_SYMBOL")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    base_amt = os.getenv("BASE_AMOUNT")
    add_profit = bool(os.getenv("ADD_PROFIT_TO_BASE_AMOUNT"))
    
    logging.info(f"Trade Symbol: {trade_symbol}")
    logging.info(f"API Key: {api_key}")
    logging.info(f"API Secret: {api_secret}")
    logging.warning(f"Base Amount: {base_amt}")
    logging.warning(f"Add Profit To Base Amount: {add_profit}")
    binanceus_request(uri_path,data,api_key,api_secret)
    

def get_binanceus_signature(data, secret):
    postdata = urllib.parse.urlencode(data)
    message = postdata.encode()
    byte_key = bytes(secret, 'UTF-8')
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return mac

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


##time in force options 
#GTC (Good Till Canceled): The order will remain active until it is either filled completely or manually canceled by the trader.
#IOC (Immediate Or Cancel): The order must be filled immediately upon placement, and any unfilled portion of the order is automatically canceled.
#FOK (Fill Or Kill): The order must be filled in its entirety immediately upon placement, otherwise, the whole order is canceled.

data = {
    "symbol": str(trade_symbol),
    "side": "BUY",
    "type": "MARKET",
    "quoteOrderQty":str(base_amt)
}


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

