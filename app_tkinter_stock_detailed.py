"""
This Python file defines a pop-up window for displaying detailed daily stock data using the tkinter library.
 The key components of this code include:

1. Importing necessary modules such as 'tkinter' for creating the GUI, 'mplfinance' for plotting stock charts,
 'matplotlib' for chart rendering, and other modules for accessing stock data and methods.

2. Defining a `StockDayDetailedPopupWindow` class that represents a pop-up window for detailed daily stock data:
   - Initializes a pop-up window with a specified title.
   - Creates a GUI with a label, entry fields for company abbreviation, date, interval, checkboxes for showing a chart,
    a submit button, and a close button.
   - Allows users to input a company abbreviation, date (in 'YYYY-MM-DD' or 'YYYY-MM' format), and an interval
    (e.g., '1 min', '5 min') to retrieve detailed daily stock data.
   - Validates user inputs, checks for valid date formats, and ensures that the selected date is not a weekend
    (Saturday or Sunday).
   - Optionally displays a candlestick chart of the stock data if the "Show Chart" checkbox is selected.

3. The code utilizes external methods and classes (e.g., `Methods`) to retrieve and display detailed daily stock data
 and to generate stock charts.

4. The pop-up window's functionality includes error handling for various scenarios, such as invalid inputs,
 no data found, date format errors, and invalid intervals.

5. The pop-up window is displayed in a centered position on the screen and is not resizable.

6. Users can submit their queries to retrieve detailed daily stock data for a specific company, date, and interval,
 and choose to display a chart.

This code provides a user-friendly interface for retrieving and visualizing detailed daily stock data for a selected
 company, date, and interval.
"""

import tkinter as tk
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
import re
from datetime import datetime
from tkinter import font as tkFont
from tkinter import ttk
from tkmacosx import Button as MacButton
from app_mixed_methods import Methods, pd


