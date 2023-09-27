"""
The 'AlertPopupWindow' class represents a Tkinter popup window for configuring price alert notifications.

Class Methods:
- '__init__(self, master, title, username)': Initializes a new 'AlertPopupWindow' instance.
    - 'master': The master Tkinter window to which this popup is associated.
    - 'title': The title of the popup window.
    - 'username': The username of the current user.

Methods:
- 'submited_data(self)': Validates and processes user-submitted data for setting up price alerts.

Note:
- This class represents a Tkinter popup window for configuring price alert notifications.
- It includes methods for handling user interactions, such as focus events and data submission.
- The user can configure alerts for stock or crypto based on their inputs.
- The alert status is displayed in the label within the popup window.
- Data validation is performed to ensure the entered values are valid for alert setup.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
from sqlalchemy.orm import sessionmaker
from model import engine, User
from app_methods_price_alert import AlertSystem

Session = sessionmaker(bind=engine)
session = Session()


class AlertPopupWindow(tk.Toplevel):
    def __init__(self, master, title, username):
        super().__init__(master)
        self.title(title)
        width = 600
        height = 350
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.font_label = tk.font.Font(family="Helvetica", size=18)
        self.default_crypto = 'Crypto Abbreviation'
        self.default_stock = 'Stock Abbreviation'
        self.username = username

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/800x350background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # BUTTONS
        submit_button = MacButton(self, font=self.font, justify='center', text='Submit', command=self.submited_data)
        close_button = MacButton(self, font=self.font, justify='center', text='Close Window', command=self.destroy)
        submit_button.place(x=210, y=210, width=176, height=50)
        close_button.place(x=210, y=270, width=176, height=50)

        # ENTRIES
        self.entry_target_var = tk.StringVar()
        self.entry_target_var.set('Target Value')
        self.entry_target = tk.Entry(self, textvariable=self.entry_target_var, borderwidth='1px', font=self.font,
                                     justify='center', bg='grey')
        self.entry_target.place(x=170, y=60, width=247, height=40)

        self.entry_stock_var = tk.StringVar()
        self.entry_stock_var.set('Stock Abbreviation')
        self.entry_stock = tk.Entry(self, textvariable=self.entry_stock_var, borderwidth='1px', font=self.font,
                                    justify='center', bg='grey')
        self.entry_stock.place(x=30, y=120, width=247, height=40)

        self.entry_crypto_var = tk.StringVar()
        self.entry_crypto_var.set('Crypto Abbreviation')
        self.entry_crypto = tk.Entry(self, textvariable=self.entry_crypto_var, borderwidth='1px', font=self.font,
                                     justify='center', bg='grey')
        self.entry_crypto.place(x=310, y=120, width=247, height=40)

        # LABEL
        self.label = tk.Label(self, font=self.font_label, justify='center', text='Activate Price Alert',
                              bg='#F7F7F7', fg='#0E82D3')
        self.label.place(x=100, y=10, width=400, height=32)

        # BINDS
        self.entry_target.bind("<FocusIn>", self.on_entry_focus_in_target)
        self.entry_target.bind("<FocusOut>", self.on_entry_focus_out_target)
        self.entry_stock.bind("<FocusIn>", self.on_entry_focus_in_stock)
        self.entry_stock.bind("<FocusOut>", self.on_entry_focus_out_stock)
        self.entry_crypto.bind("<FocusIn>", self.on_entry_focus_in_crypto)
        self.entry_crypto.bind("<FocusOut>", self.on_entry_focus_out_crypto)
        self.entry_stock.bind("<Key>", self.on_entry_key_stock)
        self.entry_crypto.bind("<Key>", self.on_entry_key_crypto)
        self.entry_stock.bind("<FocusOut>", self.on_entry_focus_out_st)
        self.entry_crypto.bind("<FocusOut>", self.on_entry_focus_out_cr)

    def on_entry_focus_in_crypto(self, event):
        if self.entry_crypto_var.get() == 'Crypto Abbreviation':
            self.entry_crypto_var.set('')

    def on_entry_focus_out_crypto(self, event):
        if not self.entry_crypto_var.get():
            self.entry_crypto_var.set('Crypto Abbreviation')

    def on_entry_focus_in_target(self, event):
        if self.entry_target_var.get() == 'Target Value':
            self.entry_target_var.set('')

    def on_entry_focus_out_target(self, event):
        if not self.entry_target_var.get():
            self.entry_target_var.set('Target Value')

    def on_entry_focus_in_stock(self, event):
        if self.entry_stock_var.get() == 'Stock Abbreviation':
            self.entry_stock_var.set('')

    def on_entry_focus_out_stock(self, event):
        if not self.entry_stock_var.get():
            self.entry_stock_var.set('Stock Abbreviation')

    def on_entry_key_stock(self, event):
        self.entry_crypto.config(state="disabled")

    def on_entry_focus_out_st(self, event):
        if not self.entry_stock.get():
            self.entry_stock.delete(0, "end")
            self.entry_stock.insert(0, self.default_stock)
        if self.entry_stock_var.get() == self.default_stock:
            self.entry_crypto.config(state="normal")

    def on_entry_key_crypto(self, event):
        self.entry_stock.config(state="disabled")

    def on_entry_focus_out_cr(self, event):
        if not self.entry_crypto.get():
            self.entry_crypto.delete(0, "end")
            self.entry_crypto.insert(0, self.default_crypto)
        if self.entry_crypto_var.get() == self.default_crypto:
            self.entry_stock.config(state="normal")

    def submited_data(self):
        try:
            email = session.query(User.email).filter_by(username=self.username).first()
            name = session.query(User.name).filter_by(username=self.username).first()
            target = float(self.entry_target_var.get().strip())
            if self.entry_target_var.get() == 'Targel Value' or self.entry_target_var.get() == " " or target < 0:
                raise ValueError
            stock = self.entry_stock_var.get().strip().upper()
            crypto = self.entry_crypto_var.get().strip().upper()
            if (crypto == self.default_crypto or crypto == "") and (stock == self.default_stock or stock == ""):
                raise ValueError
            if crypto == self.default_crypto.upper() or crypto == "":
                alert = AlertSystem(email=email[0], price=target, stock=stock, name=name[0])
                alert.alert()
            if stock == self.default_stock.upper() or stock == "":
                alert = AlertSystem(email=email[0], price=target, crypto=crypto, name=name[0])
                alert.alert()
            self.label['fg'] = '#296108'
            self.label['text'] = "Alert is Turned ON"
        except (ValueError, IndexError, AttributeError):
            self.label['fg'] = 'red'
            self.label['text'] = "Alert NOT Turned ON"
