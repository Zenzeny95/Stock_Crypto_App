"""
api_crypto_methods.py

This module defines a class for retrieving and processing cryptocurrency data.

Classes:
    ApiCryptoMethods: A class that provides methods for generating daily, weekly, and monthly reports
    of cryptocurrency data.

Usage:
    Create an instance of ApiCryptoMethods and use its methods to generate cryptocurrency reports.

Example:
    api_methods = ApiCryptoMethods()
    daily_report = api_methods.daily_crypto_report("BTC", currency="USD", date="2023-09-09")
    print(daily_report)
"""

import pandas as pd
from app_api_crypto_requests import ApiDataCrypto


class ApiCryptoMethods(ApiDataCrypto):
    def __init__(self):
        """
        Initialize a new instance of the ApiCryptoMethods class.

        This class inherits from ApiDataCrypto to access cryptocurrency data.

        Usage:
            api_methods = ApiCryptoMethods()
        """
        super().__init__()

    def daily_crypto_report(self, crypto, currency="USD", date=None):
        """
        Generate a daily cryptocurrency report.

        Args:
            crypto (str): The cryptocurrency symbol (e.g., "BTC").
            currency (str): The currency in which to display prices (default is "USD").
            date (str, optional): The specific date for the report in the "YYYY-MM-DD, YYYY-MM or YYYY" format.
            (default is None).

        Returns:
            pandas.DataFrame: A DataFrame containing daily cryptocurrency data.
        """
        duomenys = pd.DataFrame(self.daily_data_crypto(crypto, currency))
        duomenys = duomenys.set_index("timestamp")
        if currency == "USD":
            duomenys.drop(["open (USD).1", "high (USD).1", "low (USD).1", "close (USD).1"], axis=1, inplace=True)
        else:
            duomenys.drop(["open (USD)", "high (USD)", "low (USD)", "close (USD)"], axis=1, inplace=True)
        if date is not None:
            return duomenys[duomenys.index.str.startswith(date)]
        else:
            return duomenys

    def weekly_crypto_report(self, crypto, currency="USD", date=None):
        """
        Generate a weekly cryptocurrency report.

        Args:
            crypto (str): The cryptocurrency symbol (e.g., "BTC").
            currency (str): The currency in which to display prices (default is "USD").
            date (str, optional): The specific date for the report in the "YYYY-MM or YYYY" format (default is None).

        Returns:
            pandas.DataFrame: A DataFrame containing weekly cryptocurrency data.
        """
        duomenys = pd.DataFrame(self.weekly_data_crypto(crypto, currency).set_index("timestamp"))
        if currency == "USD":
            duomenys.drop(["open (USD).1", "high (USD).1", "low (USD).1", "close (USD).1"], axis=1, inplace=True)
        else:
            duomenys.drop(["open (USD)", "high (USD)", "low (USD)", "close (USD)"], axis=1, inplace=True)
        if date is not None:
            return duomenys[duomenys.index.str.startswith(date)]
        else:
            return duomenys

    def monthly_crypto_report(self, crypto, currency="USD", date=None):
        """
        Generate a monthly cryptocurrency report.

        Args:
            crypto (str): The cryptocurrency symbol (e.g., "BTC").
            currency (str): The currency in which to display prices (default is "USD").
            date (str, optional): The specific date for the report in the "YYYY-MM or YYYY" format (default is None).

        Returns:
            pandas.DataFrame: A DataFrame containing monthly cryptocurrency data.
        """
        duomenys = pd.DataFrame(self.monthly_data_crypto(crypto, currency).set_index("timestamp"))
        if currency == "USD":
            duomenys.drop(["open (USD).1", "high (USD).1", "low (USD).1", "close (USD).1"], axis=1, inplace=True)
        else:
            duomenys.drop(["open (USD)", "high (USD)", "low (USD)", "close (USD)"], axis=1, inplace=True)
        if date is not None:
            return duomenys[duomenys.index.str.startswith(date)]
        else:
            return duomenys
