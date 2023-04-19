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
from binance.enums import *




async def main():
    logging.basicConfig(filename="main.log", level=logging.INFO)
    
    
    
    client = await AsyncClient.create()
    
    load_dotenv()
    api_url = "https://api.binance.us"
    trade_symbol = os.getenv("TRADE_SYMBOL")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    logging.info(f"Trade Symbol: {trade_symbol}")
    logging.info(f"API Key: {api_key}")
    logging.info(f"API Secret: {api_secret}")
    
    client = AsyncClient(api_key=api_key,api_secret=api_secret,tld="us")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())



