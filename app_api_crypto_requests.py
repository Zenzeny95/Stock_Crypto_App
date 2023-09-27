"""
api_data_crypto.py

This module provides a class for retrieving and processing cryptocurrency data from an API.

Classes:
    ApiDataCrypto: A class for accessing cryptocurrency data through various API functions.

Usage:
    Create an instance of ApiDataCrypto with your API key and use its methods to retrieve cryptocurrency data.

Example:
    api_crypto = ApiDataCrypto()
    exchange_rate_data = api_crypto.exchange_rate("USD", "BTC")
    daily_crypto_data = api_crypto.daily_data_crypto("BTC", "USD")
    weekly_crypto_data = api_crypto.weekly_data_crypto("BTC", "USD")
    monthly_crypto_data = api_crypto.monthly_data_crypto("BTC", "USD")
"""

import requests
import os
import json
import logging
import pandas as pd
from api_info import HOST_VANTAGE, api_key

HOST_VANTAGE = HOST_VANTAGE

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("app.log")
logger.addHandler(file_handler)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s -%(message)s - Nr.%(lineno)d")
file_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)


class ApiDataCrypto:
    def __init__(self):
        """
        Initialize a new instance of the ApiDataCrypto class.

        This class provides methods for accessing cryptocurrency data through various API functions.

        Usage:
            api_crypto = ApiDataCrypto()
        """
        self.apikey_aplha = api_key

    def exchange_rate(self, currency_from, currency_to):
        """
        Retrieve the exchange rate between two currencies.

        Args:
            currency_from (str): The source currency symbol (e.g., "USD").
            currency_to (str): The target currency symbol (e.g., "BTC").

        Returns:
            dict: A dictionary containing exchange rate information.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "CURRENCY_EXCHANGE_RATE",
                   "from_currency": currency_from,
                   "to_currency": currency_to
                   }
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            exchan = json.loads(r.text)
            logger.info(f"Exchange rate data retrieved. Status code {r.status_code}")
            return exchan
        else:
            logger.error(f"Data not retrieved. Status code {r.status_code}")

    def daily_data_crypto(self, crypto, currency):
        """
        Retrieve daily cryptocurrency data.

        Args:
            crypto (str): The cryptocurrency symbol (e.g., "BTC").
            currency (str): The market currency symbol (e.g., "USD").

        Returns:
            pandas.DataFrame: A DataFrame containing daily cryptocurrency data.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "DIGITAL_CURRENCY_DAILY",
                   "symbol": crypto,
                   "market": currency,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            cdata_daily = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Daily cryptocurrency data retrieved. Status code {r.status_code}")
            return cdata_daily
        else:
            logger.error(f"Cryptocurrency data not retrieved. Status code {r.status_code}")

    def weekly_data_crypto(self, crypto, currency):
        """
        Retrieve weekly cryptocurrency data.

        Args:
            crypto (str): The cryptocurrency symbol (e.g., "BTC").
            currency (str): The market currency symbol (e.g., "USD").

        Returns:
            pandas.DataFrame: A DataFrame containing weekly cryptocurrency data.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "DIGITAL_CURRENCY_WEEKLY",
                   "symbol": crypto,
                   "market": currency,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            cdata_weekly = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Weekly cryptocurrency data retrieved. Status code {r.status_code}")
            return cdata_weekly
        else:
            logger.error(f"Cryptocurrency data not retrieved. Status code {r.status_code}")

    def monthly_data_crypto(self, crypto, currency):
        """
        Retrieve monthly cryptocurrency data.

        Args:
            crypto (str): The cryptocurrency symbol (e.g., "BTC").
            currency (str): The market currency symbol (e.g., "USD").

        Returns:
            pandas.DataFrame: A DataFrame containing monthly cryptocurrency data.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "DIGITAL_CURRENCY_MONTHLY",
                   "symbol": crypto,
                   "market": currency,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            cdata_monthly = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Monthly cryptocurrency data retrieved. Status code {r.status_code}")
            return cdata_monthly
        else:
            logger.error(f"Cryptocurrency data not retrieved. Status code {r.status_code}")
