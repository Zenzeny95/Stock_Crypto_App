"""
A popup window for premium user options.

This class defines a popup window that provides options for premium users,
including upgrading their subscription or canceling it.

Methods:
    upgrade(): Opens a popup window to upgrade the user's subscription.
    cancel(): Opens a popup window to cancel the user's subscription.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
from app_tkinter_upgrade import PopupWindowUpgrade
from app_tkinter_cancel import PopupWindowCancel


class PopupWindowPremium(tk.Toplevel):
    def __init__(self, master, title, username):
        super().__init__(master)
        self.title(title)
        self.label = tk.Label(self, font=("Helvetica", 16))
        self.label.pack(padx=20, pady=40)
        width = 600
        height = 300
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.font_label = tk.font.Font(family="Helvetica", size=18)
        self.username = username

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/600x300background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self,
                                      text='To Upgrade to Premium Select Upgrade\n\n'
                                           'To Cancel Subscription Select Cancel',
                                      anchor="n", justify="center", font=self.font_label, bg='SystemButtonFace',
                                      highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=110, y=20, width=380, height=70)

        # BUTTONS
        upgrade_button = MacButton(self, text="Upgrade", font=self.font, justify="center", command=self.upgrade)
        cancel_button = MacButton(self, text="Cancel", font=self.font, justify="center", command=self.cancel)
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        upgrade_button.place(x=75, y=130, width=200, height=50)
        cancel_button.place(x=330, y=130, width=200, height=50)
        close_button.place(x=200, y=230, width=200, height=50)

    def upgrade(self):
        self.premium_popup = PopupWindowUpgrade(self.master, "Upgrade", self.username)

    def cancel(self):
        self.cancel_popup = PopupWindowCancel(self.master, "Cancel Subscription", self.username)
