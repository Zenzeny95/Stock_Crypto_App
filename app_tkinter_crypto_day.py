"""
The 'CryptoDailyPopupWindow' class represents a Tkinter popup window for displaying cryptocurrency data and charts.

Class Methods:
- '__init__(self, master, title)': Initializes a new 'CryptoDailyPopupWindow' instance.
    - 'master': The master Tkinter window to which this popup is associated.
    - 'title': The title of the popup window.

Methods:
- 'display_chart(self, df, currency)': Displays a candlestick chart based on the provided DataFrame and currency.
    - 'df': The DataFrame containing cryptocurrency data.
    - 'currency': The currency abbreviation for the chart.
- 'refresh_results(self)': Refreshes the displayed cryptocurrency data and chart based on user
 inputs and performs input validation.

Note:
- This class represents a Tkinter popup window for interacting with cryptocurrency data.
- It includes methods for handling user input, data visualization, and data retrieval.
- The 'refresh_results' method performs various input validation checks and fetches cryptocurrency data accordingly.
- The 'display_chart' method visualizes the cryptocurrency data using a candlestick chart.
"""

import tkinter as tk
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
import re
from app_mixed_methods import Methods, pd
from tkinter import font as tkFont
from tkinter import ttk
from tkmacosx import Button as MacButton
from app_tkinter_crypto_checks import CryptoChecks


