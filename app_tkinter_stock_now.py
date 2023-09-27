"""
This Python file defines a pop-up window for displaying real-time stock data using the tkinter library.
 The key components of this code include:

1. Importing necessary modules such as 'tkinter' for creating the GUI, 'app_mixed_methods' for accessing stock data
and methods, and other GUI-related modules.

2. Defining a `StockNowPopupWindow` class that represents a pop-up window for real-time stock data:
   - Initializes a pop-up window with a specified title.
   - Creates a GUI with a label, an entry field for company abbreviation, a submit button, and a close button.
   - Allows users to input a company abbreviation and retrieve real-time stock data for that company.
   - Validates user inputs and handles cases where inputs are missing or invalid.
   - Displays the real-time stock data in a treeview widget.

3. The code utilizes external methods and classes (e.g., `Methods`) to retrieve real-time stock data
 for a specified company.

4. The pop-up window's functionality includes error handling for scenarios where no data is found
 for the provided company.

5. The pop-up window is displayed in a centered position on the screen and is not resizable.

6. Users can submit their queries to retrieve real-time stock data for a specific company.

This code provides a user-friendly interface for retrieving and displaying real-time stock data for a selected company.
"""

import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk
from tkmacosx import Button as MacButton
from app_mixed_methods import Methods


class StockNowPopupWindow(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        self.label = tk.Label(self, font=("Helvetica", 16))
        self.label.pack(padx=20, pady=40)
        width = 1000
        height = 400
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.font_label = tk.font.Font(family="Helvetica", size=18)
        self.method = Methods()

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/1000x400background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self, text='Enter Company Abbreviation and Submit to Search', anchor="n",
                                      justify="center", font=self.font_label, bg='SystemButtonFace',
                                      highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=260, y=30, width=472, height=40)

        # TREE
        self.tree = ttk.Treeview(self)
        self.tree['show'] = 'headings'
        self.tree.place(x=30, y=80, width=950, height=80)

        # ENTRY
        self.entry_var = tk.StringVar()
        self.entry_var.set("Enter Company Abbreviation")
        entry = tk.Entry(self, textvariable=self.entry_var, font=self.font, borderwidth="1px", fg="#ffffff",
                         justify="center", bg="grey")
        entry.place(x=400, y=220, width=205, height=40)

        # ENTRY BINDS
        entry.bind("<FocusIn>", self.on_entry_focus_in)
        entry.bind("<FocusOut>", self.on_entry_focus_out)

        # BUTTON
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        submit_button = MacButton(self, text="Submit", font=self.font, justify="center", command=self.refresh_results)
        submit_button.place(x=400, y=270, width=200, height=50)
        close_button.place(x=400, y=330, width=200, height=50)

    def on_entry_focus_in(self, event):
        if self.entry_var.get() == "Enter Company Abbreviation":
            self.entry_var.set("")

    def on_entry_focus_out(self, event):
        if not self.entry_var.get():
            self.entry_var.set("Enter Company Abbreviation")

    def refresh_results(self):
        try:
            self.label_message['fg'] = "#0E82D3"
            self.label_message['text'] = 'Enter Company Abbreviation and Submit to Search'
            search = self.entry_var.get().upper()
            result = self.method.now_data_company(search)
            result = result.drop('symbol', axis=1)
            df = result.drop('latestDay', axis=1)
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
            return
        except KeyError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found For This Company'
            self.tree.delete(*self.tree.get_children())
