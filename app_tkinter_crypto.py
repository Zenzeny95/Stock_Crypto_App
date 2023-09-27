"""
The 'PopupWindowCrypto' class defines a graphical user interface (GUI) popup window that allows the user to choose
from three different crypto data display options: daily, weekly, and monthly. The user can access more detailed
information by clicking on these options.

Class Attributes:
- 'master': The master widget (typically the main application window) that this popup window is associated with.
- 'title': The title of the popup window.

Methods:
- '__init__(self, master, title)': Initializes a new instance of the 'PopupWindowCrypto' class.
    - 'master': The master widget (main application window) to which this popup window is attached.
    - 'title': The title to be displayed at the top of the popup window.
    - The constructor sets up the window's appearance, size, and buttons.

- 'on_cryptodaily(self)': Opens a new popup window displaying crypto information for the day. This function is called
when the "CryptoData Daily" button is clicked.

- 'on_cryptoweekly(self)': Opens a new popup window displaying crypto information for the week. This function is called
when the "CryptoData Weekly" button is clicked.

- 'on_cryptomonthly(self)': Opens a new popup window displaying crypto information for the month. This function is
called when the "CryptoData Monthly" button is clicked.

Note:
- This class assumes that specific popup windows for daily, weekly, and monthly crypto data display are defined in the
'CryptoDailyPopupWindow,' 'CryptoWeeklyPopupWindow,' and 'CryptoMonthlyPopupWindow' classes.
- The appearance and behavior of this popup window are configured in the constructor.
- The master widget should be provided when creating an instance of this class.
"""


import tkinter as tk
from tkmacosx import Button as MacButton
from app_tkinter_crypto_day import CryptoDailyPopupWindow
from app_tkinter_crypto_weekly import CryptoWeeklyPopupWindow
from app_tkinter_crypto_monthly import CryptoMonthlyPopupWindow


class PopupWindowCrypto(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        self.font = tk.font.Font(family="Helvetica", size=16)
        width = 600
        height = 300
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/600x300background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # BUTTONS
        daily_button = MacButton(self, font=self.font, justify="center", text="CryptoData Daily",
                                 command=self.on_cryptodaily)
        weekly_button = MacButton(self, font=self.font, justify="center", text="CryptoData Weekly",
                                  command=self.on_cryptoweekly)
        monthly_button = MacButton(self, font=self.font, justify="center", text="CryptoData Monthly",
                                   command=self.on_cryptomonthly)
        close_button = MacButton(self, font=self.font, justify="center", text="Close Window", command=self.destroy)

        daily_button.place(x=200, y=10, width=176, height=50)
        weekly_button.place(x=200, y=80, width=176, height=50)
        monthly_button.place(x=200, y=150, width=176, height=50)
        close_button.place(x=200, y=240, width=176, height=50)

    def on_cryptodaily(self):
        CryptoDailyPopupWindow(self, "Crypto Info By Day")

    def on_cryptoweekly(self):
        CryptoWeeklyPopupWindow(self, "Crypto Info By Week")

    def on_cryptomonthly(self):
        CryptoMonthlyPopupWindow(self, "Crypto Info By Month")