class CryptoDailyPopupWindow(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        self.label = tk.Label(self, font=("Helvetica", 16))
        self.label.pack(padx=20, pady=40)
        width = 1600
        height = 880
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.font_label = tk.font.Font(family="Helvetica", size=18)
        self.method = Methods()
        self.checks = CryptoChecks()

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/1600x880background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self, text='Enter Crypto Abbreviation, Currency, Date and Submit to Search',
                                      anchor="n", justify="center", font=self.font_label, bg='SystemButtonFace',
                                      highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=550, y=30, width=550, height=40)

        # TREE FRAME
        tree_frame = tk.Frame(self)
        tree_frame.place(x=50, y=90, width=600, height=500)

        # TREE
        self.tree = ttk.Treeview(self)
        self.tree['show'] = 'headings'
        self.tree.place(x=50, y=90, width=600, height=500)

        # SCROLLBAR
        self.tree_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar.place(x=650, y=90, height=500)
        self.tree_scrollbar2 = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree_scrollbar2.place(x=50, y=590, width=600)
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set, xscrollcommand=self.tree_scrollbar2.set)

        # CHART FRAME
        self.chart_frame = tk.Frame(self)
        self.chart_frame.place(x=730, y=90, width=850, height=770)

        # CHECKBUTTON
        self.show_chart_var = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(self, text="Show Chart", font=self.font, variable=self.show_chart_var,
                                          bg='grey')
        self.checkbutton.place(x=410, y=655)

        # ENTRIES
        self.entry_var = tk.StringVar()
        self.entry_var.set("Enter Crypto Abbreviation")
        entry = tk.Entry(self, textvariable=self.entry_var, font=self.font, borderwidth="1px", fg="#ffffff",
                         justify="center", bg="grey")
        entry.place(x=50, y=660, width=320, height=40)

        self.entry_var2 = tk.StringVar()
        self.entry_var2.set("Date (YYYY-MM or YYYY)")
        entry2 = tk.Entry(self, textvariable=self.entry_var2, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry2.place(x=50, y=720, width=320, height=40)

        self.entry_var3 = tk.StringVar()
        self.entry_var3.set("Currency (USD, EUR, GBP, etc...)")
        entry3 = tk.Entry(self, textvariable=self.entry_var3, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry3.place(x=50, y=780, width=320, height=40)

        # ENTRY BINDS
        entry.bind("<FocusIn>", self.on_entry_focus_in1)
        entry.bind("<FocusOut>", self.on_entry_focus_out1)
        entry2.bind("<FocusIn>", self.on_entry_focus_in2)
        entry2.bind("<FocusOut>", self.on_entry_focus_out2)
        entry3.bind("<FocusIn>", self.on_entry_focus_in3)
        entry3.bind("<FocusOut>", self.on_entry_focus_out3)

        # BUTTON
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        submit_button = MacButton(self, text="Submit", font=self.font, justify="center", command=self.refresh_results)
        close_button.place(x=410, y=765, width=266, height=50)
        submit_button.place(x=410, y=695, width=266, height=50)

    def on_entry_focus_in1(self, event):
        if self.entry_var.get() == "Enter Crypto Abbreviation":
            self.entry_var.set("")

    def on_entry_focus_out1(self, event):
        if not self.entry_var.get():
            self.entry_var.set("Enter Crypto Abbreviation")

    def on_entry_focus_in2(self, event):
        if self.entry_var2.get() == "Date (YYYY-MM or YYYY)":
            self.entry_var2.set("")

    def on_entry_focus_out2(self, event):
        if not self.entry_var2.get():
            self.entry_var2.set("Date (YYYY-MM or YYYY)")

    def on_entry_focus_in3(self, event):
        if self.entry_var3.get() == "Currency (USD, EUR, GBP, etc...)":
            self.entry_var3.set("")

    def on_entry_focus_out3(self, event):
        if not self.entry_var3.get():
            self.entry_var3.set("Currency (USD, EUR, GBP, etc...)")

    def tree_view(self, df):
        self.tree.delete(*self.tree.get_children())
        rows = df.values.tolist()
        self.tree["columns"] = df.columns.to_list()
        for col_name in df.columns:
            self.tree.heading(col_name, text=col_name)
            col_width = max(
                tkFont.Font().measure(str(col_name)),
                *df[col_name].apply(lambda x: tkFont.Font().measure(str(x))), 100, )
            self.tree.column(col_name, width=col_width + 20, stretch=False)
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def display_chart(self, df, currency):
        if currency.upper() == 'CURRENCY (USD, EUR, GBP, ETC...)':
            currency = "USD"
        month_pattern = r'^\d{4}-\d{2}$'
        year_pattern = r'^\d{4}$'
        if self.show_chart_var.get():
            df['open'] = df[f'open ({currency})']
            df['high'] = df[f'high ({currency})']
            df['low'] = df[f'low ({currency})']
            df['close'] = df[f'close ({currency})']
            df.drop([f'open ({currency})', f'high ({currency})', f'low ({currency})',
                     f'close ({currency})'], axis=1, inplace=True)
            df.index = pd.to_datetime(df.index)
            df_sorted = df.sort_index()
            fig, ax = plt.subplots(figsize=(10, 5))
            if re.match(month_pattern, self.entry_var2.get()):
                mpf.plot(df_sorted, type='candle', style='yahoo', xrotation=45, datetime_format="%Y-%m-%d",
                         ax=ax)
            elif re.match(year_pattern, self.entry_var2.get()):
                mpf.plot(df_sorted, type='candle', style='yahoo', xrotation=45, datetime_format="%Y-%m",
                         ax=ax)
            ax.grid(True)
            chart_frame = self.children["!frame2"]
            for widget in chart_frame.winfo_children():
                widget.destroy()
            canvas = tkagg.FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def refresh_results(self):
        try:
            self.label_message['fg'] = "#0E82D3"
            self.label_message['text'] = 'Enter Crypto Abbreviation, Currency, Date and Submit to Search'
            crypto = self.entry_var.get().strip()
            date = self.entry_var2.get().strip()
            currency = self.entry_var3.get().strip()

            is_valid_crypto = self.checks.is_valid_crypto(crypto)
            is_valid_currency = self.checks.is_valid_currency(currency)
            is_valid_date = self.checks.is_valid_date(date)

            if is_valid_crypto is False:
                self.label_message['fg'] = "red"
                self.label_message['text'] = 'Invalid Crypto Entry'
                self.tree.delete(*self.tree.get_children())
                return
            crypto = crypto.upper()

            if is_valid_date is None and is_valid_currency is None:
                df = self.method.daily_crypto_report(crypto=crypto)
                self.tree_view(df)
                self.display_chart(df, currency=currency)
            elif is_valid_currency is None and is_valid_date is True:
                df = self.method.daily_crypto_report(crypto=crypto, date=date)
                self.tree_view(df)
                self.display_chart(df, currency.upper())
            elif is_valid_currency is True and is_valid_date is None:
                df = self.method.daily_crypto_report(crypto=crypto, currency=currency.upper())
                self.tree_view(df)
                self.display_chart(df, currency.upper())
            elif is_valid_currency is True and is_valid_date is True:
                df = self.method.daily_crypto_report(crypto=crypto, currency=currency.upper(), date=date)
                self.tree_view(df)
                self.display_chart(df, currency.upper())
            elif is_valid_currency is False or is_valid_date is False:
                print('error')
                raise ValueError
        except KeyError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found'
            self.tree.delete(*self.tree.get_children())
        except IndexError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Invalid Entry'
            self.tree.delete(*self.tree.get_children())
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Invalid Entry'
            self.tree.delete(*self.tree.get_children())
