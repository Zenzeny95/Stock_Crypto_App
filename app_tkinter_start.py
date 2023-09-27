"""
This Python file defines a finance application with a graphical user interface (GUI) using the tkinter library.
The finance app allows users to perform various financial activities, including login, registration,
accessing stock and cryptocurrency information, and upgrading to a premium subscription.
The main components of this code include:

1. Importing necessary modules such as 'bcrypt' for password hashing, 'tkinter' for creating the GUI,
'tkmacosx.Button' for macOS-specific buttons, and various other modules for database interaction and pop-up windows.

2. Creating a `FinanceApp` class that represents the main application window:
   - Initializes the GUI window with a login frame and handles the main event loop.

3. Creating a `LoginFrame` class that represents the login page within the app:
   - Implements the login GUI, including labels, entry fields, and buttons.
   - Handles user input validation and login attempts, opening registration and password recovery windows as needed.

4. Creating a `MainFrame` class that represents the main dashboard of the app:
   - Displays a welcome message with the user's name and provides options to access different app functionalities.
   - Handles opening various pop-up windows for stocks, cryptocurrencies, financial methods,
    and premium subscription upgrades.

5. Creating an `AdminFrame` class to access an admin console:
   - Provides admin-specific functionality, such as database overview, statistics, and more.

6. The code utilizes bcrypt for secure password checking and SQLAlchemy for database interactions,
   including user authentication and subscription tracking.

7. The app provides clear entry field placeholders and input validation for user-friendliness.

8. The main application is launched in the `__main__` block by creating an instance of the `FinanceApp` class.

This code serves as a foundation for a finance application with user authentication and various financial
functionalities, providing users with a convenient way to manage their financial activities.
"""

import bcrypt
from datetime import datetime, timedelta
import uuid
import tkinter as tk
from tkinter import ttk, font as tkFont
from tkmacosx import Button as MacButton
from model import engine, User, Subscription, Password
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from app_payment_checks import PaymentChecks
from app_tkinter_stock import PopupWindowStock
from app_tkinter_crypto import PopupWindowCrypto
from app_tkinter_methods import PopupWindowMethods
from app_tkinter_premium import PopupWindowPremium
from app_admin_database import PopupWindowDatabase
from app_tkinter_registration import Registration
from app_tkinter_recovery import Recovery
from app_invoice import Invoices

Session = sessionmaker(bind=engine)


class FinanceApp(tk.Tk):
    def __init__(self):
        # Pagrindas
        super().__init__()
        self.title('Finance App')
        height = 600
        width = 700
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.minsize(width, height)
        #######################
        self.check_admin_user()
        ########################
        login_frame = LoginFrame(self)
        login_frame.place(x=0, y=0, relwidth=1, relheight=1)
        ########################
        self.mainloop()
        self.renew_subscriptions()

    @staticmethod
    def check_admin_user():
        session = Session()
        admin_user = session.query(User).filter_by(username="admin").first()
        if not admin_user:
            admin_password = "Intel123*"
            admin = User(id=str(uuid.uuid4()), name="Admin", username="admin", email="admin@example.com",
                         dob="1970-01-01")
            admin_password_entry = Password()
            admin_password_entry.userpass = admin
            admin_password_entry.set_password(admin_password)

            session.add(admin)
            session.commit()

        session.close()

    def renew_subscriptions(self):
        session = Session()

        today = datetime.utcnow()
        one_month_ago = today - timedelta(days=30)

        users_to_renew = session.query(User).filter(
            and_(
                User.subscription.any(Subscription.payment is True),
                User.subscription.any(Subscription.date <= one_month_ago)
            )
        ).all()

        try:
            for user in users_to_renew:
                if user.creditcards:
                    credit_card = user.creditcards[0]
                    number, expiry_date, cvv, name, address = credit_card.get_credit_card_info()
                    month, year = expiry_date.split("/")
                    payment_check = PaymentChecks(master=self)
                    if payment_check.payment_check_testing(number, month.strip(), year.strip(), cvv):
                        user.subscription[0].payment = True
                        user.subscription[0].date = today
                        self.invoice = Invoices(user.username)
                        self.invoice.invoice()
                    else:
                        user.subscription[0].payment = False
                        user.subscription[0].date = None
                else:
                    user.subscription[0].payment = False
                    user.subscription[0].date = None
                session.commit()
                session.close()
        except (KeyError, TypeError):
            print("NOT WORKING")

        self.after(24 * 60 * 60 * 1000, self.renew_subscriptions)


class LoginFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # BACKGROUND
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.background_image = tk.PhotoImage(file="background/Background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        label_font = tkFont.Font(family='Kumar One', size=40)
        label_font2 = tkFont.Font(family="Helvetica", size=18)
        label_name = tk.Label(self, text='Stock & Crypto App', font=label_font, anchor="n", justify="center",
                              bg='SystemButtonFace', highlightthickness=0, fg="#000000")
        self.label_message = tk.Label(self, text='', font=label_font2, anchor="n", justify="center",
                                      bg='SystemButtonFace', highlightthickness=0, fg="#000000")
        label_name.place(x=50, y=15, width=599, height=64)
        self.label_message.place(x=120, y=100, width=445, height=32)

        # ENTRY
        self.entry_var_name = tk.StringVar()
        self.entry_var_pass = tk.StringVar()
        self.entry_var_name.set("Enter Your Username")
        self.entry_var_pass.set("Enter Your Password")
        self.entry_name = tk.Entry(self, textvariable=self.entry_var_name, font=self.font, borderwidth="1px",
                                   fg="#ffffff", justify="center", bg="grey")
        self.entry_pass = tk.Entry(self, textvariable=self.entry_var_pass, font=self.font, borderwidth="1px",
                                   fg="#ffffff", justify="center", bg="grey")
        self.entry_name.place(x=100, y=180, width=220, height=40)
        self.entry_pass.place(x=380, y=180, width=220, height=40)

        # ENTRY BINDS
        self.entry_name.bind("<FocusIn>", self.on_entry_focus_in1)
        self.entry_name.bind("<FocusOut>", self.on_entry_focus_out1)
        self.entry_pass.bind("<FocusIn>", self.on_entry_focus_in2)
        self.entry_pass.bind("<FocusOut>", self.on_entry_focus_out2)
        self.entry_pass.bind("<KeyRelease>", self.on_password_key_release)

        # BUTTONS
        button_font = tk.font.Font(family="Helvetica", size=16)
        login_button = MacButton(self, text='Login', justify="center", font=button_font,
                                 overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.check_login)
        register_button = MacButton(self, text='Register', justify="center", font=button_font,
                                    overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.registration)
        recovery_button = MacButton(self, text='Forgot Password', justify="center", font=button_font,
                                    overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.recovery)
        exit_button = MacButton(self, text='Exit', justify="center", font=button_font,
                                overrelief=tk.SUNKEN, relief=tk.RAISED, command=exit)
        login_button.place(x=250, y=250, width=190, height=55)
        register_button.place(x=250, y=390, width=190, height=55)
        recovery_button.place(x=250, y=460, width=190, height=55)
        exit_button.place(x=250, y=530, width=190, height=55)

    def on_entry_focus_in1(self, event):
        if self.entry_var_name.get() == "Enter Your Username":
            self.entry_var_name.set("")

    def on_entry_focus_out1(self, event):
        if not self.entry_var_name.get():
            self.entry_var_name.set("Enter Your Username")

    def on_entry_focus_in2(self, event):
        if self.entry_var_pass.get() == "Enter Your Password":
            self.entry_pass.config(show="")
            self.entry_var_pass.set("")
            self.entry_pass.delete(0, tk.END)

    def on_entry_focus_out2(self, event):
        if not self.entry_var_pass.get():
            self.entry_var_pass.set("Enter Your Password")
            self.entry_pass.config(show='')
        else:
            self.entry_pass.config(show='*')

    def on_password_key_release(self, event):
        if self.entry_var_pass.get():
            self.entry_pass.config(show='*')
        else:
            self.entry_pass.config(show='')

    def check_login(self):
        session = Session()
        username = self.entry_var_name.get()
        password = self.entry_var_pass.get()

        if username == 'admin':
            admin = session.query(User).filter_by(username='admin').first()
            if admin:
                admin_password = session.query(Password).filter_by(user_id=admin.id).first()
                if admin_password and admin_password.verify_password(password=password):
                    admin_frame = AdminFrame(self)
                    admin_frame.place(x=0, y=0, relwidth=1, relheight=1)
                    return

        user = session.query(User).filter_by(username=username).first()

        if user:
            for user_password in user.password:
                if bcrypt.checkpw(password.encode('utf-8'), user_password.hash_password.encode('utf-8')):
                    subscription = session.query(Subscription.payment).filter_by(user_id=user.id).first()
                    username = session.query(User.username).filter_by(id=user.id).first()
                    main_frame = MainFrame(self, subscription, username)
                    main_frame.place(x=0, y=0, relwidth=1, relheight=1)
                    return

        self.label_message.config(text="Invalid username or password", fg="red")

    def registration(self):
        Registration(self, "Register")

    def recovery(self):
        Recovery(self, 'Password Recovery')


class MainFrame(ttk.Frame):
    def __init__(self, master, user_type, username):
        super().__init__(master)
        self.type = user_type[0]
        self.username = username[0]

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/Background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        label_font = tkFont.Font(family='Kumar One', size=40)
        label = tk.Label(self, text=f'Welcome, {self.username}!', font=label_font, anchor="n", justify="center",
                         bg='SystemButtonFace', highlightthickness=0, fg="#000000")
        label.place(x=50, y=10, width=599, height=64)
        if self.type is False:
            label_font_info = tkFont.Font(family='Kumar One', size=18)
            label = tk.Label(self, text=f'To access all functions upgrade to Premium', font=label_font_info,
                             anchor="n", justify="center", bg='SystemButtonFace', highlightthickness=0, fg="#0E82D3")
            label.place(x=50, y=75, width=599, height=40)

        # BUTTONS
        button_font = tk.font.Font(family="Helvetica", size=16)
        stocks_button = MacButton(self, text='Stocks', justify="center", font=button_font,
                                  overrelief=tk.SUNKEN, relief=tk.RAISED,
                                  command=self.open_stocks_popup)
        crypto_button = MacButton(self, text='Crypto', justify="center", font=button_font,
                                  overrelief=tk.SUNKEN, relief=tk.RAISED,
                                  command=self.open_crypto_popup)
        analyse_button = MacButton(self, text='Methods', justify="center", font=button_font,
                                   overrelief=tk.SUNKEN, relief=tk.RAISED,
                                   command=self.open_methods_popup)
        upgrade_button = MacButton(self, text='Premium', justify="center", font=button_font,
                                   overrelief=tk.SUNKEN, relief=tk.RAISED,
                                   command=self.open_premium_popup)
        loggout_button = MacButton(self, text='Log Out', justify="center", font=button_font,
                                   overrelief=tk.SUNKEN, relief=tk.RAISED,
                                   command=self.log_out)
        exit_button = MacButton(self, text='Exit', justify="center", font=button_font,
                                overrelief=tk.SUNKEN, relief=tk.RAISED, command=exit)
        stocks_button.place(x=250, y=140, width=190, height=55)
        crypto_button.place(x=250, y=210, width=190, height=55)
        analyse_button.place(x=250, y=280, width=190, height=55)
        upgrade_button.place(x=250, y=350, width=190, height=55)
        loggout_button.place(x=250, y=460, width=190, height=55)
        exit_button.place(x=250, y=530, width=190, height=55)

    def open_stocks_popup(self):
        self.close_all_popups()
        self.stocks_popup = PopupWindowStock(self.master, "Stocks", self.type)

    def open_crypto_popup(self):
        self.close_all_popups()
        self.crypto_popup = PopupWindowCrypto(self.master, "Crypto")

    def open_methods_popup(self):
        self.close_all_popups()
        self.methods_popup = PopupWindowMethods(self.master, "Methods", self.type, self.username)

    def open_premium_popup(self):
        self.close_all_popups()
        self.premium_popup = PopupWindowPremium(self.master, "Premium", self.username)

    def log_out(self):
        self.destroy()
        login_frame = LoginFrame(self.master)
        login_frame.place(x=0, y=0, relwidth=1, relheight=1)

    def close_all_popups(self):
        if hasattr(self, "stocks_popup") and self.stocks_popup.winfo_exists():
            self.stocks_popup.destroy()
        if hasattr(self, "crypto_popup") and self.crypto_popup.winfo_exists():
            self.crypto_popup.destroy()
        if hasattr(self, "methods_popup") and self.methods_popup.winfo_exists():
            self.methods_popup.destroy()
        if hasattr(self, "premium_popup") and self.premium_popup.winfo_exists():
            self.premium_popup.destroy()


class AdminFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/Background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        label_font = tkFont.Font(family='Kumar One', size=40)
        label = tk.Label(self, text=f'Admin Console', font=label_font, anchor="n", justify="center",
                         bg='SystemButtonFace', highlightthickness=0, fg="#000000")
        label.place(x=50, y=10, width=599, height=64)

        # BUTTONS
        button_font = tk.font.Font(family="Helvetica", size=16)
        database_button = MacButton(self, text='Database', justify="center", font=button_font,
                                    overrelief=tk.SUNKEN, relief=tk.RAISED,
                                    command=self.open_database_popup)
        loggout_button = MacButton(self, text='Log Out', justify="center", font=button_font,
                                   overrelief=tk.SUNKEN, relief=tk.RAISED,
                                   command=self.log_out)
        exit_button = MacButton(self, text='Exit', justify="center", font=button_font,
                                overrelief=tk.SUNKEN, relief=tk.RAISED, command=exit)
        database_button.place(x=250, y=210, width=190, height=55)
        loggout_button.place(x=250, y=440, width=190, height=55)
        exit_button.place(x=250, y=510, width=190, height=55)

    def open_database_popup(self):
        self.database_popup = PopupWindowDatabase(self.master, "Database")

    def log_out(self):
        self.destroy()
        login_frame = LoginFrame(self.master)
        login_frame.place(x=0, y=0, relwidth=1, relheight=1)


if __name__ == "__main__":
    FinanceApp()
