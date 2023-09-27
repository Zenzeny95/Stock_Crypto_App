"""
This Python file defines a pop-up window for displaying daily stock data using the tkinter library.
 The key components of this code include:

1. Importing necessary modules such as 'tkinter' for creating the GUI, 'tkmacosx.Button' for macOS-specific buttons,
 and other modules for accessing stock data and methods.

2. Defining a `StockDayPopupWindow` class that represents a pop-up window for daily stock data:
   - Initializes a pop-up window with a specified title.
   - Creates a GUI with a label, entry fields for company abbreviation and date, a submit button, and a close button.
   - Allows users to input a company abbreviation and a date in the format 'YYYY-MM-DD' to retrieve daily stock data.
   - Validates user inputs, checks for valid date formats,
    and ensures that the selected date is not a weekend (Saturday or Sunday).
   - Displays the retrieved stock data in a Treeview widget with column headings.

3. The code utilizes external methods and classes (e.g., `Methods`) to retrieve and display daily stock data.

4. The pop-up window's functionality includes error handling for various scenarios, such as invalid inputs,
 no data found for the company or day, and date format errors.

5. The pop-up window is displayed in a centered position on the screen and is not resizable.

6. Users can submit their queries to retrieve daily stock data for a specific company and date.

This code provides a user-friendly interface for retrieving and displaying daily stock data for
 a selected company and date.
"""

import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk
from tkmacosx import Button as MacButton
from datetime import datetime
from app_mixed_methods import Methods


class StockDayPopupWindow(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        self.label = tk.Label(self, font=("Helvetica", 16))
        self.label.pack(padx=20, pady=40)
        width = 1300
        height = 450
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.font_label = tk.font.Font(family="Helvetica", size=18)
        self.method = Methods()

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/1400x450background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self, text='Enter Company Abbreviation, Date and Submit to Search', anchor="n",
                                      justify="center", font=self.font_label, bg='SystemButtonFace',
                                      highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=450, y=30, width=472, height=40)

        # TREE
        self.tree = ttk.Treeview(self)
        self.tree['show'] = 'headings'
        self.tree.place(x=50, y=100, width=1195, height=80)

        # ENTRIES
        self.entry_var = tk.StringVar()
        self.entry_var.set("Enter Company Abbreviation")
        entry = tk.Entry(self, textvariable=self.entry_var, font=self.font, borderwidth="1px", fg="#ffffff",
                         justify="center", bg="grey")
        entry.place(x=548, y=210, width=205, height=40)

        self.entry_var2 = tk.StringVar()
        self.entry_var2.set("Date (YYYY-MM-DD)")

        entry2 = tk.Entry(self, textvariable=self.entry_var2, font=self.font, borderwidth="1px", fg="#ffffff",
                          justify="center", bg="grey")
        entry2.place(x=548, y=260, width=205, height=40)

        # ENTRY BINDS
        entry.bind("<FocusIn>", self.on_entry_focus_in1)
        entry.bind("<FocusOut>", self.on_entry_focus_out1)

        entry2.bind("<FocusIn>", self.on_entry_focus_in2)
        entry2.bind("<FocusOut>", self.on_entry_focus_out2)

        # BUTTON
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        submit_button = MacButton(self, text="Submit", font=self.font, justify="center", command=self.refresh_results)
        submit_button.place(x=550, y=320, width=200, height=50)
        close_button.place(x=550, y=380, width=200, height=50)

    def on_entry_focus_in1(self, event):
        if self.entry_var.get() == "Enter Company Abbreviation":
            self.entry_var.set("")

    def on_entry_focus_out1(self, event):
        if not self.entry_var.get():
            self.entry_var.set("Enter Company Abbreviation")

    def on_entry_focus_in2(self, event):
        if self.entry_var2.get() == "Date (YYYY-MM-DD)":
            self.entry_var2.set("")

    def on_entry_focus_out2(self, event):
        if not self.entry_var2.get():
            self.entry_var2.set("Date (YYYY-MM-DD)")

    def refresh_results(self):
        try:
            self.label_message['fg'] = "#0E82D3"
            self.label_message['text'] = 'Enter Company Abbreviation, Date and Submit to Search'
            company = self.entry_var.get()
            date = self.entry_var2.get()
            if company.strip() == "Enter Company Abbreviation" or company.strip() == "":
                self.label_message['fg'] = "red"
                self.label_message['text'] = 'Invalid Company Entry'
                self.tree.delete(*self.tree.get_children())
                return
            if date.strip() == "" or date.strip() == "Date (YYYY-MM-DD)":
                self.label_message['fg'] = "red"
                self.label_message['text'] = 'Invalid Date Entry'
                self.tree.delete(*self.tree.get_children())
                return
            date_list = date.split("-")
            if len(date_list) != 3:
                raise TypeError
            for date_elem in date_list:
                if not date_elem.isdigit():
                    raise TypeError
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
            else:
                df = self.method.daily_average(company=company, month=date)
                self.tree.delete(*self.tree.get_children())
                self.tree["columns"] = df.columns.to_list()
                for col_name in df.columns:
                    self.tree.heading(col_name, text=col_name)
                    col_width = max(
                        tkFont.Font().measure(str(col_name)),
                        *df[col_name].apply(lambda x: tkFont.Font().measure(str(x))), 100,)
                    self.tree.column(col_name, width=col_width + 20, stretch=False)
                for index, row in df.iterrows():
                    self.tree.insert("", tk.END, values=row.to_list())
        except KeyError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found For This Company'
            self.tree.delete(*self.tree.get_children())
        except AttributeError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found For This Day'
            self.tree.delete(*self.tree.get_children())
        except TypeError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Date Format Invalid'
            self.tree.delete(*self.tree.get_children())
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Date Format Invalid'
            self.tree.delete(*self.tree.get_children())