class StockDayDetailedPopupWindow(tk.Toplevel):
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

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/1600x880background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self, text='Enter Company Abbreviation, Date, Interval and Submit to Search',
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
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)

        # CHART FRAME
        chart_frame = tk.Frame(self)
        chart_frame.place(x=690, y=90, width=900, height=770)

        # CHECKBUTTON
        self.show_chart_var = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(self, text="Show Chart", font=self.font, variable=self.show_chart_var,
                                          bg='grey')
        self.checkbutton.place(x=410, y=655)

        # ENTRIES
        self.entry_var = tk.StringVar()
        self.entry_var.set("Enter Company Abbreviation")
        entry = tk.Entry(self, textvariable=self.entry_var, font=self.font, borderwidth="1px", fg="#ffffff",
                         justify="center", bg="grey")
        entry.place(x=50, y=660, width=320, height=40)

        self.entry_var2 = tk.StringVar()
        self.entry_var2.set("Date (YYYY-MM-DD or YYYY-MM)")
        entry2 = tk.Entry(self, textvariable=self.entry_var2, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry2.place(x=50, y=720, width=320, height=40)

        self.entry_var3 = tk.StringVar()
        self.entry_var3.set("Interval (1 min, 5 min, 15 min, 30 min, 60 min)")
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
        submit_button.place(x=410, y=695, width=266, height=55)
        close_button.place(x=410, y=765, width=266, height=55)

    def on_entry_focus_in1(self, event):
        if self.entry_var.get() == "Enter Company Abbreviation":
            self.entry_var.set("")

    def on_entry_focus_out1(self, event):
        if not self.entry_var.get():
            self.entry_var.set("Enter Company Abbreviation")

    def on_entry_focus_in2(self, event):
        if self.entry_var2.get() == "Date (YYYY-MM-DD or YYYY-MM)":
            self.entry_var2.set("")

    def on_entry_focus_out2(self, event):
        if not self.entry_var2.get():
            self.entry_var2.set("Date (YYYY-MM-DD or YYYY-MM)")

    def on_entry_focus_in3(self, event):
        if self.entry_var3.get() == "Interval (1 min, 5 min, 15 min, 30 min, 60 min)":
            self.entry_var3.set("")

    def on_entry_focus_out3(self, event):
        if not self.entry_var3.get():
            self.entry_var3.set("Interval (1 min, 5 min, 15 min, 30 min, 60 min)")

    def display_chart(self, df):
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        month_pattern = r'^\d{4}-\d{2}$'
        df.index = pd.to_datetime(df.index)
        df_sorted = df.sort_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        if re.match(date_pattern, self.entry_var2.get()):
            mpf.plot(df_sorted, type='candle', style='yahoo', xrotation=45, datetime_format="%H:%M",
                     ax=ax)
        elif re.match(month_pattern, self.entry_var2.get()):
            mpf.plot(df_sorted, type='candle', style='yahoo', xrotation=45, datetime_format="%Y-%m-%d",
                     ax=ax)

        ax.grid(True)
        chart_frame = self.children["!frame2"]
        for widget in chart_frame.winfo_children():
            widget.destroy()
        canvas = tkagg.FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        return

    def refresh_results(self):
        try:
            self.label_message['fg'] = "#0E82D3"
            self.label_message['text'] = 'Enter Company Abbreviation, Date, Interval and Submit to Search'
            default_company = "Enter Company Abbreviation"
            default_date = "Date (YYYY-MM-DD or YYYY-MM)"
            default_interval = "Interval (1 min, 5 min, 15 min, 30 min, 60 min)"
            company = self.entry_var.get().strip()
            date = self.entry_var2.get().strip()
            date_list = date.split("-")
            for date_elem in date_list:
                if not date_elem.isdigit():
                    raise TypeError
            if len(date_list) == 3:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                weekend = datetime.weekday(date_obj)
                if weekend == 5:
                    self.label_message['fg'] = "red"
                    self.label_message['text'] = 'Selected day is Saturday'
                    self.tree.delete(*self.tree.get_children())
                    return
                elif weekend == 6:
                    self.label_message['fg'] = "red"
                    self.label_message['text'] = 'Selected day is Sunday'
                    self.tree.delete(*self.tree.get_children())
                    return
            interval = self.entry_var3.get().strip()
            valid_intervals = {"1min", "1 min", "5min", "5 min", "15min", "15 min",
                               "30min", "30 min", "60min", "60 min"}
            if interval not in valid_intervals:
                raise ValueError("Invalid Interval")
            if interval in {"1min", "5min", "15min", "30min", "60min"}:
                pass
            else:
                interval_check = interval.split(" ")
                interval = interval_check[0] + interval_check[1]
            if company == default_company or company == " ":
                self.label_message['fg'] = "red"
                self.label_message['text'] = 'Invalid Company Entry'
                self.tree.delete(*self.tree.get_children())
                return
            elif (date == " " or date == default_date) and (interval == " " or interval == default_interval):
                df = self.method.daily_detailed_report(company=company.upper())
            elif date == " " or date == default_date:
                df = self.method.daily_detailed_report(company=company.upper(), interval=interval)
            elif interval == " " or interval == default_interval:
                df = self.method.daily_detailed_report(company=company.upper(), month=date)
            else:
                df = self.method.daily_detailed_report(company=company.upper(), interval=interval, month=date)
            if self.show_chart_var.get():
                if date == " " or date == default_date:
                    self.label_message['fg'] = "red"
                    self.label_message['text'] = 'Chart Not Available Without Date'
                else:
                    self.display_chart(df)
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = df.columns.to_list()
            for col_name in df.columns:
                self.tree.heading(col_name, text=col_name)
                col_width = max(
                    tkFont.Font().measure(str(col_name)),
                    *df[col_name].apply(lambda x: tkFont.Font().measure(str(x))), 100, )
                self.tree.column(col_name, width=col_width + 20, stretch=False)
            for index, row in df.iterrows():
                self.tree.insert("", tk.END, values=row.to_list())
        except KeyError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found'
            self.tree.delete(*self.tree.get_children())
        except TypeError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Data Format Invalid'
            self.tree.delete(*self.tree.get_children())
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found'
            self.tree.delete(*self.tree.get_children())
        except AttributeError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found For This Day'
            self.tree.delete(*self.tree.get_children())
