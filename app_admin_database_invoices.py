"""
PopupWindowInvoices - Invoice Management GUI

This class defines a graphical user interface (GUI) window for managing invoices. Users can add, update, delete,
 and search for invoices within the application.

Methods:
    __init__(self, master, title):
        Initializes the PopupWindowInvoices class with the specified master widget and title.

    on_entry_focus_in_search(self, event):
        Handles the event when the search entry field gains focus.

    on_entry_focus_out_search(self, event):
        Handles the event when the search entry field loses focus.

    on_entry_focus_in_id(self, event):
        Handles the event when the ID entry field gains focus.

    on_entry_focus_out_id(self, event):
        Handles the event when the ID entry field loses focus.

    on_entry_focus_in_username(self, event):
        Handles the event when the username entry field gains focus.

    on_entry_focus_out_username(self, event):
        Handles the event when the username entry field loses focus.

    on_entry_focus_in_date(self, event):
        Handles the event when the date entry field gains focus.

    on_entry_focus_out_date(self, event):
        Handles the event when the date entry field loses focus.

    on_tree_double_click(self, event):
        Handles the event when an item in the tree view is double-clicked.

    do_id_exists(session, new_id):
        Checks if an invoice with a given ID exists in the database.

    clear_entries(self):
        Clears the entry fields in the GUI.

    tree_implementation(self, variable):
        Populates the tree view with data from the provided variable.

    display_all_invoices(self):
        Displays all invoices in the GUI.

    search_invoices(self):
        Searches for invoices based on the entered search text.

    update_invoices(self):
        Updates the selected invoice with new information.

    insert_invoices(self):
        Inserts a new invoice into the database.

    delete_invoices(self):
        Deletes the selected invoice from the database.
"""

import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk
from tkmacosx import Button as MacButton
from model import engine, Invoice
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Session = sessionmaker(bind=engine)


