"""
This Python file defines a set of pop-up windows for a finance application using the tkinter library.
 These pop-up windows are intended to display various stock-related information and functionalities.
  The key components of this code include:

1. Importing necessary modules such as 'tkinter' for creating the GUI, 'tkmacosx.Button' for macOS-specific buttons,
 and other modules for accessing stock data and methods.

2. Defining a `PopupWindowStock` class that represents a pop-up window for stock-related functionalities:
   - Initializes a pop-up window with a specified title.
   - Creates a GUI for displaying stock-related information, including a listbox for displaying data
    and buttons for different actions.
   - Allows users to view gainers/losers, open/close market data, search for specific companies, and access stock data
    for different time intervals (day, detailed day, now, weekly, and monthly).

3. The code utilizes external methods and classes (e.g., `Methods`, `SearchPopupWindow`, `StockNowPopupWindow`, etc.)
 to retrieve and display stock data.

4. The pop-up window's functionality depends on the user type (`user_type`) provided during initialization.
 Certain buttons may be disabled for specific user types.

5. The pop-up windows are displayed in a centered position on the screen and are not resizable.

6. The code provides functions for handling user actions, such as fetching and displaying
 stock data based on user selections.

7. Each pop-up window corresponds to a specific stock-related functionality, making it modular and user-friendly.

This code serves as a modular extension to the main finance application,
 allowing users to access various stock-related features through pop-up windows.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
from app_mixed_methods import *
from app_tkinter_stock_search import SearchPopupWindow
from app_tkinter_stock_now import StockNowPopupWindow
from app_tkinter_stock_day import StockDayPopupWindow
from app_tkinter_stock_detailed import StockDayDetailedPopupWindow
from app_tkinter_stock_weekly import StockWeeklyPopupWindow
from app_tkinter_stock_monthly import StockMonthlyPopupWindow


class PopupWindowStock(tk.Toplevel):
    def __init__(self, master, title, user_type):
        super().__init__(master)
        self.title(title)
        self.label = tk.Label(self, font=("Helvetica", 16))
        self.label.pack(padx=20, pady=40)
        width = 600
        height = 600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.type = user_type
        self.method = Methods()

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/600x600background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LIST BOXAS
        self.listbox = tk.Listbox(self, justify='center', font=self.font, borderwidth="1px", fg="#ffffff", bg="grey")
        self.listbox.place(x=20, y=10, width=549, height=241)

        # SCROLLBAR
        scrollbar = tk.Scrollbar(self, command=self.listbox.yview)
        scrollbar.place(x=570, y=10, height=241)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # BUTTONS FRAME
        gain_lose_button = MacButton(self, text="Gainers/Losers", justify="center", font=self.font,
                                     overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.on_gainers_losers)
        if self.type is False:
            gain_lose_button['state'] = 'disabled'
        open_close_button = MacButton(self, text="Markets Open/Close", justify="center", font=self.font,
                                      overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.on_open_close)

        # BUTTONS POPOUT
        search_button = MacButton(self, text="Search Company", justify="center", font=self.font,
                                  overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.on_search)
        if self.type is False:
            search_button['state'] = 'disabled'
        exit_button = MacButton(self, text="Close Window", justify="center", font=self.font,
                                overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.destroy)
        stockday_button = MacButton(self, text="StockData Day", justify="center", font=self.font,
                                    overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.on_stockday)
        stockdetailed_button = MacButton(self, text="StockData Detailed", justify="center", font=self.font,
                                         overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.on_stockdetailed)
        if self.type is False:
            stockdetailed_button['state'] = 'disabled'
        stocknow_button = MacButton(self, text="StockData Now", justify="center", font=self.font,
                                    overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.on_stocknow)
        stockweekly_button = MacButton(self, text="StockData Weekly", justify="center", font=self.font,
                                       overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.on_stockweekly)
        stockmonthly_button = MacButton(self, text="StockData Monthly", justify="center", font=self.font,
                                        overrelief=tk.SUNKEN, relief=tk.RAISED, command=self.on_stockmonthly)
        #################################################################
        gain_lose_button.place(x=90, y=260, width=176, height=45)
        search_button.place(x=400, y=470, width=176, height=45)
        open_close_button.place(x=310, y=260, width=176, height=45)
        exit_button.place(x=210, y=530, width=176, height=45)
        stockday_button.place(x=210, y=410, width=176, height=45)
        stockdetailed_button.place(x=400, y=410, width=176, height=45)
        stocknow_button.place(x=20, y=410, width=176, height=45)
        stockweekly_button.place(x=20, y=470, width=176, height=45)
        stockmonthly_button.place(x=210, y=470, width=176, height=45)

    def on_gainers_losers(self):
        self.listbox.delete(0, tk.END)
        row = 0
        data = self.method.gainers_losers()
        for elem in data:
            for key, val in elem.items():
                data = f"{key.capitalize()}: {val}"
                self.listbox.insert(tk.END, data)
                row += 1
                if row == 5:
                    self.listbox.insert(tk.END, "--" * 10)
                    row = 0

    def on_open_close(self):
        self.listbox.delete(0, tk.END)
        row = 0
        data = self.method.open_close()
        for elem in data:
            for key, val in elem.items():
                if "EXCEPT" in val:
                    value = val.split(",")
                    data = f"{key.capitalize()}: {value[0]}"
                    self.listbox.insert(tk.END, data)
                    self.listbox.insert(tk.END, value[1])
                    row += 1
                else:
                    data = f"{key.capitalize()}: {val}"
                    self.listbox.insert(tk.END, data)
                    row += 1
                if row == 7:
                    self.listbox.insert(tk.END, "--" * 10)
                    row = 0

    def on_search(self):
        SearchPopupWindow(self, "Search Company")

    def on_stocknow(self):
        StockNowPopupWindow(self, "Stock Info Now")

    def on_stockday(self):
        StockDayPopupWindow(self, "Stock Info By Day")

    def on_stockdetailed(self):
        StockDayDetailedPopupWindow(self, "Stock Info By Day Detailed")

    def on_stockweekly(self):
        StockWeeklyPopupWindow(self, "Stock Info By Week")

    def on_stockmonthly(self):
        StockMonthlyPopupWindow(self, "Stock Info By Month")
