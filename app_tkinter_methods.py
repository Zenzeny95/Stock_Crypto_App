"""
The 'PopupWindowMethods' class represents a Tkinter popup window for accessing various
 investment-related functionalities.

Class Methods:
- '__init__(self, master, title, user_type, username)': Initializes a new 'PopupWindowMethods' instance.
    - 'master': The master Tkinter window to which this popup is associated.
    - 'title': The title of the popup window.
    - 'user_type': A boolean indicating the user type (True for privileged users, False for others).
    - 'username': The username of the current user.

Methods:
- 'on_investmentgainloss(self)': Opens a popup window to access the "Investment Gain/Loss" functionality.
- 'on_investmentcompare(self)': Opens a popup window to access the "Compare Investments"
 functionality (privileged users only).
- 'on_technicalind(self)': Opens a popup window to access the "Technical Indicators" functionality
 (privileged users only).
- 'on_alert(self)': Opens a popup window to access the "Price Alert" functionality (privileged users only).
- 'on_exchange(self)': Opens a popup window to access the "Exchange" functionality.
- 'on_buildchart(self)': Opens a popup window to access the "Price Prediction" functionality (privileged users only).

Note:
- This class represents a Tkinter popup window for accessing investment-related features.
- It includes methods for opening different popup windows based on user interaction.
- Some functionality buttons are disabled for non-privileged users.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
from app_tkinter_methods_gainloss import InvestmentGLPopupWindow
from app_tkinter_methods_compare import InvestmentsComaprePopupWindow
from app_tkinter_methods_alert import AlertPopupWindow
from app_tkinter_methods_exchange import ExchangePopupWindow
from app_tkinter_methods_indicators import TechnicalIndicatorPopupWindow
from app_tkinter_methods_prediction import PredictionsPopupWindow


class PopupWindowMethods(tk.Toplevel):
    def __init__(self, master, title, user_type, username):
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
        self.type = user_type
        self.username = username

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/600x300background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # BUTTONS
        invest_gl_button = MacButton(self, font=self.font, justify='center', text='Investment Gain/Loss',
                                     command=self.on_investmentgainloss)
        compare_button = MacButton(self, font=self.font, justify='center', text='Compare Investments',
                                   command=self.on_investmentcompare)
        if self.type is False:
            compare_button['state'] = 'disabled'
        technical_button = MacButton(self, font=self.font, justify='center', text='Technical Indicators',
                                     command=self.on_technicalind)
        if self.type is False:
            technical_button['state'] = 'disabled'
        alert_button = MacButton(self, font=self.font, justify='center', text='Price Alert', command=self.on_alert)
        if self.type is False:
            alert_button['state'] = 'disabled'
        exchange_button = MacButton(self, font=self.font, justify='center', text='Exchange', command=self.on_exchange)

        close_button = MacButton(self, font=self.font, justify="center", text="Close Window", command=self.destroy)
        prediction_button = MacButton(self, font=self.font, justify='center', text='Price Prediction',
                                      command=self.on_predictions)
        if self.type is False:
            prediction_button['state'] = 'disabled'

        invest_gl_button.place(x=20, y=50, width=176, height=50)
        compare_button.place(x=210, y=50, width=176, height=50)
        technical_button.place(x=400, y=50, width=176, height=50)
        alert_button.place(x=210, y=120, width=176, height=50)
        exchange_button.place(x=20, y=120, width=176, height=50)
        close_button.place(x=210, y=230, width=176, height=50)
        prediction_button.place(x=400, y=120, width=176, height=50)

    def on_investmentgainloss(self):
        InvestmentGLPopupWindow(self, "Investment Gain/Loss")

    def on_investmentcompare(self):
        InvestmentsComaprePopupWindow(self, "Investments Compare")

    def on_technicalind(self):
        TechnicalIndicatorPopupWindow(self, "Technical Indicators")

    def on_alert(self):
        AlertPopupWindow(self, "Alert", self.username)

    def on_exchange(self):
        ExchangePopupWindow(self, "Exchange")

    def on_predictions(self):
        PredictionsPopupWindow(self, "ML Predictions")
