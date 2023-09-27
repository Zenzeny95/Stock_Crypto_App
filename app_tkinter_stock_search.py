"""
This Python file defines a pop-up window for searching and displaying stock data using the tkinter library.
 The key components of this code include:

1. Importing necessary modules such as 'tkinter' for creating the GUI, 'app_mixed_methods' for accessing stock data
 and methods, and 'pandas' for data manipulation.

2. Defining a `SearchPopupWindow` class that represents a pop-up window for searching and displaying stock data:
   - Initializes a pop-up window with a specified title.
   - Creates a GUI with labels, an entry field for entering a company abbreviation, a submit button, and a close button.
   - Allows users to input a company abbreviation and search for stock data.
   - Validates user inputs, handling cases where inputs are missing or invalid.
   - Displays the retrieved stock data in a treeview widget.

3. The code utilizes external methods and classes (e.g., `Methods`) to search for stock data based on
 the provided company abbreviation.

4. The pop-up window's functionality includes error handling for scenarios where no data is found
 or the company abbreviation is invalid.

5. The pop-up window is displayed in a centered position on the screen and is not resizable.

6. Users can submit their queries to search for and display stock data for a specific company.

This code provides a user-friendly interface for searching and displaying stock data based on a company abbreviation.
"""

import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk
from tkmacosx import Button as MacButton
from app_mixed_methods import Methods, pd


class SearchPopupWindow(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        self.label = tk.Label(self, font=("Helvetica", 16))
        self.label.pack(padx=20, pady=40)
        width = 1400
        height = 550
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.font_label = tk.font.Font(family="Helvetica", size=18)
        self.method = Methods()

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/1450x550background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self, text='Enter Company Abbreviation, Date, Interval and Submit to Search',
                                      anchor="n", justify="center", font=self.font_label, bg='SystemButtonFace',
                                      highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=450, y=30, width=550, height=40)

        # TREE
        self.tree = ttk.Treeview(self)
        self.tree['show'] = 'headings'
        self.tree.place(x=50, y=100, width=1300, height=254)

        # SCROLLBAR
        self.tree_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar.place(x=1350, y=100, height=254)
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)

        # ENTRY
        self.entry_var = tk.StringVar()
        self.entry_var.set("Enter Company Abbreviation")
        entry = tk.Entry(self, textvariable=self.entry_var, font=self.font, borderwidth="1px", fg="#ffffff",
                         justify="center", bg="grey")
        entry.place(x=570, y=370, width=265, height=40)

        # ENTRY BINDS
        entry.bind("<FocusIn>", self.on_entry_focus_in)
        entry.bind("<FocusOut>", self.on_entry_focus_out)

        # BUTTON
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        submit_button = MacButton(self, text="Submit", font=self.font, justify="center", command=self.refresh_results)
        submit_button.place(x=570, y=420, width=266, height=50)
        close_button.place(x=570, y=480, width=266, height=50)

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
            default_company = "Enter Company Abbreviation"
            company = self.entry_var.get()
            if company == default_company or company == " ":
                self.label_message['fg'] = "red"
                self.label_message['text'] = 'Invalid Company Entry'
                self.tree.delete(*self.tree.get_children())
                return
            df = pd.DataFrame(self.method.search(company.upper()))
            if df.empty:
                raise KeyError
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
            self.label_message['text'] = 'No Data Found'
            self.tree.delete(*self.tree.get_children())
            return
