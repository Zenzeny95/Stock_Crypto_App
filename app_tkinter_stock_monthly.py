"""
This Python file defines a pop-up window for displaying monthly stock data using the tkinter library.
 The key components of this code include:

1. Importing necessary modules such as 'tkinter' for creating the GUI, 'mplfinance' for plotting stock charts,
 'matplotlib' for chart rendering, and other modules for accessing stock data and methods.

2. Defining a `StockMonthlyPopupWindow` class that represents a pop-up window for monthly stock data:
   - Initializes a pop-up window with a specified title.
   - Creates a GUI with a label, entry fields for company abbreviation, date (in 'YYYY' or 'YYYY-MM' format),
    checkboxes for showing a chart, a submit button, and a close button.
   - Allows users to input a company abbreviation and an optional date to retrieve monthly stock data. Users can also
    choose to display a candlestick chart of the stock data.
   - Validates user inputs, checks for valid date formats (YYYY or YYYY-MM), and handles cases where inputs
    are missing or invalid.
   - Displays a candlestick chart if the "Show Chart" checkbox is selected.

3. The code utilizes external methods and classes (e.g., `Methods`) to retrieve and display monthly stock data
 and to generate stock charts.

4. The pop-up window's functionality includes error handling for various scenarios, such as invalid inputs,
 no data found, and invalid date formats.

5. The pop-up window is displayed in a centered position on the screen and is not resizable.

6. Users can submit their queries to retrieve monthly stock data for a specific company and date,
 and choose to display a chart.

This code provides a user-friendly interface for retrieving and visualizing monthly stock data for a selected company
 and date, with the option to display a chart.
"""

import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk
from tkmacosx import Button as MacButton
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
import re
from app_mixed_methods import Methods, pd


class StockMonthlyPopupWindow(tk.Toplevel):
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
        self.label_message = tk.Label(self, text='Enter Company Abbreviation, Date and Submit to Search',
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
        chart_frame.place(x=730, y=90, width=850, height=770)

        # CHECKBUTTON
        self.show_chart_var = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(self, text="Show Chart", font=self.font, variable=self.show_chart_var,
                                          bg='grey')
        self.checkbutton.place(x=55, y=680)

        # ENTRIES
        self.entry_var = tk.StringVar()
        self.entry_var.set("Enter Company Abbreviation")
        entry = tk.Entry(self, textvariable=self.entry_var, font=self.font, borderwidth="1px", fg="#ffffff",
                         justify="center", bg="grey")
        entry.place(x=50, y=720, width=320, height=40)

        self.entry_var2 = tk.StringVar()
        self.entry_var2.set("Date (YYYY or YYYY-MM)")
        entry2 = tk.Entry(self, textvariable=self.entry_var2, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry2.place(x=50, y=780, width=320, height=40)

        # ENTRY BINDS
        entry.bind("<FocusIn>", self.on_entry_focus_in1)
        entry.bind("<FocusOut>", self.on_entry_focus_out1)
        entry2.bind("<FocusIn>", self.on_entry_focus_in2)
        entry2.bind("<FocusOut>", self.on_entry_focus_out2)

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
        if self.entry_var2.get() == "Date (YYYY or YYYY-MM)":
            self.entry_var2.set("")

    def on_entry_focus_out2(self, event):
        if not self.entry_var2.get():
            self.entry_var2.set("Date (YYYY or YYYY-MM)")

    def display_chart(self, df):
        if self.show_chart_var.get():
            df.index = pd.to_datetime(df.index)
            df_sorted = df.sort_index()
            fig, ax = plt.subplots(figsize=(10, 5))
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
            self.label_message['text'] = 'Enter Company Abbreviation, Date and Submit to Search'
            default_company = "Enter Company Abbreviation"
            default_date = "Date (YYYY or YYYY-MM)"
            company = self.entry_var.get().strip()
            date = self.entry_var2.get().strip()
            if company == default_company or company == " ":
                self.label_message['fg'] = "red"
                self.label_message['text'] = 'Invalid Company Entry'
                self.tree.delete(*self.tree.get_children())
                return
            elif date == default_date or date == " ":
                df = self.method.monthly_report(company=company)
            else:
                year_pattern = r'^\d{4}$'
                year_month_pattern = r'^\d{4}-\d{2}$'
                if not (re.match(year_pattern, date) or re.match(year_month_pattern, date)):
                    raise ValueError
                df = self.method.monthly_report(company=company, date=date)
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
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = "Invalid date format"
            self.tree.delete(*self.tree.get_children())
