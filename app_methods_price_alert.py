"""
AlertSystem - Email-Based Price Alert System

This class defines an email-based price alert system that allows users to set price thresholds for stocks
 and cryptocurrencies and receive email notifications when the price reaches the specified threshold.

Methods:
    __init__(self, name, email, price, stock=None, crypto=None):
        Initializes the AlertSystem with user-specific information.

    alert(self):
        Checks the current price of the specified stock or cryptocurrency and schedules recurring
         price checks based on the provided thresholds.

    check_stock_price_higher(self, email, price, name, stock, siandien):
        Checks if the current stock price is higher than the specified threshold and schedules
         recurring checks if needed.

    check_stock_price_lower(self, email, price, name, stock, siandien):
        Checks if the current stock price is lower than the specified threshold and schedules
         recurring checks if needed.

    check_crypto_price_higher(self, email, price, name, crypto):
        Checks if the current cryptocurrency price is higher than the specified threshold and schedules
         recurring checks if needed.

    check_crypto_price_lower(self, email, price, name, crypto):
        Checks if the current cryptocurrency price is lower than the specified threshold and schedules
         recurring checks if needed.

    send_alert(self, current_price):
        Sends an email alert containing information about the price alert trigger to the specified recipient.

Usage:
    Create an instance of the AlertSystem class and call the alert() method to start monitoring price alerts.
    Customize the SMTP_HOST, PORT, EMAIL, and PASSWORD attributes for your email configuration.
"""

from datetime import datetime
import logging
import smtplib
import threading
from email.message import EmailMessage
from emailo_config import SMTP_HOST, PORT, EMAIL, PASSWORD
from string import Template
from app_api_stock_methods import ApiStocksMethods
from app_api_crypto_methods import ApiCryptoMethods


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("app.log")
logger.addHandler(file_handler)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s -%(message)s - Nr.%(lineno)d")
file_handler.setFormatter(formatter)

logger.setLevel(logging.INFO)


class AlertSystem:
    def __init__(self, name, email, price, stock=None, crypto=None):
        self.SMTP_HOST = SMTP_HOST
        self.PORT = PORT
        self.EMAIL = EMAIL
        self.PASSWORD = PASSWORD
        self.name = name
        self.email = email
        self.price = price
        self.stock = stock
        self.crypto = crypto
        self.stock_methods = ApiStocksMethods()
        self.crypto_methods = ApiCryptoMethods()

    def alert(self):
        try:
            siandien = f"{datetime.now().year}-{datetime.now().month})"
            verte = float(self.price)
            if self.stock is None and self.crypto is None:
                raise ValueError
            elif self.stock is not None:
                kaina = self.stock_methods.daily_data_company(self.stock, interval="5min", month=siandien)
                stock_kaina = kaina.iloc[0]['close']
                if verte > float(stock_kaina):
                    self.check_stock_price_higher(self.email, self.price, self.name, self.stock, siandien)
                elif verte < float(stock_kaina):
                    self.check_stock_price_lower(self.email, self.price, self.name, self.stock, siandien)
                else:
                    return "Invalid input"
            elif self.crypto is not None:
                data = datetime.today()
                siandien = datetime.strftime(data, '%Y-%m-%d')
                kaina = self.crypto_methods.daily_crypto_report(self.crypto, date=siandien).iloc[0]['close (USD)']
                crypto_kaina = kaina.iloc[0]['close']
                if verte > crypto_kaina:
                    self.check_crypto_price_higher(self.email, self.price, self.name, self.crypto)
                elif verte < crypto_kaina:
                    self.check_crypto_price_lower(self.email, self.price, self.name, self.crypto)
                else:
                    return "Invalid input"
        except (IndexError, AttributeError, ValueError):
            logger.exception(IndexError, AttributeError, ValueError)
            return "Invalid Entry"

    def check_stock_price_higher(self, email, price, name, stock, siandien):
        kaina = self.stock_methods.daily_data_company(stock, interval="5min", month=siandien)
        stock_kaina = kaina.iloc[0]['close']
        verte = float(price)
        if verte > float(stock_kaina):
            threading.Timer(300, self.check_stock_price_higher, args=(email, price, name, stock, siandien)).start()
        elif verte <= float(stock_kaina):
            self.send_alert(stock_kaina)

    def check_stock_price_lower(self, email, price, name, stock, siandien):
        kaina = self.stock_methods.daily_data_company(stock, interval="5min", month=siandien)
        stock_kaina = kaina.iloc[0]['close']
        verte = float(price)
        if verte < float(stock_kaina):
            threading.Timer(300, self.check_stock_price_lower, args=(email, price, name, stock, siandien)).start()
        elif verte >= float(stock_kaina):
            self.send_alert(stock_kaina)

    def check_crypto_price_higher(self, email, price, name, crypto):
        data = datetime.today()
        siandien = datetime.strftime(data, '%Y-%m-%d')
        kaina = self.crypto_methods.daily_crypto_report(crypto, date=siandien).iloc[0]['close (USD)']
        crypto_kaina = kaina.iloc[0]['close']
        verte = float(price)
        if verte > float(crypto_kaina):
            threading.Timer(300, self.check_crypto_price_higher, args=(email, price, name, crypto)).start()
        elif verte <= float(crypto_kaina):
            self.send_alert(crypto_kaina)

    def check_crypto_price_lower(self, email, price, name, crypto):
        data = datetime.today()
        siandien = datetime.strftime(data, '%Y-%m-%d')
        kaina = self.crypto_methods.daily_crypto_report(crypto, date=siandien).iloc[0]['close (USD)']
        crypto_kaina = kaina.iloc[0]['close']
        verte = float(price)
        if verte < float(crypto_kaina):
            threading.Timer(300, self.check_crypto_price_lower, args=(email, price, name, crypto)).start()
        elif verte >= float(crypto_kaina):
            self.send_alert(crypto_kaina)

    def send_alert(self, current_price):
        try:
            email = EmailMessage()
            email["from"] = f"Stock & Crypto App Alert <{self.EMAIL}>"
            email["to"] = self.email
            email["subject"] = "Price Alert"
            with open("templates/alert.html", mode="r", encoding="utf-8") as f:
                html_text = f.read()
            pakeitimai = {"vardas": self.name, "verte": current_price}
            sablonas = Template(html_text)
            html_text = sablonas.substitute(pakeitimai)
            email.set_content(html_text, "html")
            with smtplib.SMTP(host=self.SMTP_HOST, port=self.PORT) as smtp_server:
                smtp_server.ehlo()
                smtp_server.starttls()
                smtp_server.login(self.EMAIL, self.PASSWORD)
                smtp_server.send_message(email)
            logger.info("Alert email sent")
        except (IndexError, AttributeError, ValueError):
            logger.exception(IndexError, AttributeError, ValueError)
            return "Invalid Entry"
