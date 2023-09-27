"""
The 'TechnicalIndicatorPopupWindow' class represents a Tkinter popup window for selecting technical indicators.

Class Methods:
- '__init__(self, master, title)': Initializes a new 'TechnicalIndicatorPopupWindow' instance.
    - 'master': The master Tkinter window to which this popup is associated.
    - 'title': The title of the popup window.

Methods:
- 'on_sma(self)': Opens the Simple Moving Average (SMA) technical indicator popup window.
- 'on_ema(self)': Opens the Exponential Moving Average (EMA) technical indicator popup window.
- 'on_stoch(self)': Opens the Stochastic Oscillator (STOCH) technical indicator popup window.
- 'on_rsi(self)': Opens the Relative Strength Index (RSI) technical indicator popup window.
- 'on_adx(self)': Opens the Average Directional Index (ADX) technical indicator popup window.
- 'on_cci(self)': Opens the Commodity Channel Index (CCI) technical indicator popup window.
- 'on_aroon(self)': Opens the Aroon technical indicator popup window.
- 'on_bbands(self)': Opens the Bollinger Bands (BBANDS) technical indicator popup window.
- 'on_ad(self)': Opens the Accumulation/Distribution (AD) technical indicator popup window.
- 'on_obv(self)': Opens the On-Balance Volume (OBV) technical indicator popup window.

Note:
- This class represents a Tkinter popup window for selecting various technical indicators.
- Users can click buttons to open specific indicator popup windows.
- Each indicator has its own associated popup window for customization.
- The class provides methods to open these indicator-specific popup windows.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
from app_indicator_sma import SMAPopupWindow
from app_indicator_ema import EMAPopupWindow
from app_indicator_stoch import STOCHPopupWindow
from app_indicator_rsi import RSIPopupWindow
from app_indicator_adx import ADXPopupWindow
from app_indicator_cci import CCIPopupWindow
from app_indicator_aroon import AROONPopupWindow
from app_indicator_bbands import BBANDSPopupWindow
from app_indicator_ad import ADPopupWindow
from app_indicator_obv import OBVPopupWindow


class TechnicalIndicatorPopupWindow(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        width = 400
        height = 470
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/400x470background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # BUTTONS
        sma_button = MacButton(self, font=self.font, justify='center', text='SMA', command=self.on_sma)
        ema_button = MacButton(self, font=self.font, justify='center', text='EMA', command=self.on_ema)
        stoch_button = MacButton(self, font=self.font, justify='center', text='STOCH', command=self.on_stoch)
        rsi_button = MacButton(self, font=self.font, justify='center', text='RSI', command=self.on_rsi)
        adx_button = MacButton(self, font=self.font, justify='center', text='ADX', command=self.on_adx)
        cci_button = MacButton(self, font=self.font, justify='center', text='CCI', command=self.on_cci)
        aroon_button = MacButton(self, font=self.font, justify='center', text='AROON', command=self.on_aroon)
        bbands_button = MacButton(self, font=self.font, justify='center', text='BBANDS', command=self.on_bbands)
        ad_button = MacButton(self, font=self.font, justify='center', text='AD', command=self.on_ad)
        obv_button = MacButton(self, font=self.font, justify='center', text='OBV', command=self.on_obv)
        close_button = MacButton(self, font=self.font, justify='center', text='Close Window', command=self.destroy)

        sma_button.place(x=10, y=30, width=170, height=50)
        ema_button.place(x=210, y=30, width=170, height=50)
        stoch_button.place(x=210, y=100, width=170, height=50)
        rsi_button.place(x=10, y=170, width=170, height=50)
        adx_button.place(x=210, y=170, width=170, height=50)
        cci_button.place(x=10, y=100, width=170, height=50)
        aroon_button.place(x=10, y=240, width=170, height=50)
        bbands_button.place(x=210, y=240, width=170, height=50)
        ad_button.place(x=10, y=310, width=170, height=50)
        obv_button.place(x=210, y=310, width=170, height=50)
        close_button.place(x=110, y=400, width=170, height=50)

    def on_sma(self):
        SMAPopupWindow(self, "SMA Technical Indicator")

    def on_ema(self):
        EMAPopupWindow(self, "EMA Technical Indicator")

    def on_stoch(self):
        STOCHPopupWindow(self, "STOCH Technical Indicator")

    def on_rsi(self):
        RSIPopupWindow(self, "RSI Technical Indicator")

    def on_adx(self):
        ADXPopupWindow(self, "ADX Technical Indicator")

    def on_cci(self):
        CCIPopupWindow(self, "CCI Technical Indicator")

    def on_aroon(self):
        AROONPopupWindow(self, "AROON Technical Indicator")

    def on_bbands(self):
        BBANDSPopupWindow(self, "BBANDS Technical Indicator")

    def on_ad(self):
        ADPopupWindow(self, "AD Technical Indicator")

    def on_obv(self):
        OBVPopupWindow(self, "OBV Technical Indicator")
