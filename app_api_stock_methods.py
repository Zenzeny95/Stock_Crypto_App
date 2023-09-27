"""
api_stocks_methods.py

This module defines a class for retrieving and processing stock market data.

Classes:
    ApiStocksMethods: A class that provides methods for generating stock market reports.

Usage:
    Create an instance of ApiStocksMethods and use its methods to generate stock market reports.

Example:
    api_methods = ApiStocksMethods()
    now_data = api_methods.now_data_report("AAPL")
    daily_avg = api_methods.daily_average("AAPL", interval="60min", month="2023-09")
    daily_details = api_methods.daily_detailed_report("AAPL", interval="60min", month="2023-09")
    weekly_data = api_methods.weekly_report("AAPL", date="2023-09-09")
    monthly_data = api_methods.monthly_report("AAPL", date="2023-09-09")
"""

import pandas as pd
from datetime import datetime
from app_api_stocks_requests import ApiDataStocks


class ApiStocksMethods(ApiDataStocks):
    def __init__(self):
        """
                Initialize a new instance of the ApiStocksMethods class.

                This class inherits from ApiDataStocks to access stock market data.

                Usage:
                    api_methods = ApiStocksMethods()
                """
        super().__init__()
        self.date_now = f"{datetime.now().year}" + "-" + f"{datetime.now().month}".zfill(2)

    def now_data_report(self, company):
        """
                Generate a report with the latest stock market data for a specific company.

                Args:
                    company (str): The company's stock symbol (e.g., "AAPL").

                Returns:
                    pandas.DataFrame: A DataFrame containing the latest stock market data.
                """
        return self.now_data_company(company)

    def daily_average(self, company, interval="60min", month=None):
        """
                Generate a daily average report for a specific company's stock.

                Args:
                    company (str): The company's stock symbol (e.g., "AAPL").
                    interval (str): The time interval for data (default is "60min").
                    month (str): The specific date for the report in the "YYYY-MM-DD, YYYY-MM, YYYY" format
                  (default is None).

                Returns:
                    pandas.DataFrame: A DataFrame containing the daily average
                     stock market data for the specified month.
                """
        if month is None:
            month = self.date_now
        if len(month.split('-')) == 3:
            y, m, d = month.split('-')
            report = self.daily_data_company(company, interval, month=(y + '-' + m)).set_index("timestamp")
            report2 = report[report.index.str.startswith(month)]
            df_new = pd.DataFrame({'Data': month,
                                   'Open': report2['open'].mean(),
                                   'High': report2['high'].mean(),
                                   'Low': report2['low'].mean(),
                                   'Close': report2['close'].mean(),
                                   'Volume': report2['volume'].sum(),
                                   "Change amount": (report2['close'].mean() - report2['open'].mean()),
                                   "Change %": ((report2['close'].mean() - report2['open'].mean())
                                                / report2['close'].mean() * 100)
                                   }, index=[0])
            return df_new
        return "No Data For This Date"

    def daily_detailed_report(self, company, interval="60min", month=None):
        """
              Generate a detailed daily report for a specific company's stock.

              Args:
                  company (str): The company's stock symbol (e.g., "AAPL").
                  interval (str): The time interval for data (default is "60min").
                  month (str): The specific date for the report in the "YYYY-MM-DD, YYYY-MM, YYYY" format
                  (default is None).

              Returns:
                  pandas.DataFrame: A DataFrame containing detailed daily stock market data for the specified month.
              """
        if month is None:
            month = self.date_now
        if len(month.split('-')) == 2:
            return self.daily_data_company(company, interval, month).set_index("timestamp")
        if len(month.split('-')) == 3:
            y, m, d = month.split('-')
            report = self.daily_data_company(company, interval, month=(y + '-' + m)).set_index("timestamp")
            return report[report.index.str.startswith(month)]
        return "No Data For This Date"

    def weekly_report(self, company, date=None):
        """
               Generate a weekly report for a specific company's stock.

               Args:
                   company (str): The company's stock symbol (e.g., "AAPL").
                   date (str: The specific date for the report in the "YYYY-MM or YYYY" format (default is None).

               Returns:
                   pandas.DataFrame: A DataFrame containing weekly stock market data.
               """
        report = self.weekly_data_company(company).set_index("timestamp")
        if date is not None:
            return report[report.index.str.startswith(date)]
        else:
            return report

    def monthly_report(self, company, date=None):
        """
                Generate a monthly report for a specific company's stock.

                Args:
                    company (str): The company's stock symbol (e.g., "AAPL").
                    date (str): The specific date for the report in the "YYYY-MM or YYYY" format (default is None).

                Returns:
                    pandas.DataFrame: A DataFrame containing monthly stock market data.
                """
        report = self.monthly_data_company(company).set_index("timestamp")
        if date is not None:
            return report[report.index.str.startswith(date)]
        else:
            return report
