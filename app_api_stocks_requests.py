"""
api_data_stocks.py

This module defines a class for retrieving and processing stock market data.

Classes:
    ApiDataStocks: A class that provides methods for retrieving various stock market data.

Usage:
    Create an instance of ApiDataStocks and use its methods to retrieve stock market data.
"""

import requests
import os
import logging
import pandas as pd
import json
from datetime import datetime
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


class ApiDataStocks:
    def __init__(self):
        """
       Initialize a new instance of the ApiDataStocks class.

       This class provides methods for retrieving and processing stock market data.

       Usage:
           api_data = ApiDataStocks()
       """
        self.apikey_aplha = api_key
        self.date_now = f"{datetime.now().year}" + "-" + f"{datetime.now().month}".zfill(2)

    def gainers_losers(self):
        """
        Retrieve a list of top gainers and losers in the stock market.

        Returns:
            list: A list of top gainers and losers.

        Example:
            api_data = ApiDataStocks()
            gl_data = api_data.gainers_losers()
            print(gl_data)
        """
        gl_list = []
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "TOP_GAINERS_LOSERS"
                   }
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            gl = json.loads(r.text)
            logger.info(f"Gauta Gainers-Losers data. Status kodas {r.status_code}")
            for key, val in gl.items():
                for zodynas in val:
                    if type(zodynas) == str:
                        pass
                    else:
                        gl_list.append(zodynas)
            return gl_list
        else:
            logger.error(f"Gainer-loser data negauta. Status kodas{r.status_code}")

    def open_close(self):
        """
        Retrieve information about the market's open and close status.

        Returns:
            list: A list containing market open and close information.

        Example:
            api_data = ApiDataStocks()
            oc_data = api_data.open_close()
            print(oc_data)
        """
        oc_list = []
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "MARKET_STATUS"
                   }
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            status = json.loads(r.text)
            logger.info(f"Gauta Open-Close data. Status kodas {r.status_code}")
            for key, val in status.items():
                for zodynas in val:
                    if type(zodynas) == str:
                        pass
                    else:
                        oc_list.append(zodynas)
            return oc_list
        else:
            logger.error(f"Open-close data negauta. Status kodas{r.status_code}")

    def search(self, keyword):
        """
        Search for stock symbols using keywords.

        Args:
            keyword (str): Keywords to search for.

        Returns:
            pandas.DataFrame: A DataFrame containing search results.

        Example:
            api_data = ApiDataStocks()
            search_results = api_data.search("AAPL")
            print(search_results)
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "SYMBOL_SEARCH",
                   "keywords": keyword,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            result = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta Search data. Status kodas {r.status_code}")
            return result
        else:
            logger.error(f"Search data negauta. Status kodas{r.status_code}")

    def now_data_company(self, company):
        """
        Retrieve the latest stock market data for a specific company.

        Args:
            company (str): The company's stock symbol (e.g., "AAPL").

        Returns:
            pandas.DataFrame: A DataFrame containing the latest stock market data for the specified company.

        Example:
            api_data = ApiDataStocks()
            now_data = api_data.now_data_company("AAPL")
            print(now_data)
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "GLOBAL_QUOTE",
                   "symbol": company,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            sdata_now = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta Stock Now data. Status kodas {r.status_code}")
            return sdata_now
        else:
            logger.error(f"Stock data negauta. Status kodas{r.status_code}")

    def daily_data_company(self, company, interval="60min", month=None):
        """
        Retrieve daily stock market data for a specific company.

        Args:
            company (str): The company's stock symbol (e.g., "AAPL").
            interval (str): The time interval for data (default is "60min").
            month (str, optional): The month for which to retrieve the data (default is None).

        Returns:
            pandas.DataFrame: A DataFrame containing daily stock market data for the specified company.

        Example:
            api_data = ApiDataStocks()
            daily_data = api_data.daily_data_company("AAPL", interval="60min", month="2023-09-01")
            print(daily_data)
        """
        if month is None:
            month = self.date_now
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "TIME_SERIES_INTRADAY",
                   "symbol": company,
                   "interval": interval,
                   "month": month,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            print("CSV data downloaded successfully.")
            sdata_daily = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta Stock Daily data. Status kodas {r.status_code}")
            return sdata_daily
        else:
            logger.error(f"Stock data negauta. Status kodas{r.status_code}")

    def day_data_company(self, company):
        """
            Retrieve daily stock data for a given company from an external API.

            Args:
                company (str): The symbol or identifier of the company for which you want to retrieve data.

            Returns:
                pandas.DataFrame: A DataFrame containing daily stock data for the specified company,
                                  including columns such as 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', etc.

            Raises:
                Exception: If the API request fails or returns an error status code.

            This method sends a GET request to an external financial data API to fetch daily stock data
            for the specified company. The retrieved data is in CSV format and is temporarily saved to
            a local file for processing. Upon successful retrieval, the data is read into a pandas DataFrame,
            and the temporary file is removed. If the API request fails, an error message is logged.
            """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "TIME_SERIES_DAILY",
                   "symbol": company,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            print("CSV data downloaded successfully.")
            sdata_daily = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta Stock Daily data. Status kodas {r.status_code}")
            return sdata_daily
        else:
            logger.error(f"Stock data negauta. Status kodas{r.status_code}")

    def weekly_data_company(self, company):
        """
        Retrieve weekly stock market data for a specific company.

        Args:
            company (str): The company's stock symbol (e.g., "AAPL").

        Returns:
            pandas.DataFrame: A DataFrame containing weekly stock market data for the specified company.

        Example:
            api_data = ApiDataStocks()
            weekly_data = api_data.weekly_data_company("AAPL")
            print(weekly_data)
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "TIME_SERIES_WEEKLY",
                   "symbol": company,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            sdata_weekly = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta Stock Weekly data. Status kodas {r.status_code}")
            return sdata_weekly
        else:
            logger.error(f"Stock data negauta. Status kodas{r.status_code}")

    def monthly_data_company(self, company):
        """
        Retrieve monthly stock market data for a specific company.

        Args:
            company (str): The company's stock symbol (e.g., "AAPL").

        Returns:
            pandas.DataFrame: A DataFrame containing monthly stock market data for the specified company.

        Example:
            api_data = ApiDataStocks()
            monthly_data = api_data.monthly_data_company("AAPL")
            print(monthly_data)
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "TIME_SERIES_MONTHLY",
                   "symbol": company,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            sdata_monthly = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta Stock Monthly data. Status kodas {r.status_code}")
            return sdata_monthly
        else:
            logger.error(f"Stock data negauta. Status kodas{r.status_code}")

    def sma(self, symbol, series='close', interval='weekly', timep=60, month=None):
        """
        Retrieve Simple Moving Average (SMA) data for a specific stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., "AAPL").

            series (str): The series type for BBANDS calculation (default is 'close').
            The desired price type in the time series. Four types are supported: close, open, high, low.

            interval (str): The time interval for data (default is 'weekly').
            Time interval between two consecutive data points in the time series.
            The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.

            timep (int): The time period for Aroon Oscillator calculation (default is 60).
            Number of data points used to calculate each AROON value.
            Positive integers are accepted (e.g., time_period=60, time_period=200)

            month (str, optional): The month for which to retrieve the data (default is None).
            This parameter is ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min)
            for the equity markets. The daily/weekly/monthly intervals are agnostic to this parameter.
            By default, this parameter is not set and the technical indicator values will be calculated based on the
            most recent 30 days of intraday data. You can use the month parameter (in YYYY-MM format) to compute
            intraday technical indicators for a specific month in history. For example, month=2009-01.
            Any month equal to or later than 2000-01 (January 2000) is supported.

        Returns:
            pandas.DataFrame: A DataFrame containing SMA data for the specified stock symbol.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "SMA",
                   "symbol": symbol,
                   "interval": interval,
                   "time_period": timep,
                   "series_type": series,
                   "month": month,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            sma = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta SMA data. Status kodas {r.status_code}")
            return sma
        else:
            logger.error(f"SMA data negauta. Status kodas{r.status_code}")

    def ema(self, symbol, series='close', interval='weekly', timep=60, month=None):
        """
        Retrieve Exponential Moving Average (EMA) data for a specific stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., "AAPL").

            series (str): The series type for BBANDS calculation (default is 'close').
            The desired price type in the time series. Four types are supported: close, open, high, low.

            interval (str): The time interval for data (default is 'weekly').
            Time interval between two consecutive data points in the time series.
            The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.

            timep (int): The time period for Aroon Oscillator calculation (default is 60).
            Number of data points used to calculate each AROON value.
            Positive integers are accepted (e.g., time_period=60, time_period=200)

            month (str, optional): The month for which to retrieve the data (default is None).
            This parameter is ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min)
            for the equity markets. The daily/weekly/monthly intervals are agnostic to this parameter.
            By default, this parameter is not set and the technical indicator values will be calculated based on the
            most recent 30 days of intraday data. You can use the month parameter (in YYYY-MM format) to compute
            intraday technical indicators for a specific month in history. For example, month=2009-01.
            Any month equal to or later than 2000-01 (January 2000) is supported.

        Returns:
            pandas.DataFrame: A DataFrame containing EMA data for the specified stock symbol.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "EMA",
                   "symbol": symbol,
                   "interval": interval,
                   "time_period": timep,
                   "series_type": series,
                   "month": month,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            ema = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta EMA data. Status kodas {r.status_code}")
            return ema
        else:
            logger.error(f"EMA data negauta. Status kodas{r.status_code}")

    def stoch(self, symbol, interval='weekly', fastk=5, slowk=3, slowd=3,
              slowkma=0, slowdma=0, month=None):
        """
        Retrieve Stochastic Oscillator (STOCH) data for a specific stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., "AAPL").

            interval (str): The time interval for data (default is 'weekly').
            Time interval between two consecutive data points in the time series.
            The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.

            month (str, optional): The month for which to retrieve the data (default is None).
            This parameter is ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min)
            for the equity markets. The daily/weekly/monthly intervals are agnostic to this parameter.
            By default, this parameter is not set and the technical indicator values will be calculated based on the
            most recent 30 days of intraday data. You can use the month parameter (in YYYY-MM format) to compute
            intraday technical indicators for a specific month in history. For example, month=2009-01.
            Any month equal to or later than 2000-01 (January 2000) is supported.

            fastk (int, optional): The time period for fast %K calculation (default is 5).
            The time period of the fastk moving average. Positive integers are accepted. By default, fastkperiod=5.

            slowk (int, optional): The time period for slow %K calculation (default is 3).
            The time period of the slowk moving average. Positive integers are accepted. By default, slowkperiod=3.

            slowd (int, optional): The time period for slow %D calculation (default is 3).
            The time period of the slowd moving average. Positive integers are accepted. By default, slowdperiod=3.

            slowkma (int, optional): The type of moving average for slow %K (default is 0).
            Moving average type for the slowk moving average. By default, slowkmatype=0. Integers 0 - 8 are accepted
            with the following mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA),
            2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA),
            4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA),
            6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA).

            slowdma (int, optional): The type of moving average for slow %D (default is 0).
            Moving average type for the slowd moving average. By default, slowdmatype=0. Integers 0 - 8 are accepted
            with the following mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA),
            2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA),
            4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA),
            6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA).

        Returns:
            pandas.DataFrame: A DataFrame containing STOCH data for the specified stock symbol.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "STOCH",
                   "symbol": symbol,
                   "interval": interval,
                   "month": month,
                   "fastkperiod": fastk,
                   "slowkperiod": slowk,
                   "slowdperiod": slowd,
                   "slowkmatype": slowkma,
                   "slowdmatype": slowdma,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            stoch = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta Stoch data. Status kodas {r.status_code}")
            return stoch
        else:
            logger.error(f"Stoch data negauta. Status kodas{r.status_code}")

    def rsi(self, symbol, interval='weekly', timep='60', series='close', month=None):
        """
        Retrieve Relative Strength Index (RSI) data for a specific stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., "AAPL").

            interval (str): The time interval for data (default is 'weekly').
            Time interval between two consecutive data points in the time series.
            The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.

            timep (int): The time period for Aroon Oscillator calculation (default is 60).
            Number of data points used to calculate each AROON value.
            Positive integers are accepted (e.g., time_period=60, time_period=200)

            series (str): The series type for RSI calculation (default is 'close').
            The desired price type in the time series. Four types are supported: close, open, high, low.

            month (str, optional): The month for which to retrieve the data (default is None).
            This parameter is ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min)
            for the equity markets. The daily/weekly/monthly intervals are agnostic to this parameter.
            By default, this parameter is not set and the technical indicator values will be calculated based on the
            most recent 30 days of intraday data. You can use the month parameter (in YYYY-MM format) to compute
            intraday technical indicators for a specific month in history. For example, month=2009-01.
            Any month equal to or later than 2000-01 (January 2000) is supported.

        Returns:
            pandas.DataFrame: A DataFrame containing RSI data for the specified stock symbol.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "RSI",
                   "symbol": symbol,
                   "interval": interval,
                   "time_period": timep,
                   "series_type": series,
                   "month": month,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            rsi = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta RSI data. Status kodas {r.status_code}")
            return rsi
        else:
            logger.error(f"RSI data negauta. Status kodas{r.status_code}")

    def adx(self, symbol, interval='weekly', timep='60', month=None):
        """
        Retrieve Average Directional Index (ADX) data for a specific stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., "AAPL").

            interval (str): The time interval for data (default is 'weekly').
            Time interval between two consecutive data points in the time series.
            The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.

            timep (int): The time period for Aroon Oscillator calculation (default is 60).
            Number of data points used to calculate each AROON value.
            Positive integers are accepted (e.g., time_period=60, time_period=200)

            month (str, optional): The month for which to retrieve the data (default is None).
            This parameter is ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min)
            for the equity markets. The daily/weekly/monthly intervals are agnostic to this parameter.
            By default, this parameter is not set and the technical indicator values will be calculated based on the
            most recent 30 days of intraday data. You can use the month parameter (in YYYY-MM format) to compute
            intraday technical indicators for a specific month in history. For example, month=2009-01.
            Any month equal to or later than 2000-01 (January 2000) is supported.

        Returns:
            pandas.DataFrame: A DataFrame containing ADX data for the specified stock symbol.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "ADX",
                   "symbol": symbol,
                   "interval": interval,
                   "time_period": timep,
                   "month": month,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            adx = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta ADX data. Status kodas {r.status_code}")
            return adx
        else:
            logger.error(f"ADX data negauta. Status kodas{r.status_code}")

    def cci(self, symbol, interval='weekly', timep='60', month=None):
        """
        Retrieve Commodity Channel Index (CCI) data for a specific stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., "AAPL").

            interval (str): The time interval for data (default is 'weekly').
            Time interval between two consecutive data points in the time series.
            The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.

            timep (int): The time period for Aroon Oscillator calculation (default is 60).
            Number of data points used to calculate each AROON value.
            Positive integers are accepted (e.g., time_period=60, time_period=200)

            month (str, optional): The month for which to retrieve the data (default is None).
            This parameter is ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min)
            for the equity markets. The daily/weekly/monthly intervals are agnostic to this parameter.
            By default, this parameter is not set and the technical indicator values will be calculated based on the
            most recent 30 days of intraday data. You can use the month parameter (in YYYY-MM format) to compute
            intraday technical indicators for a specific month in history. For example, month=2009-01.
            Any month equal to or later than 2000-01 (January 2000) is supported.

        Returns:
            pandas.DataFrame: A DataFrame containing CCI data for the specified stock symbol.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "CCI",
                   "symbol": symbol,
                   "interval": interval,
                   "time_period": timep,
                   "month": month,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            cci = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta CCI data. Status kodas {r.status_code}")
            return cci
        else:
            logger.error(f"CCI data negauta. Status kodas{r.status_code}")

    def aroon(self, symbol, interval='weekly', timep='60', month=None):
        """
        Retrieve Aroon Oscillator data for a specific stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., "AAPL").

            interval (str): The time interval for data (default is 'weekly').
            Time interval between two consecutive data points in the time series.
            The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.

            timep (int): The time period for Aroon Oscillator calculation (default is 60).
            Number of data points used to calculate each AROON value.
            Positive integers are accepted (e.g., time_period=60, time_period=200)

            month (str, optional): The month for which to retrieve the data (default is None).
            This parameter is ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min)
            for the equity markets. The daily/weekly/monthly intervals are agnostic to this parameter.
            By default, this parameter is not set and the technical indicator values will be calculated based on the
            most recent 30 days of intraday data. You can use the month parameter (in YYYY-MM format) to compute
            intraday technical indicators for a specific month in history. For example, month=2009-01.
            Any month equal to or later than 2000-01 (January 2000) is supported.

        Returns:
            pandas.DataFrame: A DataFrame containing Aroon Oscillator data for the specified stock symbol.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "AROON",
                   "symbol": symbol,
                   "interval": interval,
                   "time_period": timep,
                   "month": month,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            aroon = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta AROON data. Status kodas {r.status_code}")
            return aroon
        else:
            logger.error(f"AROON data negauta. Status kodas{r.status_code}")

    def bbands(self, symbol, interval='weekly', timep='60min', series='close',
               nbdevup=2, nbdevdn=2, matype=0, month=None):
        """
        Retrieve Bollinger Bands (BBANDS) data for a specific stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., "AAPL").

            interval (str): The time interval for data (default is 'weekly').

            timep (int): The time period for BBANDS calculation (default is 60).
            The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly

            series (str): The series type for BBANDS calculation (default is 'close').
            The desired price type in the time series. Four types are supported: close, open, high, low.

            month (str, optional): The month for which to retrieve the data (default is None).
            This parameter is ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min)
            for the equity markets. The daily/weekly/monthly intervals are agnostic to this parameter.
            By default, this parameter is not set and the technical indicator values will be calculated based on the
            most recent 30 days of intraday data. You can use the month parameter (in YYYY-MM format) to compute
            intraday technical indicators for a specific month in history. For example, month=2009-01.
            Any month equal to or later than 2000-01 (January 2000) is supported.

            nbdevup (int, optional):
            The standard deviation multiplier of the upper band. Positive integers are accepted. By default, nbdevup=2.

            nbdevdn (int, optional):
            The standard deviation multiplier of the lower band. Positive integers are accepted. By default, nbdevdn=2.

            matype(int, optional):
            Moving average type of the time series. By default, matype=0. Integers 0 - 8 are accepted with the following
            mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA), 2 = Weighted Moving Average
            (WMA), 3 = Double Exponential Moving Average (DEMA), 4 = Triple Exponential Moving Average (TEMA),
            5 = Triangular Moving Average (TRIMA), 6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA),
            8 = MESA Adaptive Moving Average (MAMA).

        Returns:
            pandas.DataFrame: A DataFrame containing BBANDS data for the specified stock symbol.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "BBANDS",
                   "symbol": symbol,
                   "interval": interval,
                   "time_period": timep,
                   "series_type": series,
                   "month": month,
                   "nbdevup": nbdevup,
                   "nbdevdn": nbdevdn,
                   "matype": matype,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            bbands = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta BBANDS data. Status kodas {r.status_code}")
            return bbands
        else:
            logger.error(f"BBANDS data negauta. Status kodas{r.status_code}")

    def ad(self, symbol, interval='weekly', month=None):
        """
        Retrieve Chaikin A/D Line (AD) data for a specific stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., "AAPL").

            interval (str): The time interval for data (default is 'weekly').
            Time interval between two consecutive data points in the time series.
            The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.

            month (str, optional): The month for which to retrieve the data (default is None).
            This parameter is ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min)
            for the equity markets. The daily/weekly/monthly intervals are agnostic to this parameter.
            By default, this parameter is not set and the technical indicator values will be calculated based on the
            most recent 30 days of intraday data. You can use the month parameter (in YYYY-MM format) to compute
            intraday technical indicators for a specific month in history. For example, month=2009-01.
            Any month equal to or later than 2000-01 (January 2000) is supported.

        Returns:
            pandas.DataFrame: A DataFrame containing Chaikin A/D Line data for the specified stock symbol.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "AD",
                   "symbol": symbol,
                   "interval": interval,
                   "month": month,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            ad = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta AD data. Status kodas {r.status_code}")
            return ad
        else:
            logger.error(f"AD data negauta. Status kodas{r.status_code}")

    def obv(self, symbol, interval='weekly', month=None):
        """
        Retrieve On-Balance Volume (OBV) data for a specific stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., "AAPL").

            interval (str): The time interval for data (default is 'weekly').
            Time interval between two consecutive data points in the time series.
            The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.

            month (str, optional): The month for which to retrieve the data (default is None).
            This parameter is ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min)
            for the equity markets. The daily/weekly/monthly intervals are agnostic to this parameter.
            By default, this parameter is not set and the technical indicator values will be calculated based on the
            most recent 30 days of intraday data. You can use the month parameter (in YYYY-MM format) to compute
            intraday technical indicators for a specific month in history. For example, month=2009-01.
            Any month equal to or later than 2000-01 (January 2000) is supported.

        Returns:
            pandas.DataFrame: A DataFrame containing OBV data for the specified stock symbol.
        """
        endpoint = "/query"
        payload = {"apikey": self.apikey_aplha,
                   "function": "OBV",
                   "symbol": symbol,
                   "interval": interval,
                   "month": month,
                   "outputsize": "full",
                   "datatype": "csv"}
        r = requests.get(HOST_VANTAGE + endpoint, params=payload)
        if r.status_code in range(200, 400):
            temp_csv_path = "temp_data.csv"
            with open(temp_csv_path, 'wb') as f:
                f.write(r.content)
            obv = pd.read_csv(temp_csv_path)
            os.remove(temp_csv_path)
            logger.info(f"Gauta OBV data. Status kodas {r.status_code}")
            return obv
        else:
            logger.error(f"OBV data negauta. Status kodas{r.status_code}")
