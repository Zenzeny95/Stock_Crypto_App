"""
The 'PaymentChecks' class provides methods for checking and processing payment information for upgrading user accounts.
This class is primarily designed for use in a graphical user interface (GUI) application, where users can enter
credit card details to make payments.

Class Attributes:
- 'window': Represents the master window of the GUI application.

Methods:
- 'upgrade_check()': Checks the validity of credit card information provided by the user. It validates the
credit card number, expiration date, and CVV code. If the information is valid, it also performs a test payment using
the Stripe API to ensure the card is functional. Returns True if the payment information is valid;
otherwise, returns False.

- 'payment_check_testing(card, month, year, cvv)': Conducts a test payment using the Stripe API to verify the validity
of the provided payment information. It checks if the payment is successful and
returns True if the payment succeeds; otherwise, returns False.

- 'countdown(time_left)': Displays a countdown message in the GUI, indicating a successful action and informing the user
that the window will close automatically after a specified time.

Note:
- This class relies on the 'stripe' library and the 'stripe_key' obtained from the 'api_info'
module to interact with the Stripe payment gateway.
- The 'window' attribute should be set to the master window of the GUI application for proper functionality.
- It is assumed that the GUI application will handle the display and interaction with the user.
- Proper configuration of the Stripe API is required for payment processing.
"""


import re
import stripe
from datetime import datetime
from api_info import stripe_key


class PaymentChecks:
    def __init__(self, master):
        self.window = master

    def upgrade_check(self):
        card = self.window.entry_card_var.get()
        expire = self.window.entry_expire_var.get()
        cvv = self.window.entry_code_var.get()

        try:
            credit_card_pattern = re.compile(r'^((\d{4}\s?\d{4}\s?\d{4}\s?\d{4}$) | (^\d{4}\s?\d{6}\s?\d{5}))$',
                                             re.VERBOSE)
            if not re.match(credit_card_pattern, card):
                self.window.label_message['fg'] = 'red'
                self.window.label_message['text'] = "Invalid credit card."
                return False
            if not re.match(r'^((0[1-9]|1[0-2])/([2-9]\d))$', expire):
                self.window.label_message['fg'] = 'red'
                self.window.label_message['text'] = "Invalid expiration date."
                return False
            else:
                current_date = datetime.now()
                expiration_month, expiration_year = map(int, expire.strip().split('/'))
                if 49 >= expiration_year >= 0:
                    expiration_year_new = 2000 + expiration_year
                else:
                    self.window.label_message['fg'] = 'red'
                    self.window.label_message['text'] = "Invalid expiration date."
                    return False
                if (expiration_year_new < current_date.year) or (expiration_year_new == current_date.year and
                                                                 expiration_month < current_date.month):
                    self.window.label_message['fg'] = 'red'
                    self.window.label_message['text'] = "Credit card is expired."
                    return False
            if not re.match(r'^\d{3,4}$', cvv):
                self.window.label_message['fg'] = 'red'
                self.window.label_message['text'] = "Invalid CVV code."
                return False

            if not self.payment_check_testing(card, expiration_month, expiration_year, cvv):
                return False

            return True

        except ValueError:
            self.window.label_message['fg'] = 'red'
            self.window.label_message['text'] = "Invalid payment information."
            return False

    def payment_check_testing(self, card, month, year, cvv):
        stripe.api_key = stripe_key
        amount = 499

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='eur',
            payment_method_types=['card'],
        )

        try:
            payment_intent.confirm(
                payment_method='pm_card_mastercard',
            )

            if payment_intent.status == 'succeeded':
                self.window.label_message['fg'] = '#296108'
                self.window.label_message['text'] = "Payment successful!"
                return True
            else:
                self.window.label_message['fg'] = 'red'
                self.window.label_message['text'] = "Payment failed. Please try again."
                return False

        except stripe.error.StripeError as e:
            self.window.label_message['fg'] = 'red'
            self.window.label_message['text'] = f"Payment failed: {e}"
            return False

    def countdown(self, time_left):
        self.window.label_message['fg'] = '#296108'
        if time_left > 0:
            self.window.label_message['text'] = f"Action successful! Closing in {time_left}..."
            self.window.after(1000, self.countdown, time_left - 1)
        else:
            self.window.destroy()
