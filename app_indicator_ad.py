"""
This module defines a Tkinter-based popup window for displaying Chaikin A/D (Accumulation/Distribution) Line charts
and allowing users to input parameters for data retrieval and visualization.

The ADPopupWindow class provides a graphical user interface for users to input parameters such as equity or currency
pair, interval, and month, and then retrieve and display Chaikin A/D Line charts based on the provided parameters.

Usage:
    1. Instantiate an ADPopupWindow object with a master Tkinter window and a title.
    2. Use the GUI to input parameters.
    3. Click the "Submit" button to fetch and display the Chaikin A/D Line chart.
    4. Optionally, provide parameters for equity or currency pair, interval, and month.
    5. The "Close Window" button closes the popup window.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
import re
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
from app_mixed_methods import Methods, pd
from app_api_stocks_requests import ApiDataStocks


class ADPopupWindow(tk.Toplevel):
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
        self.stock_data = ApiDataStocks()

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/1600x880background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # CHART FRAME
        self.chart_frame_stock = tk.Frame(self)
        self.chart_frame_ad = tk.Frame(self)
        self.chart_frame_stock.place(x=530, y=10, width=1050, height=515)
        self.chart_frame_ad.place(x=530, y=526, width=1050, height=350)

        # LABEL
        label = tk.Label(self, font=self.font, justify='center', fg='black', bg='#F1EFEF')
        label['text'] = f'ADX - Average Directional Movement Index\n\n' \
                        f'1. Equity or Forex pair (IBM or USDEUR)\n\n' \
                        f'2. Interval = weekly, monthly\n\n' \
                        f'3. For example, date=2009-01 or date=2009,\n' \
                        f'or date interval 2009-01/2012-01.\nAny month equal to or\n' \
                        f'later than 2000-01 (January 2000) is supported.\n'

        self.label_message = tk.Label(self, text='Enter Information and Submit to See Results',
                                      anchor="n", justify="center", font=self.font_label, bg='SystemButtonFace',
                                      highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=10, y=30, width=500, height=40)
        label.place(x=10, y=90, width=500, height=320)

        # ENTRIES

        self.entry_var5 = tk.StringVar()
        self.entry_var5.set("Equity or Currency pair")
        entry5 = tk.Entry(self, textvariable=self.entry_var5, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry5.place(x=150, y=420, width=266, height=40)

        self.entry_var4 = tk.StringVar()
        self.entry_var4.set("Interval")
        entry4 = tk.Entry(self, textvariable=self.entry_var4, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry4.place(x=150, y=475, width=266, height=40)

        self.entry_var3 = tk.StringVar()
        self.entry_var3.set("Date")
        entry3 = tk.Entry(self, textvariable=self.entry_var3, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry3.place(x=150, y=530, width=266, height=40)

        # ENTRY BINDS
        entry3.bind("<FocusIn>", self.on_entry_focus_in3)
        entry3.bind("<FocusOut>", self.on_entry_focus_out3)
        entry4.bind("<FocusIn>", self.on_entry_focus_in4)
        entry4.bind("<FocusOut>", self.on_entry_focus_out4)
        entry5.bind("<FocusIn>", self.on_entry_focus_in5)
        entry5.bind("<FocusOut>", self.on_entry_focus_out5)

        # BUTTON
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        submit_button = MacButton(self, text="Submit", font=self.font, justify="center", command=self.refresh_results)
        submit_button.place(x=150, y=695, width=266, height=55)
        close_button.place(x=150, y=765, width=266, height=55)

    def on_entry_focus_in3(self, event):
        if self.entry_var3.get() == "Date":
            self.entry_var3.set("")

    def on_entry_focus_out3(self, event):
        if not self.entry_var3.get():
            self.entry_var3.set("Date")

    def on_entry_focus_in4(self, event):
        if self.entry_var4.get() == "Interval":
            self.entry_var4.set("")

    def on_entry_focus_out4(self, event):
        if not self.entry_var4.get():
            self.entry_var4.set("Interval")

    def on_entry_focus_in5(self, event):
        if self.entry_var5.get() == "Equity or Currency pair":
            self.entry_var5.set("")

    def on_entry_focus_out5(self, event):
        if not self.entry_var5.get():
            self.entry_var5.set("Equity or Currency pair")

    def display_chart_stock(self, df_data):
        df_data.index = pd.to_datetime(df_data.index)
        df_sorted = df_data.sort_index()
        fig, ax = plt.subplots(figsize=(12, 6))
        mpf.plot(df_sorted, type='candle', style='yahoo', xrotation=0, datetime_format="%Y-%m-%d", ax=ax)
        ax.grid(True)
        ax.yaxis.tick_left()
        ax.yaxis.set_label_position("left")
        ax.set_title('Stock Chart')
        chart_frame = self.chart_frame_stock
        for widget in chart_frame.winfo_children():
            widget.destroy()
        canvas = tkagg.FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def display_chart_ad(self, df):
        df.sort_values('time', ascending=True, inplace=True)
        df['time'] = pd.to_datetime(df['time'])
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df['time'], df['Chaikin A/D'], color='blue', label='Chaikin A/D')
        ax.grid(True)
        ax.legend()
        ax.set_title('Chaikin A/D Chart')
        ax.set_ylabel('Chaikin A/D')
        chart_frame = self.chart_frame_ad
        max_visible_ticks = 8
        ax.xaxis.set_major_locator(plt.MaxNLocator(max_visible_ticks))
        for widget in chart_frame.winfo_children():
            widget.destroy()
        canvas = tkagg.FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def fetch_data_for_date_range(self, symbol, interval, start_date, end_date):
        df_ad = self.stock_data.ad(symbol=symbol, interval=interval)
        df_interval = self.method.monthly_report(company=symbol)

        df_ad_filtered = df_ad[(df_ad['time'] >= start_date) & (df_ad['time'] <= end_date)]
        df_interval_filtered = df_interval[(df_interval.index >= start_date) & (df_interval.index <= end_date)]

        return df_ad_filtered, df_interval_filtered

    def refresh_results(self):
        try:
            self.label_message['fg'] = "#0E82D3"
            self.label_message['text'] = 'Enter Information and Submit to See Results'
            valid_intervals = {'weekly', 'monthly'}
            equity = self.entry_var5.get().strip().upper()
            interval = self.entry_var4.get().strip()
            if interval not in valid_intervals:
                raise ValueError
            date = self.entry_var3.get().strip()
            if date == "Date":
                df_ad = self.stock_data.ad(symbol=equity, interval=interval)
                if interval == "weekly":
                    df_data = self.method.weekly_report(company=equity)
                    self.display_chart_stock(df_data)
                    self.display_chart_ad(df_ad)
                    return
                else:
                    df_data = self.method.monthly_report(company=equity)
                    self.display_chart_stock(df_data)
                    self.display_chart_ad(df_ad)
                    return
            date_pattern = r"^(?:\d{4}|\d{4}-\d{2})(?:\/(?:\d{4}|\d{4}-\d{2}))?$"
            if re.match(date_pattern, date):
                date_pattern_split = r'^\d{4}(?:-\d{2})?/\d{4}(?:-\d{2})?$'
                if re.match(date_pattern_split, date):
                    start_date, end_date = date.split("/")
                    df_ad, df_interval = self.fetch_data_for_date_range(symbol=equity, interval=interval,
                                                                        start_date=start_date, end_date=end_date)
                    self.display_chart_stock(df_interval)
                    self.display_chart_ad(df_ad)
                    return
                else:
                    df_ad = self.stock_data.ad(symbol=equity, interval=interval, month=date)
                    df_ad = df_ad[df_ad['time'].str.startswith(date)]
                    if interval == "weekly":
                        df_data = self.method.weekly_report(company=equity, date=date)
                        self.display_chart_stock(df_data)
                        self.display_chart_ad(df_ad)
                        return
                    else:
                        df_data = self.method.monthly_report(company=equity, date=date)
                        self.display_chart_stock(df_data)
                        self.display_chart_ad(df_ad)
                        return
            else:
                raise ValueError
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Invalid Entry'
        except KeyError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found\n Check Entries'
