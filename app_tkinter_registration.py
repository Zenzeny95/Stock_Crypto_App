"""
This Python file defines a user registration form in a graphical user interface (GUI) application using tkinter.
 The registration form allows users to sign up with their personal information and, optionally, upgrade to
a premium subscription with payment details. The main components of this code include:

1. Importing necessary modules such as 'uuid' for generating UUIDs, 're' for regular expressions, 'tkinter'
for creating the GUI, and 'tkmacosx.Button' for macOS-specific buttons.

2. Creating a SQLAlchemy `Session` object for database interaction.

3. Defining a `Registration` class that represents the registration form:
   - Initializes the GUI window and its components, including labels, entry fields, checkboxes, and buttons.
   - Handles various events like focusing in and out of entry fields.
   - Implements methods for input validation.
   - Allows users to optionally upgrade to a premium subscription, revealing additional payment-related entry fields.

4. There's a commented-out `payment_check` method that appears to be related to handling payments via Stripe,
but it's currently commented out.

This code is designed for user registration and input validation, offering users a simple way to sign up for
a service and choose a premium subscription if desired.
"""

import uuid
import re
import tkinter as tk
from tkmacosx import Button as MacButton
from model import *
from sqlalchemy.orm import sessionmaker
from app_payment_checks import PaymentChecks
from app_invoice import Invoices

Session = sessionmaker(bind=engine)


