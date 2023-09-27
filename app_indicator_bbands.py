"""
This class defines a Tkinter-based popup window for displaying Bollinger Bands (BBANDS) charts
and allows users to input parameters for data retrieval and visualization.

The BBANDSPopupWindow class provides a graphical user interface for users to input parameters such as
equity or currency pair, interval, month, data points, price type, standard deviation multipliers,
moving average type, and chart type (line or area). It then retrieves and displays BBANDS charts based
on the provided parameters.

Usage:
    1. Instantiate a BBANDSPopupWindow object with a master Tkinter window and a title.
    2. Use the GUI to input BBANDS parameters.
    3. Click the "Submit" button to fetch and display the BBANDS chart.
    4. Optionally, provide parameters for equity or currency pair, interval, month, and more.
    5. Choose between Line Chart and Area Chart display using checkboxes.
    6. The "Close Window" button closes the popup window.

The class provides a user-friendly interface for exploring Bollinger Bands (BBANDS) charts
with customized parameters and chart type.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
import matplotlib.ticker as ticker
import mplfinance as mpf
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app_mixed_methods import Methods, pd
from app_api_stocks_requests import ApiDataStocks


class BBANDSPopupWindow(tk.Toplevel):
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
        self.chart_frame_bbands = tk.Frame(self)
        self.chart_frame_stock.place(x=720, y=10, width=900, height=515)
        self.chart_frame_bbands.place(x=720, y=526, width=900, height=350)

        # BUTTON
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        submit_button = MacButton(self, text="Submit", font=self.font, justify="center", command=self.refresh_results)
        close_button.place(x=430, y=765, width=266, height=55)
        submit_button.place(x=430, y=695, width=266, height=55)

        # LABEL
        label = tk.Label(self, font=self.font, justify='center', fg='black', bg='#F1EFEF')
        label['text'] = f'BBANDS - Bollinger Bands\n\n' \
                        f'1. Equity or Forex pair (IBM or USDEUR)\n\n' \
                        f'2. Interval = weekly, monthly\n\n' \
                        f'3. For example, date=2009-01 or date=2009,\n' \
                        f'or date interval 2009-01/2012-01.\nAny month equal to or\n' \
                        f'later than 2000-01 (January 2000) is supported.\n\n' \
                        f'4. Data Points - Number of data points used\n' \
                        f' to calculate each BBANDS value. Positive integers\n' \
                        f' are accepted (e.g., time_period=60, time_period=200)\n' \
                        f'The daily/weekly/monthly intervals\n are agnostic to this parameter\n\n' \
                        f'5. Price Type - The desired price type in the time series.\n' \
                        f' Four types are supported: close, open, high, low\n\n' \
                        f'6. NBDEVUP - The standard deviation multiplier of\n' \
                        f' the upper band. Positive integers are accepted.\n\n' \
                        f'7. NBDEVDN - The standard deviation multiplier of\n' \
                        f' the lower band. Positive integers are accepted.\n\n' \
                        f'8. MaType - Moving average type of the time series.\n' \
                        f' By default, matype=0. Integers 0 - 8 are accepted\n' \
                        f' with the following mappings.\n' \
                        f' 0 = Simple Moving Average (SMA),\n' \
                        f' 1 = Exponential Moving Average (EMA),\n' \
                        f' 2 = Weighted Moving Average (WMA),\n' \
                        f' 3 = Double Exponential Moving Average (DEMA),\n' \
                        f' 4 = Triple Exponential Moving Average (TEMA),\n' \
                        f' 5 = Triangular Moving Average (TRIMA),\n' \
                        f' 6 = T3 Moving Average,\n' \
                        f' 7 = Kaufman Adaptive Moving Average (KAMA),\n' \
                        f' 8 = MESA Adaptive Moving Average (MAMA).'
        self.label_message = tk.Label(self, text='Enter Information and Submit to See Results',
                                      anchor="n", justify="center", font=self.font_label, bg='SystemButtonFace',
                                      highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=50, y=30, width=550, height=40)
        label.place(x=10, y=90, width=400, height=750)

        # CHECKBOX
        self.checkbox_state1 = tk.IntVar()
        self.checkbox1 = tk.Checkbutton(self, font=self.font, justify='center', text='Line Chart',
                                        fg='black', bg='#F1EFEF', offvalue=0, onvalue=1,
                                        variable=self.checkbox_state1, command=self.on_checkbox1_change)
        self.checkbox1.place(x=430, y=100, width=150, height=30)

        self.checkbox_state2 = tk.IntVar()
        self.checkbox2 = tk.Checkbutton(self, font=self.font, justify='center', text='Area Chart',
                                        fg='black', bg='#F1EFEF', offvalue=0, onvalue=1,
                                        variable=self.checkbox_state2, command=self.on_checkbox2_change)
        self.checkbox2.place(x=430, y=150, width=150, height=30)

        # ENTRIES

        self.entry_var5 = tk.StringVar()
        self.entry_var5.set("Equity or Currency pair")
        entry5 = tk.Entry(self, textvariable=self.entry_var5, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry5.place(x=430, y=250, width=266, height=40)

        self.entry_var4 = tk.StringVar()
        self.entry_var4.set("Interval")
        entry4 = tk.Entry(self, textvariable=self.entry_var4, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry4.place(x=430, y=305, width=266, height=40)

        self.entry_var7 = tk.StringVar()
        self.entry_var7.set("Data Points")
        entry7 = tk.Entry(self, textvariable=self.entry_var7, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry7.place(x=430, y=360, width=266, height=40)

        self.entry_var6 = tk.StringVar()
        self.entry_var6.set("Price Type")
        entry6 = tk.Entry(self, textvariable=self.entry_var6, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry6.place(x=430, y=415, width=266, height=40)

        self.entry_var3 = tk.StringVar()
        self.entry_var3.set("Date")
        entry3 = tk.Entry(self, textvariable=self.entry_var3, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry3.place(x=430, y=470, width=266, height=40)

        self.entry_var8 = tk.StringVar()
        self.entry_var8.set("NBDEVUP (Optional)")
        entry8 = tk.Entry(self, textvariable=self.entry_var8, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry8.place(x=430, y=525, width=266, height=40)

        self.entry_var9 = tk.StringVar()
        self.entry_var9.set("NBDEVDN (Optional)")
        entry9 = tk.Entry(self, textvariable=self.entry_var9, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry9.place(x=430, y=580, width=266, height=40)

        self.entry_var10 = tk.StringVar()
        self.entry_var10.set("MaType (Optional)")
        entry10 = tk.Entry(self, textvariable=self.entry_var10, font=self.font, borderwidth="1px", fg="#ffffff",
                           justify="center", bg="grey")
        entry10.place(x=430, y=635, width=266, height=40)

        # ENTRY BINDS
        entry3.bind("<FocusIn>", self.on_entry_focus_in3)
        entry3.bind("<FocusOut>", self.on_entry_focus_out3)
        entry4.bind("<FocusIn>", self.on_entry_focus_in4)
        entry4.bind("<FocusOut>", self.on_entry_focus_out4)
        entry5.bind("<FocusIn>", self.on_entry_focus_in5)
        entry5.bind("<FocusOut>", self.on_entry_focus_out5)
        entry6.bind("<FocusIn>", self.on_entry_focus_in6)
        entry6.bind("<FocusOut>", self.on_entry_focus_out6)
        entry7.bind("<FocusIn>", self.on_entry_focus_in7)
        entry7.bind("<FocusOut>", self.on_entry_focus_out7)
        entry8.bind("<FocusIn>", self.on_entry_focus_in8)
        entry8.bind("<FocusOut>", self.on_entry_focus_out8)
        entry9.bind("<FocusIn>", self.on_entry_focus_in9)
        entry9.bind("<FocusOut>", self.on_entry_focus_out9)
        entry10.bind("<FocusIn>", self.on_entry_focus_in10)
        entry10.bind("<FocusOut>", self.on_entry_focus_out10)

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

    def on_entry_focus_in6(self, event):
        if self.entry_var6.get() == "Price Type":
            self.entry_var6.set("")

    def on_entry_focus_out6(self, event):
        if not self.entry_var6.get():
            self.entry_var6.set("Price Type")

    def on_entry_focus_in7(self, event):
        if self.entry_var7.get() == "Data Points":
            self.entry_var7.set("")

    def on_entry_focus_out7(self, event):
        if not self.entry_var7.get():
            self.entry_var7.set("Data Points")

    def on_entry_focus_in8(self, event):
        if self.entry_var8.get() == "NBDEVUP (Optional)":
            self.entry_var8.set("")

    def on_entry_focus_out8(self, event):
        if not self.entry_var8.get():
            self.entry_var8.set("NBDEVUP (Optional)")

    def on_entry_focus_in9(self, event):
        if self.entry_var9.get() == "NBDEVDN (Optional)":
            self.entry_var9.set("")

    def on_entry_focus_out9(self, event):
        if not self.entry_var9.get():
            self.entry_var9.set("NBDEVDN (Optional)")

    def on_entry_focus_in10(self, event):
        if self.entry_var10.get() == "MaType (Optional)":
            self.entry_var10.set("")

    def on_entry_focus_out10(self, event):
        if not self.entry_var10.get():
            self.entry_var10.set("MaType (Optional)")

    def on_checkbox1_change(self):
        if self.checkbox_state1.get() == 1:
            self.checkbox2.config(state=tk.DISABLED)
        elif self.checkbox_state1.get() == 0:
            self.checkbox2.config(state=tk.NORMAL)

    def on_checkbox2_change(self):
        if self.checkbox_state2.get() == 1:
            self.checkbox1.config(state=tk.DISABLED)
        elif self.checkbox_state2.get() == 0:
            self.checkbox1.config(state=tk.NORMAL)

    def display_chart_stock(self, df_data):
        df_data.index = pd.to_datetime(df_data.index)
        df_sorted = df_data.sort_index()
        fig, ax = plt.subplots(figsize=(10, 5))
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

    def display_chart_bbands(self, df):
        chart_frame = self.chart_frame_bbands
        if self.checkbox_state1.get() == 1:
            df.sort_values('time', ascending=True, inplace=True)
            df['time'] = pd.to_datetime(df['time'])
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(df['time'], df['Real Lower Band'], color='blue', label='Real Lower Band')
            ax.plot(df['time'], df['Real Middle Band'], color='orange', label='Real Middle Band')
            ax.plot(df['time'], df['Real Upper Band'], color='purple', label='Real Upper Band')
            ax.grid(True)
            ax.legend()
            ax.set_title('BBANDS Chart')
            ax.set_ylabel('BBANDS Values')
            ymin, ymax = ax.get_ylim()
            ax.set_ylim(ymin, ymax)
            max_visible_ticks = 8
            ax.xaxis.set_major_locator(plt.MaxNLocator(max_visible_ticks))
            for widget in chart_frame.winfo_children():
                widget.destroy()
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        if self.checkbox_state2.get() == 1:
            df.sort_values('time', ascending=True, inplace=True)
            df['time'] = pd.to_datetime(df['time'])
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.fill_between(df['time'], df['Real Lower Band'], df['Real Middle Band'],
                            df['Real Upper Band'], color='blue', alpha=0.5)
            ax.legend()
            ax.set_title('BBANDS Indicator Area Chart')
            ax.set_ylabel('BBANDS Values')
            ax.grid(True)
            ymin, ymax = ax.get_ylim()
            ax.set_ylim(ymin, ymax)
            max_visible_ticks = 8
            ax.xaxis.set_major_locator(ticker.MaxNLocator(max_visible_ticks))
            for widget in chart_frame.winfo_children():
                widget.destroy()
            canvas = tkagg.FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def fetch_data_for_date_range(self, equity, interval, start_date, end_date, pricet,
                                  timep, matype, nbdevdn, nbdevup):
        df_bbands = self.stock_data.bbands(symbol=equity, interval=interval, series=pricet, timep=timep, matype=matype,
                                           nbdevdn=nbdevdn, nbdevup=nbdevup)
        df_interval = self.method.monthly_report(company=equity)

        df_bbands_filtered = df_bbands[(df_bbands['time'] >= start_date) & (df_bbands['time'] <= end_date)]
        df_interval_filtered = df_interval[(df_interval.index >= start_date) & (df_interval.index <= end_date)]

        return df_bbands_filtered, df_interval_filtered

    def refresh_results(self):
        try:
            self.label_message['fg'] = "#0E82D3"
            self.label_message['text'] = 'Enter Information and Submit to See Results'
            valid_intervals = {'weekly', 'monthly'}
            price_set = {'close', 'open', 'low', 'high'}
            matype = self.entry_var10.get().strip()
            nbdevdn = self.entry_var9.get().strip()
            nbdevup = self.entry_var8.get().strip()
            timep = int(self.entry_var7.get().strip())
            equity = self.entry_var5.get().strip().upper()
            interval = self.entry_var4.get().strip()
            if interval not in valid_intervals:
                raise ValueError
            pricet = self.entry_var6.get().strip()
            if pricet.lower() not in price_set:
                raise ValueError
            date = self.entry_var3.get().strip()
            if date == "Date":
                df_bbands = self.stock_data.bbands(symbol=equity, interval=interval, series=pricet, timep=timep,
                                                   matype=matype, nbdevdn=nbdevdn, nbdevup=nbdevup, month=date)
                if interval == "weekly":
                    df_data = self.method.weekly_report(company=equity)
                    self.display_chart_stock(df_data)
                    self.display_chart_bbands(df_bbands)
                    return
                else:
                    df_data = self.method.monthly_report(company=equity)
                    self.display_chart_stock(df_data)
                    self.display_chart_bbands(df_bbands)
                    return
            date_pattern = r"^(?:\d{4}|\d{4}-\d{2})(?:\/(?:\d{4}|\d{4}-\d{2}))?$"
            if re.match(date_pattern, date):
                date_pattern_split = r'^\d{4}(?:-\d{2})?/\d{4}(?:-\d{2})?$'
                if re.match(date_pattern_split, date):
                    start_date, end_date = date.split("/")
                    df_bbands, df_interval = self.fetch_data_for_date_range(equity=equity, interval=interval,
                                                                            start_date=start_date, end_date=end_date,
                                                                            pricet=pricet, timep=timep, matype=matype,
                                                                            nbdevdn=nbdevdn, nbdevup=nbdevup)
                    self.display_chart_stock(df_interval)
                    self.display_chart_bbands(df_bbands)
                    return
                else:
                    df_bbands = self.stock_data.bbands(symbol=equity, interval=interval, series=pricet, timep=timep,
                                                       matype=matype, nbdevdn=nbdevdn, nbdevup=nbdevup)
                    df_bbands = df_bbands[df_bbands['time'].str.startswith(date)]
                    if interval == "weekly":
                        df_data = self.method.weekly_report(company=equity, date=date)
                        self.display_chart_stock(df_data)
                        self.display_chart_bbands(df_bbands)
                        return
                    else:
                        df_data = self.method.monthly_report(company=equity, date=date)
                        self.display_chart_stock(df_data)
                        self.display_chart_bbands(df_bbands)
                        return
            else:
                raise ValueError
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Invalid Entry'
        except KeyError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found\n Check Entries'