class PopupWindowInvoices(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        self.label = tk.Label(self, font=("Helvetica", 16))
        self.label.pack(padx=20, pady=40)
        width = 1200
        height = 880
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.font_label = tk.font.Font(family="Helvetica", size=18)
        self.columns = ['id', 'username', 'date']

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/1200x880background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self, text='Here You Can Add, Update, Delete or Search Invoices',
                                      anchor="n", justify="center", font=self.font_label, bg='SystemButtonFace',
                                      highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=320, y=30, width=550, height=40)

        # TREE FRAME
        tree_frame = tk.Frame(self)
        tree_frame.place(x=75, y=90, width=1050, height=400)

        # TREE
        self.tree = ttk.Treeview(self)
        self.tree['show'] = 'headings'
        self.tree.place(x=75, y=90, width=1050, height=400)

        # SCROLLBAR
        self.tree_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar2 = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree_scrollbar.place(x=1110, y=90, height=400)
        self.tree_scrollbar2.place(x=75, y=475, width=1030)
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set, xscrollcommand=self.tree_scrollbar2.set)

        # ENTRIES
        self.entry_search_var = tk.StringVar()
        self.entry_search_var.set("Search")
        entry_search = tk.Entry(self, textvariable=self.entry_search_var, font=self.font, borderwidth="1px",
                                fg="#ffffff", justify="center", bg="grey")
        entry_search.place(x=50, y=670, width=320, height=40)

        self.entry_id_var = tk.StringVar()
        self.entry_id_var.set("ID")
        entry_id = tk.Entry(self, textvariable=self.entry_id_var, font=self.font, borderwidth="1px", fg="#ffffff",
                            justify="center", bg="grey")
        entry_id.place(x=50, y=520, width=320, height=40)

        self.entry_username_var = tk.StringVar()
        self.entry_username_var.set("Username")
        entry_username = tk.Entry(self, textvariable=self.entry_username_var, font=self.font, borderwidth="1px",
                                  fg="#ffffff", justify="center", bg="grey")
        entry_username.place(x=50, y=570, width=320, height=40)

        self.entry_date_var = tk.StringVar()
        self.entry_date_var.set("Invoice Date")
        entry_date = tk.Entry(self, textvariable=self.entry_date_var, font=self.font, borderwidth="1px", fg="#ffffff",
                              justify="center", bg="grey")
        entry_date.place(x=50, y=620, width=320, height=40)

        # ENTRY BINDS
        entry_search.bind("<FocusIn>", self.on_entry_focus_in_search)
        entry_search.bind("<FocusOut>", self.on_entry_focus_out_search)
        entry_id.bind("<FocusIn>", self.on_entry_focus_in_id)
        entry_id.bind("<FocusOut>", self.on_entry_focus_out_id)
        entry_username.bind("<FocusIn>", self.on_entry_focus_in_username)
        entry_username.bind("<FocusOut>", self.on_entry_focus_out_username)
        entry_date.bind("<FocusIn>", self.on_entry_focus_in_date)
        entry_date.bind("<FocusOut>", self.on_entry_focus_out_date)

        self.tree.bind("<Double-1>", self.on_tree_double_click)

        # BUTTON
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        delete_button = MacButton(self, text="Delete", font=self.font, justify="center", command=self.delete_invoices)
        update_button = MacButton(self, text="Update", font=self.font, justify="center", command=self.update_invoices)
        insert_button = MacButton(self, text="Insert", font=self.font, justify="center", command=self.insert_invoices)
        search_button = MacButton(self, text="Search", font=self.font, justify="center", command=self.search_invoices)
        clear_button = MacButton(self, text="Clear", font=self.font, justify="center", command=self.clear_entries)
        search_button.place(x=50, y=720, width=320, height=55)
        insert_button.place(x=450, y=515, width=266, height=55)
        update_button.place(x=450, y=585, width=266, height=55)
        delete_button.place(x=450, y=655, width=266, height=55)
        clear_button.place(x=450, y=725, width=266, height=55)
        close_button.place(x=450, y=805, width=266, height=55)

        self.display_all_invoices()

    def on_entry_focus_in_search(self, event):
        if self.entry_search_var.get() == "Search":
            self.entry_search_var.set("")

    def on_entry_focus_out_search(self, event):
        if not self.entry_search_var.get():
            self.entry_search_var.set("Search")

    def on_entry_focus_in_id(self, event):
        if self.entry_id_var.get() == "ID":
            self.entry_id_var.set("")

    def on_entry_focus_out_id(self, event):
        if not self.entry_id_var.get():
            self.entry_id_var.set("ID")

    def on_entry_focus_in_username(self, event):
        if self.entry_username_var.get() == "Username":
            self.entry_username_var.set("")

    def on_entry_focus_out_username(self, event):
        if not self.entry_username_var.get():
            self.entry_username_var.set("Username")

    def on_entry_focus_in_date(self, event):
        if self.entry_date_var.get() == "Invoice Date":
            self.entry_date_var.set("")

    def on_entry_focus_out_date(self, event):
        if not self.entry_date_var.get():
            self.entry_date_var.set("Invoice Date")

    def on_tree_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(*selected_item)['values']
            if item_values:
                self.entry_id_var.set(item_values[0])
                self.entry_username_var.set(item_values[1])
                self.entry_date_var.set(item_values[2])
        return

    @staticmethod
    def do_id_exists(session, new_id):
        invoice = session.query(Invoice).filter_by(id=new_id).first()
        if invoice:
            return True
        return False

    def clear_entries(self):
        self.entry_search_var.set("Search")
        self.entry_id_var.set("ID")
        self.entry_username_var.set("Username")
        self.entry_date_var.set("Invoice Date")
        return

    def tree_implementation(self, variable):
        try:
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = self.columns
            for col_name in self.columns:
                self.tree.heading(col_name, text=col_name)
                col_width = max(
                    tkFont.Font().measure(str(col_name)),
                    *map(lambda x: tkFont.Font().measure(str(x)),
                         [getattr(user, col_name.lower()) for user in variable]), 100, )
                self.tree.column(col_name, width=col_width + 20, stretch=False)
            for user in variable:
                self.tree.insert("", tk.END, values=[getattr(user, col_name.lower()) for col_name in self.columns])
            return
        except KeyError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found'
            self.tree.delete(*self.tree.get_children())
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = "Invalid Entry"
            self.tree.delete(*self.tree.get_children())

    def display_all_invoices(self):
        session = Session()
        users = session.query(Invoice).all()
        self.tree_implementation(users)
        session.close()
        return

    def search_invoices(self):
        search_text = self.entry_search_var.get().strip()
        if search_text == "Search":
            self.display_all_invoices()
            return
        session = Session()
        invoices = session.query(Invoice).filter(
            (Invoice.id.ilike(f'%{search_text}%')) |
            (Invoice.username.ilike(f'%{search_text}%')) |
            (Invoice.date.ilike(f'%{search_text}%'))
        ).all()
        self.tree_implementation(invoices)
        session.close()
        return

    def update_invoices(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(*selected_item)['values']
            if item_values:
                new_id = self.entry_id_var.get()
                new_username = self.entry_username_var.get()
                new_date = self.entry_date_var.get()

                session = Session()
                invoice_to_update = session.query(Invoice).filter_by(id=item_values[0]).first()
                if invoice_to_update:
                    if invoice_to_update.id != new_id and\
                            self.do_id_exists(session, new_id) is True:
                        self.label_message['fg'] = "red"
                        self.label_message['text'] = 'ID Exists'
                        session.close()
                        return
                    try:
                        if invoice_to_update.id != new_id:
                            invoice_to_update.id = new_id
                        if invoice_to_update.username != new_username:
                            invoice_to_update.username = new_username
                        if str(invoice_to_update.date) == new_date:
                            pass
                        elif new_date.lower().strip() == 'none':
                            invoice_to_update.date = None
                        else:
                            invoice_to_update.date = datetime.utcnow()
                        session.commit()
                        session.close()
                        self.tree.item(*selected_item, values=(new_id, new_username, new_date))
                        self.label_message['fg'] = "#296108"
                        self.label_message['text'] = 'Invoice Updated Succesfully'
                        return
                    except (AttributeError, KeyError, TypeError, ValueError):
                        session.rollback()
                        self.label_message['fg'] = "red"
                        self.label_message['text'] = 'Update Failed. Try Again'
                        return
                else:
                    self.label_message['fg'] = "red"
                    self.label_message['text'] = 'User Not Found'
                    return

    def insert_invoices(self):
        new_id = self.entry_id_var.get()
        new_username = self.entry_username_var.get()
        try:
            if self.entry_date_var.get() and self.entry_date_var.get() != 'Invoice Date':
                self.new_date = self.entry_date_var.get()
                self.new_date = datetime.strptime(self.new_date, '%Y-%m-%d %H:%M:%S.%f')
            else:
                self.new_date = datetime.now()
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Incorrect Date Format'

        session = Session()
        if self.do_id_exists(session, new_id):
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'ID Exists'
            session.close()
            return
        try:
            new_invoice = Invoice(
                id=new_id,
                username=new_username,
                date=self.new_date,
            )

            session.add(new_invoice)
            session.commit()

            self.tree.insert('', tk.END, values=(new_id, new_username, self.new_date))
            self.clear_entries()

            self.label_message['fg'] = "#296108"
            self.label_message['text'] = 'Invoice Inserted Succesfully'
            return
        except Exception as e:
            print(f"Exception occurred: {e}")
            session.rollback()
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Insert Failed. Try Again'
            return

    def delete_invoices(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(*selected_item)['values']
            if item_values:
                user_id_to_delete = item_values[0]

                session = Session()
                invoice_to_delete = session.query(Invoice).filter_by(id=user_id_to_delete).first()
                if invoice_to_delete:
                    try:
                        session.delete(invoice_to_delete)
                        session.commit()
                        session.close()

                        self.tree.delete(*selected_item)
                        self.clear_entries()

                        self.label_message['fg'] = "#296108"
                        self.label_message['text'] = 'Invoice Deleted Succesfully'
                        return
                    except (AttributeError, KeyError, TypeError, ValueError):
                        session.rollback()
                        self.label_message['fg'] = "red"
                        self.label_message['text'] = 'Deletion Failed. Try Again'
                        return
                else:
                    self.label_message['fg'] = "red"
                    self.label_message['text'] = 'User Not Found'
                    return