class Registration(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        width = 700
        height = 700
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.font_label = tk.font.Font(family="Helvetica", size=18)
        self.payment = PaymentChecks(master=self)

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/Background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self, text='Please fill in information below', anchor="n", justify="center",
                                      font=self.font_label, bg='SystemButtonFace', highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=110, y=40, width=472, height=40)

        # ENTRY
        self.entry_username_var = tk.StringVar()
        self.entry_username_var.set("Username")
        self.entry_username = tk.Entry(self, textvariable=self.entry_username_var, font=self.font, borderwidth="1px",
                                       fg="#ffffff", justify="center", bg="grey")
        self.entry_username.place(x=110, y=130, width=200, height=40)

        self.entry_email_var = tk.StringVar()
        self.entry_email_var.set("Email")
        self.entry_email = tk.Entry(self, textvariable=self.entry_email_var, font=self.font, borderwidth="1px",
                                    fg="#ffffff", justify="center", bg="grey")
        self.entry_email.place(x=380, y=130, width=200, height=40)

        self.entry_pass_var = tk.StringVar()
        self.entry_pass_var.set("Password")
        self.entry_pass = tk.Entry(self, textvariable=self.entry_pass_var, font=self.font, borderwidth="1px",
                                   fg="#ffffff", justify="center", bg="grey")
        self.entry_pass.place(x=110, y=190, width=200, height=40)

        self.entry_pass2_var = tk.StringVar()
        self.entry_pass2_var.set("Repeat Password")
        self.entry_pass2 = tk.Entry(self, textvariable=self.entry_pass2_var, font=self.font, borderwidth="1px",
                                    fg="#ffffff", justify="center", bg="grey")
        self.entry_pass2.place(x=380, y=190, width=200, height=40)

        self.entry_name_var = tk.StringVar()
        self.entry_name_var.set("Name")
        self.entry_name = tk.Entry(self, textvariable=self.entry_name_var, font=self.font, borderwidth="1px",
                                   fg="#ffffff", justify="center", bg="grey")
        self.entry_name.place(x=110, y=250, width=200, height=40)

        self.entry_dob_var = tk.StringVar()
        self.entry_dob_var.set("DOB (YYYY-MM-DD)")
        self.entry_dob = tk.Entry(self, textvariable=self.entry_dob_var, font=self.font, borderwidth="1px",
                                  fg="#ffffff", justify="center", bg="grey")
        self.entry_dob.place(x=380, y=250, width=200, height=40)

        # CHECKBOX
        self.upgrade_var = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(self, text="    Upgrade to PREMIUM for 4.99 Eur/month", font=self.font,
                                          variable=self.upgrade_var, bg='#F4F6F6', fg='#0E82D3', command=self.upgrade)
        self.checkbutton.place(x=240, y=340, width=320, height=30)

        # BUTTONS
        submit_button = MacButton(self, text="Submit", font=self.font, justify="center", command=self.submit)
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        submit_button.place(x=110, y=610, width=200, height=50)
        close_button.place(x=380, y=610, width=200, height=50)

        # BINDS
        self.entry_username.bind("<FocusIn>", self.on_entry_focus_in_username)
        self.entry_username.bind("<FocusOut>", self.on_entry_focus_out_username)
        self.entry_pass.bind("<FocusIn>", self.on_entry_focus_in_pass)
        self.entry_pass.bind("<FocusOut>", self.on_entry_focus_out_pass)
        self.entry_pass.bind("<KeyRelease>", self.on_password_key_release)
        self.entry_email.bind("<FocusIn>", self.on_entry_focus_in_email)
        self.entry_email.bind("<FocusOut>", self.on_entry_focus_out_email)
        self.entry_dob.bind("<FocusIn>", self.on_entry_focus_in_dob)
        self.entry_dob.bind("<FocusOut>", self.on_entry_focus_out_dob)
        self.entry_pass2.bind("<FocusIn>", self.on_entry_focus_in_pass2)
        self.entry_pass2.bind("<FocusOut>", self.on_entry_focus_out_pass2)
        self.entry_pass2.bind("<KeyRelease>", self.on_password_key_release2)
        self.entry_name.bind("<FocusIn>", self.on_entry_focus_in_name)
        self.entry_name.bind("<FocusOut>", self.on_entry_focus_out_name)

    def on_password_key_release(self, event):
        if self.entry_pass_var.get():
            self.entry_pass.config(show='*')
        else:
            self.entry_pass.config(show='')

    def on_password_key_release2(self, event):
        if self.entry_pass2_var.get():
            self.entry_pass2.config(show='*')
        else:
            self.entry_pass2.config(show='')

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

    def on_entry_focus_in_pass(self, event):
        if self.entry_pass_var.get() == "Password":
            self.entry_pass_var.set("")
            self.entry_pass.delete(0, tk.END)

    def on_entry_focus_out_pass(self, event):
        if not self.entry_pass_var.get():
            self.entry_pass_var.set("Password")
            self.entry_pass.config(show='')
        else:
            self.entry_pass.config(show='*')

    def on_entry_focus_in_email(self, event):
        if self.entry_email_var.get() == "Email":
            self.entry_email_var.set("")

    def on_entry_focus_out_email(self, event):
        if not self.entry_email_var.get():
            self.entry_email_var.set("Email")

    def on_entry_focus_in_pass2(self, event):
        if self.entry_pass2_var.get() == "Repeat Password":
            self.entry_pass2_var.set("")

    def on_entry_focus_out_pass2(self, event):
        if not self.entry_pass2_var.get():
            self.entry_pass2_var.set("Repeat Password")

    def on_entry_focus_in_dob(self, event):
        if self.entry_dob_var.get() == "DOB (YYYY-MM-DD)":
            self.entry_dob_var.set("")

    def on_entry_focus_out_dob(self, event):
        if not self.entry_dob_var.get():
            self.entry_dob_var.set("DOB (YYYY-MM-DD)")

    def on_entry_focus_in_name(self, event):
        if self.entry_name_var.get() == "Name":
            self.entry_name_var.set("")

    def on_entry_focus_out_name(self, event):
        if not self.entry_name_var.get():
            self.entry_name_var.set("Name")

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

    def upgrade(self):
        if self.upgrade_var.get():
            self.entry_card_var = tk.StringVar()
            self.entry_card_var.set("Card Number")
            self.entry_card = tk.Entry(self, textvariable=self.entry_card_var, font=self.font, borderwidth="1px",
                                       fg="#ffffff", justify="center", bg="grey")
            self.entry_card.place(x=110, y=390, width=472, height=38)

            self.entry_expire_var = tk.StringVar()
            self.entry_expire_var.set("Expire")
            self.entry_expire = tk.Entry(self, textvariable=self.entry_expire_var, font=self.font, borderwidth="1px",
                                         fg="#ffffff", justify="center", bg="grey")
            self.entry_expire.place(x=110, y=440, width=200, height=40)

            self.entry_code_var = tk.StringVar()
            self.entry_code_var.set("Security Code")
            self.entry_code = tk.Entry(self, textvariable=self.entry_code_var, font=self.font, borderwidth="1px",
                                       fg="#ffffff", justify="center", bg="grey")
            self.entry_code.place(x=380, y=440, width=200, height=40)

            self.entry_fname_var = tk.StringVar()
            self.entry_fname_var.set("Full name")
            self.entry_fname = tk.Entry(self, textvariable=self.entry_fname_var, font=self.font, borderwidth="1px",
                                        fg="#ffffff", justify="center", bg="grey")
            self.entry_fname.place(x=110, y=490, width=200, height=40)

            self.entry_address_var = tk.StringVar()
            self.entry_address_var.set("Billing Address")
            self.entry_address = tk.Entry(self, textvariable=self.entry_address_var, font=self.font, borderwidth="1px",
                                          fg="#ffffff", justify="center", bg="grey")
            self.entry_address.place(x=380, y=490, width=200, height=40)

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

        else:
            if hasattr(self, "entry_card"):
                self.entry_card.delete(0, tk.END)
                self.entry_card.place_forget()
            if hasattr(self, "entry_expire"):
                self.entry_expire.delete(0, tk.END)
                self.entry_expire.place_forget()
            if hasattr(self, "entry_code"):
                self.entry_code.delete(0, tk.END)
                self.entry_code.place_forget()
            if hasattr(self, "entry_fname"):
                self.entry_fname.delete(0, tk.END)
                self.entry_fname.place_forget()
            if hasattr(self, "entry_address"):
                self.entry_address.delete(0, tk.END)
                self.entry_address.place_forget()

    def submit(self):
        self.session = Session()
        password = self.entry_pass_var.get()
        password2 = self.entry_pass2_var.get()
        if password != password2:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = "Passwords do not match."
            return
        username = self.entry_username_var.get()
        email = self.entry_email_var.get()
        dob = self.entry_dob_var.get()
        name = self.entry_name_var.get()

        try:
            if re.match(r'\d{4}-\d{2}-\d{2}', dob):
                dob_date = datetime.strptime(dob, "%Y-%m-%d")
                age = (datetime.now() - dob_date).days // 365
                if age < 18:
                    self.label_message['fg'] = 'red'
                    self.label_message['text'] = "Age restriction. User is younger than 18yo."
                    return
            else:
                self.label_message['fg'] = 'red'
                self.label_message['text'] = "Required date format: YYYY-MM-DD."
                return
        except ValueError:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = "Required date format: YYYY-MM-DD."
        try:
            if len(password) < 8:
                self.label_message['fg'] = 'red'
                self.label_message['text'] = "Password has to have at least 8 characters."
                return
            if not re.search(r'[A-Z]', password):
                self.label_message['fg'] = 'red'
                self.label_message['text'] = "Password has to have at least 1 upper letter."
                return
            if not re.search(r'\d', password):
                self.label_message['fg'] = 'red'
                self.label_message['text'] = "Password has to have at least 1 digit."
                return
            if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\\-]', password):
                self.label_message['fg'] = 'red'
                self.label_message['text'] = "Password has to have at least 1 symbol."
                return
        except ValueError:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = "Invalid password input."
        try:
            if len(username) < 3:
                self.label_message['fg'] = 'red'
                self.label_message['text'] = "Username has to have at least 3 characters."
                return
            username_check = self.session.query(User).filter_by(username=username).first()
            if username_check:
                self.label_message['fg'] = 'red'
                self.label_message['text'] = "Such username already exists."
                return
        except ValueError:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = "Username error. Try different one."
        try:
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(pattern, email):
                email_check = self.session.query(User).filter_by(email=email).first()
                if email_check:
                    self.label_message['fg'] = 'red'
                    self.label_message['text'] = "This email address is already in use."
                    return
            else:
                self.label_message['fg'] = 'red'
                self.label_message['text'] = "Email address is not valid."
                return
        except ValueError:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = "Email error. Try different one."

        while True:
            new_uuid = str(uuid.uuid4())
            existing_user = self.session.query(User).filter_by(id=new_uuid).first()
            if not existing_user:
                break

        self.new_user = User(
            id=new_uuid,
            username=username,
            email=email,
            dob=dob,
            name=name,
        )
        self.session.add(self.new_user)

        user_password = Password(
            hash_password=password,
            userpass=self.new_user,
        )

        user_password.set_password(password)
        self.session.add(user_password)

        if not self.upgrade_var.get():
            user_subscription = Subscription(
                payment=False,
                usersubs=self.new_user,
            )

            self.session.add(user_subscription)
            self.session.commit()

        else:
            if self.payment.upgrade_check():
                card = self.entry_card_var.get()
                expire = self.entry_expire_var.get()
                cvv = self.entry_code_var.get()
                fname = self.entry_fname_var.get()
                address = self.entry_address_var.get()

                credit_card = CreditCard()
                credit_card.user_id = new_uuid
                credit_card.set_credit_card_info(card, expire, cvv, fname, address)
                self.session.add(credit_card)

                user_subscription = Subscription(
                    payment=True,
                    date=datetime.utcnow(),
                    user_id=self.new_user.id,
                )

                self.session.add(user_subscription)
                self.session.commit()

                self.invoice = Invoices(username)
                self.invoice.invoice()

            else:
                return

        self.after(1000, self.payment.countdown, 3)

    # def payment_check(self, card, month, year, cvv):
    #     stripe.api_key = stripe_key
    #     amount = 499

        # token = stripe.Token.create(
        #     card={
        #         "number": card,
        #         "exp_month": month,
        #         "exp_year": year,
        #         "cvc": cvv,
        #     }
        # )
        # try:
        # charge = stripe.Charge.create(
        #     amount=amount,
        #     currency='eur',
        #     payment_method='card',
        #     description='Premium',
        #     source=token.id
        # )
        #
        # if charge.status == 'succeeded':
        #     self.label_message['fg'] = '#296108'
        #     self.label_message['text'] = "Payment successful!"
        #     return True
        # else:
        #     self.label_message['fg'] = 'red'
        #     self.label_message['text'] = "Payment failed. Please try again."
        #     return False

        # except Exception:
        #     self.label_message['fg'] = 'red'
        #     self.label_message['text'] = "Payment failed. Please try again."
        #     return False
