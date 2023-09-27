"""
The 'CryptoChecks' class contains static methods for performing various checks related to cryptocurrencies,
currencies, and dates.

Class Methods:
- '__init__(self)': Initializes an instance of the 'CryptoChecks' class. (Note: The constructor is empty and does not
perform any specific initialization.)

Static Methods:
- 'is_valid_crypto(crypto)': Checks if a given cryptocurrency abbreviation is valid by comparing it with a list
of known cryptocurrencies.
    - 'crypto': The cryptocurrency abbreviation to be checked.
    - Returns 'True' if the cryptocurrency abbreviation is valid; otherwise, returns 'False'.

- 'is_valid_currency(currency)': Checks if a given currency abbreviation is valid by comparing it
with a list of known currencies.
    - 'currency': The currency abbreviation to be checked.
    - Returns 'True' if the currency abbreviation is valid; 'False' if it is invalid, and 'None'
     if it matches the default currency.

- 'is_valid_date(date)': Checks if a given date string is valid by matching it against valid date patterns for
 YYYY-MM (year-month) or YYYY (year) formats.
    - 'date': The date string to be checked.
    - Returns 'True' if the date string is valid; 'False' if it is invalid, and 'None' if
     it matches the default date format.

Note:
- These static methods are designed to validate user inputs for cryptocurrencies, currencies,
 and dates in a standardized way.
- They perform checks by comparing the input against predefined lists and regular expressions.
- If the input matches a default value (e.g., "Enter Crypto Abbreviation"), the methods return 'None' to
 indicate that the input has not been provided or changed.
"""

import csv
import re


class CryptoChecks:
    def __init__(self):
        pass

    @staticmethod
    def is_valid_crypto(crypto):
        default_crypto = "Enter Crypto Abbreviation"
        if crypto.strip() != default_crypto:
            crypto = crypto.strip().upper()
            crypto_csv_file = 'csv/digital_currency_list.csv'
            with open(crypto_csv_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if crypto in row[0]:
                        return True
                return False
        return False

    @staticmethod
    def is_valid_currency(currency):
        default_currency = "Currency (USD, EUR, GBP, etc...)"
        if currency.strip() != default_currency:
            currency = currency.strip().upper()
            currency_csv_file = 'csv/physical_currency_list.csv'
            with open(currency_csv_file, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if currency in row[0]:
                        return True
                return False
        else:
            return None

    @staticmethod
    def is_valid_date(date):
        default_date = "Date (YYYY-MM or YYYY)"
        month_pattern = r'^(20[0-9]\d|201\d|200[9-9])-([0-1][0-9]|1[0-2])$'
        year_pattern = r'^(20[0-9]\d|201\d|200[9-9])$'

        if date != default_date:
            if re.match(month_pattern, date.strip()):
                return True
            elif re.match(year_pattern, date.strip()):
                return True
            else:
                return False
        else:
            return None
