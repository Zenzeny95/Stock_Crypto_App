"""
The 'Recovery' class represents a Tkinter-based password recovery window.

Class Methods:
- '__init__(self, master, title)': Initializes a new 'Recovery' instance.
    - 'master': The master Tkinter window to which this popup is associated.
    - 'title': The title of the recovery window.

Methods:
- 'code_entries(self)': Sets up the entry field and button for entering the verification code.
- 'pass_entries(self)': Sets up the entry fields and button for entering the new password.
- 'request_reset_password(self)': Handles the password reset request process.
- 'send_password_reset_email(self)': Sends a password reset email to the user.
- 'verify_code(self)': Verifies the provided verification code.
- 'submit(self)': Handles the submission of the new password.

Note:
- This class represents a Tkinter-based password recovery window.
- Users can request a password reset by providing their username, email, date of birth, and name.
- Users receive a verification code via email and use it to reset their password.
- Password reset is subject to specific requirements, including password strength.
"""

import smtplib
from email.message import EmailMessage
from emailo_config import *
from string import Template
from datetime import timedelta
import uuid
import re
import tkinter as tk
from tkmacosx import Button as MacButton
from model import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from app_payment_checks import PaymentChecks


Session = sessionmaker(bind=engine)
session = Session()


class Recovery(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        width = 700
        height = 750
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
        self.label_message = tk.Label(self, text='To change password please fill in information below.', anchor="n",
                                      justify="center", font=self.font_label, bg='SystemButtonFace',
                                      highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=110, y=30, width=472, height=40)

        # ENTRY
        self.entry_username_var = tk.StringVar()
        self.entry_username_var.set("Username")
        self.entry_username = tk.Entry(self, textvariable=self.entry_username_var, font=self.font, borderwidth="1px",
                                       fg="#ffffff", justify="center", bg="grey")
        self.entry_username.place(x=110, y=100, width=220, height=40)

        self.entry_email_var = tk.StringVar()
        self.entry_email_var.set("Email")
        self.entry_email = tk.Entry(self, textvariable=self.entry_email_var, font=self.font, borderwidth="1px",
                                    fg="#ffffff", justify="center", bg="grey")
        self.entry_email.place(x=380, y=100, width=220, height=40)

        self.entry_name_var = tk.StringVar()
        self.entry_name_var.set("Name")
        self.entry_name = tk.Entry(self, textvariable=self.entry_name_var, font=self.font, borderwidth="1px",
                                   fg="#ffffff", justify="center", bg="grey")
        self.entry_name.place(x=110, y=160, width=220, height=40)

        self.entry_dob_var = tk.StringVar()
        self.entry_dob_var.set("DOB (YYYY-MM-DD)")
        self.entry_dob = tk.Entry(self, textvariable=self.entry_dob_var, font=self.font, borderwidth="1px",
                                  fg="#ffffff", justify="center", bg="grey")
        self.entry_dob.place(x=380, y=160, width=220, height=40)

        # BUTTONS
        request_button = MacButton(self, text="Recover", font=self.font, justify="center",
                                   command=self.request_reset_password)
        request_button.place(x=240, y=230, width=200, height=50)
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        close_button.place(x=240, y=650, width=200, height=50)

        # BINDS
        self.entry_username.bind("<FocusIn>", self.on_entry_focus_in_username)
        self.entry_username.bind("<FocusOut>", self.on_entry_focus_out_username)
        self.entry_email.bind("<FocusIn>", self.on_entry_focus_in_email)
        self.entry_email.bind("<FocusOut>", self.on_entry_focus_out_email)
        self.entry_dob.bind("<FocusIn>", self.on_entry_focus_in_dob)
        self.entry_dob.bind("<FocusOut>", self.on_entry_focus_out_dob)
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

    def on_entry_focus_in_username(self, event):
        if self.entry_username_var.get() == "Username":
            self.entry_username_var.set("")

    def on_entry_focus_out_username(self, event):
        if not self.entry_username_var.get():
            self.entry_username_var.set("Username")

    def on_entry_focus_in_email(self, event):
        if self.entry_email_var.get() == "Email":
            self.entry_email_var.set("")

    def on_entry_focus_out_email(self, event):
        if not self.entry_email_var.get():
            self.entry_email_var.set("Email")

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

    def on_entry_focus_in_token(self, event):
        if self.entry_token_var.get() == "Enter Code":
            self.entry_token_var.set("")

    def on_entry_focus_out_token(self, event):
        if not self.entry_token_var.get():
            self.entry_token_var.set("Enter Code")

    def on_entry_focus_in_pass(self, event):
        if self.entry_pass_var.get() == "New Password":
            self.entry_pass_var.set("")
            self.entry_pass.delete(0, tk.END)

    def on_entry_focus_out_pass(self, event):
        if not self.entry_pass_var.get():
            self.entry_pass_var.set("New Password")
            self.entry_pass.config(show='')
        else:
            self.entry_pass.config(show='*')

    def on_entry_focus_in_pass2(self, event):
        if self.entry_pass2_var.get() == "Repeat New Password":
            self.entry_pass2_var.set("")

    def on_entry_focus_out_pass2(self, event):
        if not self.entry_pass2_var.get():
            self.entry_pass2_var.set("Repeat New Password")

    def code_entries(self):
        # ENTRY
        self.entry_token_var = tk.StringVar()
        self.entry_token_var.set("Enter Code")
        self.entry_token = tk.Entry(self, textvariable=self.entry_token_var, font=self.font, borderwidth="1px",
                                    fg="#ffffff", justify="center", bg="grey")
        self.entry_token.place(x=190, y=330, width=300, height=40)

        # BUTTON

        code_button = MacButton(self, text="Code", font=self.font, justify="center", command=self.verify_code)
        code_button.place(x=240, y=400, width=200, height=50)

        # BINDS

        self.entry_token.bind("<FocusIn>", self.on_entry_focus_in_token)
        self.entry_token.bind("<FocusOut>", self.on_entry_focus_out_token)

    def pass_entries(self):
        # ENTRY
        self.entry_pass_var = tk.StringVar()
        self.entry_pass_var.set("New Password")
        self.entry_pass = tk.Entry(self, textvariable=self.entry_pass_var, font=self.font, borderwidth="1px",
                                   fg="#ffffff", justify="center", bg="grey")
        self.entry_pass.place(x=120, y=510, width=200, height=40)

        self.entry_pass2_var = tk.StringVar()
        self.entry_pass2_var.set("Repeat New Password")
        self.entry_pass2 = tk.Entry(self, textvariable=self.entry_pass2_var, font=self.font, borderwidth="1px",
                                    fg="#ffffff", justify="center", bg="grey")
        self.entry_pass2.place(x=380, y=510, width=200, height=40)

        # BUTTON
        submit_button = MacButton(self, text="Submit", font=self.font, justify="center", command=self.submit)
        submit_button.place(x=240, y=580, width=200, height=50)

        # BINDS
        self.entry_pass.bind("<FocusIn>", self.on_entry_focus_in_pass)
        self.entry_pass.bind("<FocusOut>", self.on_entry_focus_out_pass)
        self.entry_pass.bind("<KeyRelease>", self.on_password_key_release)
        self.entry_pass2.bind("<FocusIn>", self.on_entry_focus_in_pass2)
        self.entry_pass2.bind("<FocusOut>", self.on_entry_focus_out_pass2)
        self.entry_pass2.bind("<KeyRelease>", self.on_password_key_release2)

    def request_reset_password(self):
        username = self.entry_username_var.get()
        email = self.entry_email_var.get()
        dob = self.entry_dob_var.get()
        name = self.entry_name_var.get()

        existing_user = session.query(User).filter(
            and_(
                User.username == username,
                User.email == email,
                User.dob == dob,
                User.name == name
            )
        ).first()

        if existing_user:

            existing_requests = session.query(PasswordResetRequest).filter_by(user_id=existing_user.id).all()
            for request in existing_requests:
                session.delete(request)

            while True:
                self.reset_token = str(uuid.uuid4())
                existing_code = session.query(PasswordResetRequest).filter_by(token=self.reset_token).first()
                if not existing_code:
                    break

            reset_request = PasswordResetRequest(user_id=existing_user.id, token=self.reset_token)
            session.add(reset_request)
            session.commit()

            self.send_password_reset_email()
            self.code_entries()
            return
        else:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = "User with provided information doesn't exist"
            return

    def send_password_reset_email(self):
        emailas = self.entry_email_var.get()
        email = EmailMessage()
        email["from"] = f"Stock & Crypto App <{EMAIL}>"
        email["to"] = emailas
        email["subject"] = "Password Reset"

        with open("templates/recovery.html", mode="r", encoding="utf-8") as f:
            html_text = f.read()

        changes = {
            "token": self.reset_token,
        }
        template = Template(html_text)
        html_text = template.substitute(changes)

        email.set_content(html_text, "html")

        with smtplib.SMTP(host=SMTP_HOST, port=PORT) as smtp_server:
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.login(EMAIL, PASSWORD)
            smtp_server.send_message(email)

        self.label_message['fg'] = '#296108'
        self.label_message['text'] = 'Reset email has been sent succuesfully'
        return

    def verify_code(self):
        self.reset_request = session.query(PasswordResetRequest).filter_by(token=self.entry_token_var.get()).first()

        if not self.reset_request:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = "Token is not valid."
            return

        timestamp = self.reset_request.timestamp
        expiration_time = timestamp + timedelta(minutes=5)
        current_time = datetime.now()

        if current_time > expiration_time:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = "Token is expired."
            session.delete(self.reset_request)
            session.commit()
            return

        self.label_message['fg'] = '#296108'
        self.label_message['text'] = "Token is valid."
        self.pass_entries()
        return

    def submit(self):
        password = self.entry_pass_var.get()
        password2 = self.entry_pass2_var.get()
        if password != password2:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = "Passwords do not match."
            return
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
            return

        user = session.query(User).filter_by(id=self.reset_request.user_id).first()

        existing_password = session.query(Password).filter_by(user_id=user.id).first()

        if existing_password:
            existing_password.set_password(password=password)
        else:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = "Password record not found for the user."
            return

        session.delete(self.reset_request)
        session.commit()

        self.after(1000, self.payment.countdown, 3)
