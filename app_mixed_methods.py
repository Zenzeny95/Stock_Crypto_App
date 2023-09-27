"""
This Python file defines a class named 'Methods' that encapsulates various methods for financial and investment-related
calculations and actions. The class inherits functionality from 'ApiStocksMethods' and 'ApiCryptoMethods' classes,
extending their capabilities.

The primary functionalities provided by this class include:
1. Calculating the gain or loss of an investment in stocks or cryptocurrencies based on an
initial investment amount and a start date.
2. Comparing the gain or loss of two different investments (stocks, cryptocurrencies) based on the same
initial investment amount and start date.

The class includes the following public methods:
- 'calculate_investment_gain_loss': Calculates the gain or loss of an investment.
- 'investment_compare': Compares the gain or loss of two investments.

The file also configures logging for recording events and errors to a log file named 'app.log'.

Note:
- The class assumes access to financial data via the 'ApiStocksMethods' and 'ApiCryptoMethods' classes.
- Proper configuration of SMTP email settings and email templates is required for email alerts.
"""


from app_api_stock_methods import ApiStocksMethods, datetime
from app_api_crypto_methods import ApiCryptoMethods
import logging
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("app.log")
logger.addHandler(file_handler)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s -%(message)s - Nr.%(lineno)d")
file_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)


class Methods(ApiStocksMethods, ApiCryptoMethods):
    """
    Methods class that inherits from ApiStocksMethods and ApiCryptoMethods, providing additional functionality
    for calculating investment gains/losses, comparing investments, and sending email alerts based on price changes.
    """
    def __init__(self):
        super().__init__()

    def calculate_investment_gain_loss(self, amount, start_date, stock=None, crypto=None):
        """
        Calculate the gain or loss of an investment in either stocks or cryptocurrencies.

        Args:
            amount (float): The initial investment amount.
            start_date (str): The start date for calculating the investment gain/loss (YYYY-MM-DD).
            stock (str): The stock symbol (e.g., AAPL) for stock investments.
            crypto (str): The cryptocurrency symbol (e.g., BTC) for crypto investments.

        Returns:
            dict or str: A dictionary containing investment details (if successful), or "Invalid input" (if invalid).

        Note:
            The calculation is based on the difference between the initial investment amount and the current value
            of the investment.

        Example:
            To calculate the gain/loss of a $1000 investment in Apple (AAPL) stock from January 1, 2022:

            ```python
            method = Methods()
            result = method.calculate_investment_gain_loss(1000, "2022-01-01", stock="AAPL")
            print(result)
            ```
        """
        if stock is not None:
            stock_data = self.daily_average(stock, month=start_date)
            initial_price = stock_data.iloc[0]['Open']
            num_shares = float(amount) / float(initial_price)
            current_price = self.now_data_company(stock).iloc[0]['open']
            current_value = num_shares * current_price
            gain_loss = float(current_value) - float(amount)
            stocksai = {"pradine": amount,
                        "akcijos": num_shares,
                        "dabartine": current_value,
                        "pel_nuo": gain_loss}
            logger.info("Gautas akciju ivestavimo ivertinimas")
            return stocksai
        elif crypto is not None:
            siandien = datetime.today().strftime('%Y-%m-%d')
            crypto_data = self.daily_crypto_report(crypto, date=start_date)
            initial_price = crypto_data.iloc[0]['open (USD)']
            num_shares = float(amount) / float(initial_price)
            current_price = self.daily_crypto_report(crypto, date=siandien).iloc[0]['close (USD)']
            current_value = num_shares * current_price
            gain_loss = float(current_value) - float(amount)
            cryptos = {"pradine": amount,
                       "zetonai": num_shares,
                       "dabartine": current_value,
                       "pel_nuo": gain_loss}
            logger.info("Gautas crypto ivestavimo ivertinimas")
            return cryptos
        else:
            return "Bloga ivestis"

    def investment_compare(self, amount, start_date, stock1=None, stock2=None, crypto1=None, crypto2=None):
        """
        Compare the gain or loss of two different investments.

        Args:
            amount (float): The initial investment amount.
            start_date (str): The start date for calculating the investment gain/loss (YYYY-MM-DD).
            stock1 (str): The symbol of the first stock for comparison.
            stock2 (str): The symbol of the second stock for comparison.
            crypto1 (str): The symbol of the first cryptocurrency for comparison.
            crypto2 (str): The symbol of the second cryptocurrency for comparison.

        Returns:
            tuple or str: A tuple containing dictionaries with investment details (if successful),
            or "Invalid input" (if invalid).

        Note:
            The function calculates and compares the gain/loss of two investments based on the provided parameters.

        Example:
            To compare the gain/loss of $1000 investments in Apple (AAPL) and
            Microsoft (MSFT) stocks from January 1, 2022:

            ```python
            method = Methods()
            result = method.investment_compare(1000, "2022-01-01", stock1="AAPL", stock2="MSFT")
            print(result)
            ```
        """
        if stock1 is not None and stock2 is not None:
            pirmas = self.calculate_investment_gain_loss(amount, start_date, stock=stock1)
            antras = self.calculate_investment_gain_loss(amount, start_date, stock=stock2)
            logger.info("Gautas akciju ivestavimo palyginimas")
            return pirmas, antras
        elif stock1 is not None and crypto1 is not None:
            pirmas = self.calculate_investment_gain_loss(amount, start_date, stock=stock1)
            antras = self.calculate_investment_gain_loss(amount, start_date, crypto=crypto1)
            logger.info("Gautas akciju ir crypto ivestavimo palyginimas")
            return pirmas, antras
        elif crypto1 is not None and crypto2 is not None:
            pirmas = self.calculate_investment_gain_loss(amount, start_date, crypto=crypto1)
            antras = self.calculate_investment_gain_loss(amount, start_date, crypto=crypto2)
            logger.info("Gautas crypto ivestavimo palyginimas")
            return pirmas, antras
        else:
            return "Bloga ivestis"
