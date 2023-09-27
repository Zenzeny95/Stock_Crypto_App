"""
PopupWindowDatabase - Database Selection Window

This class defines a pop-up window for selecting a database category (Users, Subscriptions, Invoices)
within an application's admin interface.

Methods:
    __init__(self, master, title):
        Initializes the pop-up window with a specified title and UI elements.

    open_user_popup(self):
        Opens a pop-up window for managing user data.

    open_subscription_popup(self):
        Opens a pop-up window for managing subscription data.

    open_invoice_popup(self):
        Placeholder for opening a pop-up window for managing invoice data.

    close_all_popups(self):
        Closes any open pop-up windows associated with this instance.
"""

import tkinter as tk
from tkinter import font as tkFont
from tkmacosx import Button as MacButton
from app_admin_database_users import PopupWindowUsers
from app_admin_database_subscriptions import PopupWindowSubscriptions
from app_admin_database_invoices import PopupWindowInvoices


class PopupWindowDatabase(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        width = 600
        height = 600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/600x600background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        label_font = tkFont.Font(family='Kumar One', size=40)
        label = tk.Label(self, text=f'Select A Database', font=label_font, anchor="n", justify="center",
                         bg='SystemButtonFace', highlightthickness=0, fg="#000000")
        label.place(x=110, y=50, width=400, height=64)

        # BUTTONS
        button_font = tk.font.Font(family="Helvetica", size=16)
        user_button = MacButton(self, text='Users', justify="center", font=button_font,
                                overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.open_user_popup)
        subscription_button = MacButton(self, text='Subscriptions', justify="center", font=button_font,
                                        overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.open_subscription_popup)
        invoice_button = MacButton(self, text='Invoices', justify="center", font=button_font,
                                   overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.open_invoice_popup)
        close_button = MacButton(self, text='Close Window', justify="center", font=button_font,
                                 overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.destroy)
        user_button.place(x=200, y=180, width=190, height=55)
        subscription_button.place(x=200, y=250, width=190, height=55)
        invoice_button.place(x=200, y=320, width=190, height=55)
        close_button.place(x=200, y=490, width=190, height=55)

    def open_user_popup(self):
        self.close_all_popups()
        self.user_popup = PopupWindowUsers(self.master, "Users")

    def open_subscription_popup(self):
        self.close_all_popups()
        self.subscription_popup = PopupWindowSubscriptions(self.master, "Subscription")

    def open_invoice_popup(self):
        self.close_all_popups()
        self.invoice_popup = PopupWindowInvoices(self.master, "Invoices")

    def close_all_popups(self):
        if hasattr(self, "user_popup") and self.user_popup.winfo_exists():
            self.user_popup.destroy()
        if hasattr(self, "subscription_popup") and self.subscription_popup.winfo_exists():
            self.subscription_popup.destroy()
        if hasattr(self, "invoice_popup") and self.invoice_popup.winfo_exists():
            self.invoice_popup.destroy()
