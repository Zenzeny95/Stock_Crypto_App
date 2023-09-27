"""
This Python file defines a pop-up window for upgrading to a premium subscription using the tkinter library.
 The key components of this code include:

1. Importing necessary modules such as 'tkinter' for creating the GUI, 'model' for database models,
 and 'app_payment_checks' for payment-related checks.

2. Defining a `PopupWindowUpgrade` class that represents a pop-up window for upgrading to a premium subscription:
   - Initializes a pop-up window with a specified title.
   - Creates a GUI with labels, entry fields for user information
    (username, full name, billing address, credit card details), and buttons for upgrading and closing the window.
   - Allows users to enter their information and subscribe to a premium service.
   - Validates user inputs, handling cases where inputs are missing or invalid.
   - Updates the user's subscription status in the database and stores credit card information
    if the subscription is successful.
   - Displays messages to inform the user about the status of their subscription.

3. The code utilizes external classes and methods (e.g., `PaymentChecks`) to perform payment-related checks
 and database operations.

4. The pop-up window's functionality includes error handling for scenarios where the user is not found,
 the user already has a subscription, or there are issues with the payment information.

5. The pop-up window is displayed in a centered position on the screen and is not resizable.

6. Users can upgrade to a premium subscription by providing their information and making a payment.

This code provides a user-friendly interface for upgrading to a premium subscription
 and handles the associated database operations and payment checks.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
from model import *
from app_payment_checks import PaymentChecks
from app_invoice import Invoices
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)


class PopupWindowUpgrade(tk.Toplevel):
    def __init__(self, master, title, username):
        super().__init__(master)
        self.title(title)
        self.label = tk.Label(self, font=("Helvetica", 16))
        self.label.pack(padx=20, pady=40)
        width = 600
        height = 600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.font_label = tk.font.Font(family="Helvetica", size=18)
        self.payment = PaymentChecks(master=self)
        self.username = username

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/600x600background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self, text='Upgrade to PREMIUM for 4.99 Eur/month', anchor="n", justify="center",
                                      font=self.font_label, bg='SystemButtonFace', highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=70, y=40, width=472, height=40)

        # ENTRIES
        self.entry_username_var = tk.StringVar()
        self.entry_username_var.set("Username")
        self.entry_username = tk.Entry(self, textvariable=self.entry_username_var, font=self.font, borderwidth="1px",
                                       fg="#ffffff", justify="center", bg="grey")
        self.entry_username.place(x=190, y=130, width=200, height=40)

        self.entry_fname_var = tk.StringVar()
        self.entry_fname_var.set("Full name")
        self.entry_fname = tk.Entry(self, textvariable=self.entry_fname_var, font=self.font, borderwidth="1px",
                                    fg="#ffffff", justify="center", bg="grey")
        self.entry_fname.place(x=190, y=180, width=200, height=40)

        self.entry_address_var = tk.StringVar()
        self.entry_address_var.set("Billing Address")
        self.entry_address = tk.Entry(self, textvariable=self.entry_address_var, font=self.font, borderwidth="1px",
                                      fg="#ffffff", justify="center", bg="grey")
        self.entry_address.place(x=190, y=230, width=200, height=40)

        self.entry_expire_var = tk.StringVar()
        self.entry_expire_var.set("Expire")
        self.entry_expire = tk.Entry(self, textvariable=self.entry_expire_var, font=self.font, borderwidth="1px",
                                     fg="#ffffff", justify="center", bg="grey")
        self.entry_expire.place(x=190, y=280, width=200, height=40)

        self.entry_code_var = tk.StringVar()
        self.entry_code_var.set("Security Code")
        self.entry_code = tk.Entry(self, textvariable=self.entry_code_var, font=self.font, borderwidth="1px",
                                   fg="#ffffff", justify="center", bg="grey")
        self.entry_code.place(x=190, y=330, width=200, height=40)

        self.entry_card_var = tk.StringVar()
        self.entry_card_var.set("Card Number")
        self.entry_card = tk.Entry(self, textvariable=self.entry_card_var, font=self.font, borderwidth="1px",
                                   fg="#ffffff", justify="center", bg="grey")
        self.entry_card.place(x=90, y=380, width=400, height=40)

        # BINDS
        self.entry_username.bind("<FocusIn>", self.on_entry_focus_in_username)
        self.entry_username.bind("<FocusOut>", self.on_entry_focus_out_username)
        self.entry_card.bind("<FocusIn>", self.on_entry_focus_in_card)
        self.entry_card.bind("<FocusOut>", self.on_entry_focus_out_card)
        self.entry_expire.bind("<FocusIn>", self.on_entry_focus_in_expire)
        self.entry_expire.bind("<FocusOut>", self.on_entry_focus_out_expire)
        self.entry_code.bind("<FocusIn>", self.on_entry_focus_in_code)
        self.entry_code.bind("<FocusOut>", self.on_entry_focus_out_code)
        self.entry_code.bind("<KeyRelease>", self.on_code_key_release)
        self.entry_fname.bind("<FocusIn>", self.on_entry_focus_in_fname)
        self.entry_fname.bind("<FocusOut>", self.on_entry_focus_out_fname)
        self.entry_address.bind("<FocusIn>", self.on_entry_focus_in_address)
        self.entry_address.bind("<FocusOut>", self.on_entry_focus_out_address)

        # BUTTONS
        subscribe_button = MacButton(self, text="Upgrade", font=self.font, justify="center", command=self.subscribe)
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        subscribe_button.place(x=190, y=460, width=200, height=50)
        close_button.place(x=190, y=520, width=200, height=50)

    def on_code_key_release(self, event):
        if self.entry_code_var.get():
            self.entry_code.config(show='*')
        else:
            self.entry_code.config(show='')

    def on_entry_focus_in_username(self, event):
        if self.entry_username_var.get() == "Username":
            self.entry_username_var.set("")

    def on_entry_focus_out_username(self, event):
        if not self.entry_username_var.get():
            self.entry_username_var.set("Username")

    def on_entry_focus_in_card(self, event):
        if self.entry_card_var.get() == "Card Number":
            self.entry_card_var.set("")

    def on_entry_focus_out_card(self, event):
        if not self.entry_card_var.get():
            self.entry_card_var.set("Card Number")

    def on_entry_focus_in_expire(self, event):
        if self.entry_expire_var.get() == "Expire":
            self.entry_expire_var.set("")

    def on_entry_focus_out_expire(self, event):
        if not self.entry_expire_var.get():
            self.entry_expire_var.set("Expire")

    def on_entry_focus_in_code(self, event):
        if self.entry_code_var.get() == "Security Code":
            self.entry_code_var.set("")
            self.entry_code.delete(0, tk.END)

    def on_entry_focus_out_code(self, event):
        if not self.entry_code_var.get():
            self.entry_code_var.set("Security Code")
            self.entry_code.config(show='')
        else:
            self.entry_code.config(show='*')

    def on_entry_focus_in_fname(self, event):
        if self.entry_fname_var.get() == "Full name":
            self.entry_fname_var.set("")

    def on_entry_focus_out_fname(self, event):
        if not self.entry_fname_var.get():
            self.entry_fname_var.set("Full name")

    def on_entry_focus_in_address(self, event):
        if self.entry_address_var.get() == "Billing Address":
            self.entry_address_var.set("")

    def on_entry_focus_out_address(self, event):
        if not self.entry_address_var.get():
            self.entry_address_var.set("Billing Address")

    def update_subscription(self):
        username = self.entry_username_var.get()
        if username == self.username:
            self.user = self.session.query(User).filter_by(username=username).first()
            if self.user:
                user_subscription = self.session.query(Subscription).filter_by(user_id=self.user.id).first()
                if user_subscription:
                    if user_subscription.payment is True:
                        self.label_message['fg'] = 'red'
                        self.label_message['text'] = f'User {username} already has subscription.'
                        return False
                    else:
                        user_subscription.payment = True
                        user_subscription.date = datetime.utcnow()
                        self.label_message['fg'] = '#296108'
                        self.label_message['text'] = f'Subscription updated for user: {username}'
                        return True
                else:
                    self.label_message['fg'] = 'red'
                    self.label_message['text'] = f'No subscription found for user: {username}'
                    return False
            else:
                self.label_message['fg'] = 'red'
                self.label_message['text'] = f'User not found: {username}'
                return False
        else:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = f'Incorrect Username: {username}'
            return False

    def subscribe(self):
        if self.payment.upgrade_check():
            card = self.entry_card_var.get()
            expire = self.entry_expire_var.get()
            code = self.entry_code_var.get()
            fname = self.entry_fname_var.get()
            address = self.entry_address_var.get()

            self.session = Session()

            if self.update_subscription() is False:
                return

            credit_card = CreditCard()
            credit_card.user_id = self.user.id
            credit_card.set_credit_card_info(card, expire, code, fname, address)
            self.session.add(credit_card)
            self.session.commit()

            self.invoice = Invoices(self.username)
            self.invoice.invoice()

            self.after(1000, self.payment.countdown, 3)
        else:
            return
