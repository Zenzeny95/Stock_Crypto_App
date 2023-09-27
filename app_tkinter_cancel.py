"""
A popup window for canceling user subscriptions.

This class defines a popup window that allows users to cancel their subscriptions.
It interacts with the database to perform subscription cancellation.

Methods:
    cancel_subscription(): Cancels the user's subscription and updates the database accordingly.
"""

from model import engine, User
from sqlalchemy.orm import sessionmaker
import tkinter as tk


Session = sessionmaker(bind=engine)


class PopupWindowCancel(tk.Toplevel):
    def __init__(self, master, title, username):
        super().__init__(master)
        self.title(title)
        self.label = tk.Label(self, font=("Helvetica", 16))
        self.label.pack(padx=20, pady=40)
        width = 400
        height = 172
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.font_label = tk.font.Font(family="Helvetica", size=18)
        self.username = username

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/400x470background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self, text='', anchor="n", justify="center", font=self.font_label,
                                      bg='SystemButtonFace', highlightthickness=0)
        self.label_message.place(x=10, y=35, width=380, height=100)

        self.cancel_subscription()

    def cancel_subscription(self):
        session = Session()

        user = session.query(User).filter_by(username=self.username).first()
        print(user)
        if user:
            print(user.creditcards)
            if user.creditcards:
                for credit_card in user.creditcards:
                    session.delete(credit_card)
                    session.commit()
                self.label_message['fg'] = '#296108'
                self.label_message['text'] = "Subscription Cancelled Succesful!\nWindow Will Close in 2 Seconds"
                self.after(2000, self.destroy)
            else:
                self.label_message['fg'] = 'red'
                self.label_message['text'] = f"User {self.username} Is Not Subscribed!\nWindow Will Close in 2 Seconds"
                self.after(2000, self.destroy)
        else:
            self.label_message['fg'] = 'red'
            self.label_message['text'] = f"User {self.username} Not Found\nWindow Will Close in 2 Seconds"
            self.after(2000, self.destroy)
