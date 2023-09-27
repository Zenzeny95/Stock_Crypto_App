"""
This class defines a Tkinter-based popup window for displaying Stochastic Oscillator (STOCH) charts
and allows users to input parameters for data retrieval and visualization.

The STOCHPopupWindow class provides a graphical user interface for users to input parameters such as
equity or currency pair, interval, month, fastk, slowk, slowd, slowkma, slowdma, and chart type.
It then retrieves and displays STOCH charts based on the provided parameters.

Usage:
    1. Instantiate an STOCHPopupWindow object with a master Tkinter window and a title.
    2. Use the GUI to input STOCH parameters.
    3. Click the "Submit" button to fetch and display the STOCH chart.
    4. Optionally, provide parameters for equity or currency pair, interval, month, fastk, slowk, slowd,
       slowkma, slowdma, and chart type.
    5. The "Close Window" button closes the popup window.

The class provides a user-friendly interface for exploring Stochastic Oscillator (STOCH) charts
with customized parameters.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
import matplotlib.ticker as ticker
import mplfinance as mpf
import re
from app_api_stocks_requests import ApiDataStocks, pd
from app_mixed_methods import Methods


class STOCHPopupWindow(tk.Toplevel):
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
        self.chart_frame_stoch = tk.Frame(self)
        self.chart_frame_stock.place(x=720, y=10, width=900, height=515)
        self.chart_frame_stoch.place(x=720, y=526, width=900, height=350)

        # BUTTON
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        submit_button = MacButton(self, text="Submit", font=self.font, justify="center", command=self.refresh_results)
        close_button.place(x=430, y=765, width=266, height=55)
        submit_button.place(x=430, y=695, width=266, height=55)

        # LABEL
        label = tk.Label(self, font=self.font, justify='center', fg='black', bg='#F1EFEF')
        label['text'] = f'STOCH - Stochastic Oscillator\n\n' \
                        f'1. Equity or Forex pair (IBM or USDEUR)\n\n' \
                        f'2. Interval = weekly, monthly\n\n' \
                        f'3. For example, date=2009-01 or date=2009,\n' \
                        f'or date interval 2009-01/2012-01.\nAny month equal to or\n' \
                        f'later than 2000-01 (January 2000) is supported.\n\n' \
                        f'4. FastkPeriod - The time period of the fastk moving\n average' \
                        f'. Positive integers are accepted.\nBy default, fastkperiod=5\n\n' \
                        f'5. SlowkPeriod - The time period of the slowk moving\n average.' \
                        f' Positive integers are accepted.\nBy default, slowkperiod=3\n\n' \
                        f'6. SlowdPeriod - The time period of the slowd moving\n average.' \
                        f' Positive integers are accepted.\nBy default, slowdperiod=3\n\n' \
                        f'7. SlowkMaType - Integers 0 - 8 are accepted with the\n' \
                        f' following mappings. 0 = SMA, 1 = EMA, 2 = WMA,\n 3 = DEMA' \
                        f', 4 = TEMA, 5 = TRIMA,\n 6 = T3 Moving Average, 7 = KAMA, 8 = MAMA.\n' \
                        f'By default, slowkmatype=0\n\n' \
                        f'8. SlowdMaType - Integers 0 - 8 are accepted with the\n' \
                        f' following mappings. 0 = SMA, 1 = EMA, 2 = WMA,\n 3 = DEMA' \
                        f', 4 = TEMA, 5 = TRIMA,\n 6 = T3 Moving Average, 7 = KAMA, 8 = MAMA.\n' \
                        f'By default, slowdmatype=0'
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
        entry5.place(x=430, y=220, width=266, height=40)

        self.entry_var4 = tk.StringVar()
        self.entry_var4.set("Interval")
        entry4 = tk.Entry(self, textvariable=self.entry_var4, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry4.place(x=430, y=275, width=266, height=40)

        self.entry_var3 = tk.StringVar()
        self.entry_var3.set("Date")
        entry3 = tk.Entry(self, textvariable=self.entry_var3, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry3.place(x=430, y=330, width=266, height=40)

        self.entry_var6 = tk.StringVar()
        self.entry_var6.set("FastkPeriod (Optional)")
        entry6 = tk.Entry(self, textvariable=self.entry_var6, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry6.place(x=430, y=415, width=266, height=40)

        self.entry_var7 = tk.StringVar()
        self.entry_var7.set("SlowkPeriod (Optional)")
        entry7 = tk.Entry(self, textvariable=self.entry_var7, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry7.place(x=430, y=470, width=266, height=40)

        self.entry_var8 = tk.StringVar()
        self.entry_var8.set("SlowdPeriod (Optional)")
        entry8 = tk.Entry(self, textvariable=self.entry_var8, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry8.place(x=430, y=525, width=266, height=40)

        self.entry_var9 = tk.StringVar()
        self.entry_var9.set("SlowkMaType (Optional)")
        entry9 = tk.Entry(self, textvariable=self.entry_var9, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry9.place(x=430, y=580, width=266, height=40)

        self.entry_var10 = tk.StringVar()
        self.entry_var10.set("SlowdMaType (Optional)")
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
        if self.entry_var6.get() == "FastkPeriod (Optional)":
            self.entry_var6.set("")

    def on_entry_focus_out6(self, event):
        if not self.entry_var6.get():
            self.entry_var6.set("FastkPeriod (Optional)")

    def on_entry_focus_in7(self, event):
        if self.entry_var7.get() == "SlowkPeriod (Optional)":
            self.entry_var7.set("")

    def on_entry_focus_out7(self, event):
        if not self.entry_var7.get():
            self.entry_var7.set("SlowkPeriod (Optional)")

    def on_entry_focus_in8(self, event):
        if self.entry_var8.get() == "SlowdPeriod (Optional)":
            self.entry_var8.set("")

    def on_entry_focus_out8(self, event):
        if not self.entry_var8.get():
            self.entry_var8.set("SlowdPeriod (Optional)")

    def on_entry_focus_in9(self, event):
        if self.entry_var9.get() == "SlowkMaType (Optional)":
            self.entry_var9.set("")

    def on_entry_focus_out9(self, event):
        if not self.entry_var9.get():
            self.entry_var9.set("SlowkMaType (Optional)")

    def on_entry_focus_in10(self, event):
        if self.entry_var10.get() == "SlowdMaType (Optional)":
            self.entry_var10.set("")

    def on_entry_focus_out10(self, event):
        if not self.entry_var10.get():
            self.entry_var10.set("SlowdMaType (Optional)")

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

    def display_chart_stoch(self, df):
        df.sort_values('time', ascending=True, inplace=True)
        chart_frame = self.chart_frame_stoch
        if self.checkbox_state1.get() == 1:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df['time'], df['SlowK'], color='blue', label='SlowK')
            ax.plot(df['time'], df['SlowD'], color='red', label='SlowD')
            ax.legend()
            ax.set_title('STOCH Indicator Chart')
            ax.set_ylabel('STOCH Values')
            ax.grid(True)
            max_visible_ticks = 8
            ax.xaxis.set_major_locator(ticker.MaxNLocator(max_visible_ticks))
            for widget in chart_frame.winfo_children():
                widget.destroy()
            canvas = tkagg.FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        if self.checkbox_state2.get() == 1:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.fill_between(df['time'], df['SlowK'], df['SlowD'], color='blue', alpha=0.5, label='STOCH Area')
            ax.legend()
            ax.set_title('STOCH Indicator Area Chart')
            ax.set_ylabel('STOCH Values')
            ax.grid(True)
            max_visible_ticks = 8
            ax.xaxis.set_major_locator(ticker.MaxNLocator(max_visible_ticks))
            for widget in chart_frame.winfo_children():
                widget.destroy()
            canvas = tkagg.FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def fetch_data_for_date_range(self, equity, interval, start_date, end_date, fastkperiod, slowkperiod,
                                  slowdperiod, slowkmatype, slowdmatype):
        df_stoch = self.stock_data.stoch(symbol=equity, interval=interval, fastk=fastkperiod, slowk=slowkperiod,
                                         slowd=slowdperiod, slowkma=slowkmatype, slowdma=slowdmatype, month=start_date)
        df_interval = self.method.monthly_report(company=equity)

        df_stoch_filtered = df_stoch[(df_stoch['time'] >= start_date) & (df_stoch['time'] <= end_date)]
        df_interval_filtered = df_interval[(df_interval.index >= start_date) & (df_interval.index <= end_date)]

        return df_stoch_filtered, df_interval_filtered

    def refresh_results(self):
        try:
            self.label_message['fg'] = "#0E82D3"
            self.label_message['text'] = 'Enter Information and Submit to See Results'
            valid_intervals = {'weekly', 'monthly'}
            slowdmatype = self.entry_var10.get().strip()
            slowkmatype = self.entry_var9.get().strip()
            slowdperiod = self.entry_var8.get().strip()
            slowkperiod = self.entry_var7.get().strip()
            fastkperiod = self.entry_var6.get().strip()
            equity = self.entry_var5.get().strip().upper()
            interval = self.entry_var4.get().strip()
            if interval not in valid_intervals:
                raise ValueError
            date = self.entry_var3.get().strip()
            if date == "Date":
                df_stoch = self.stock_data.stoch(symbol=equity, interval=interval, fastk=fastkperiod, slowk=slowkperiod,
                                                 slowd=slowdperiod, slowkma=slowkmatype,
                                                 slowdma=slowdmatype, month=date)
                if interval == "weekly":
                    df_data = self.method.weekly_report(company=equity)
                    self.display_chart_stock(df_data)
                    self.display_chart_stoch(df_stoch)
                    return
                else:
                    df_data = self.method.monthly_report(company=equity)
                    self.display_chart_stock(df_data)
                    self.display_chart_stoch(df_stoch)
                    return
            date_pattern = r"^(?:\d{4}|\d{4}-\d{2})(?:\/(?:\d{4}|\d{4}-\d{2}))?$"
            if re.match(date_pattern, date):
                date_pattern_split = r'^\d{4}(?:-\d{2})?/\d{4}(?:-\d{2})?$'
                if re.match(date_pattern_split, date):
                    start_date, end_date = date.split("/")
                    df_stoch, df_interval = self.fetch_data_for_date_range(equity=equity, interval=interval,
                                                                           start_date=start_date, end_date=end_date,
                                                                           slowdmatype=slowdmatype,
                                                                           slowkmatype=slowkmatype,
                                                                           slowdperiod=slowdperiod,
                                                                           slowkperiod=slowkperiod,
                                                                           fastkperiod=fastkperiod)
                    self.display_chart_stock(df_interval)
                    self.display_chart_stoch(df_stoch)
                    return
                else:
                    df_stoch = self.stock_data.stoch(symbol=equity, interval=interval, fastk=fastkperiod,
                                                     slowk=slowkperiod, slowd=slowdperiod, slowkma=slowkmatype,
                                                     slowdma=slowdmatype, month=date)
                    df_stoch = df_stoch[df_stoch['time'].str.startswith(date)]
                    if interval == "weekly":
                        df_data = self.method.weekly_report(company=equity, date=date)
                        self.display_chart_stock(df_data)
                        self.display_chart_stoch(df_stoch)
                        return
                    else:
                        df_data = self.method.monthly_report(company=equity, date=date)
                        self.display_chart_stock(df_data)
                        self.display_chart_stoch(df_stoch)
                        return
            else:
                raise ValueError
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Invalid Entry'
        except KeyError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found\n Check Entries'
