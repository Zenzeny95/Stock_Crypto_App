"""
PopupWindowSubscriptions - Subscriptions Management Window

This class defines a pop-up window for managing subscription data within an application's admin interface.

Methods:
    __init__(self, master, title):
        Initializes the pop-up window with a specified title and UI elements.

    on_entry_focus_in_search(self, event):
        Handles the focus in event for the search entry field.

    on_entry_focus_out_search(self, event):
        Handles the focus out event for the search entry field.

    on_entry_focus_in_id(self, event):
        Handles the focus in event for the ID entry field.

    on_entry_focus_out_id(self, event):
        Handles the focus out event for the ID entry field.

    on_entry_focus_in_payment(self, event):
        Handles the focus in event for the payment entry field.

    on_entry_focus_out_payment(self, event):
        Handles the focus out event for the payment entry field.

    on_entry_focus_in_date(self, event):
        Handles the focus in event for the date entry field.

    on_entry_focus_out_date(self, event):
        Handles the focus out event for the date entry field.

    on_tree_double_click(self, event):
        Handles the double-click event on the treeview.

    clear_entries(self):
        Clears the entry fields.

    tree_implementation(self, variable):
        Updates the treeview widget based on the provided data.

    display_all_subscriptions(self):
        Displays all subscription records in the treeview.

    search_subscriptions(self):
        Searches for subscription records based on the search query.

    update_subscriptions(self):
        Updates the selected subscription record with new values.
"""

import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk
from tkmacosx import Button as MacButton
from model import engine, Subscription, User
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Session = sessionmaker(bind=engine)


class PopupWindowSubscriptions(tk.Toplevel):
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
        self.columns = ['id', 'payment', 'date', 'user_id', 'username']

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/1200x880background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self, text='Here You Can Add, Update, Delete or Search Subscriptions',
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
        entry_search.place(x=800, y=610, width=266, height=40)

        self.entry_id_var = tk.StringVar()
        self.entry_id_var.set("ID")
        entry_id = tk.Entry(self, textvariable=self.entry_id_var, font=self.font, borderwidth="1px", fg="#ffffff",
                            justify="center", bg="grey")
        entry_id.place(x=450, y=510, width=266, height=40)

        self.entry_payment_var = tk.StringVar()
        self.entry_payment_var.set("Payment (True or False)")
        entry_payment = tk.Entry(self, textvariable=self.entry_payment_var, font=self.font, borderwidth="1px",
                                 fg="#ffffff", justify="center", bg="grey")
        entry_payment.place(x=450, y=560, width=266, height=40)

        self.entry_date_var = tk.StringVar()
        self.entry_date_var.set("Date of Payment")
        entry_date = tk.Entry(self, textvariable=self.entry_date_var, font=self.font, borderwidth="1px", fg="#ffffff",
                              justify="center", bg="grey")
        entry_date.place(x=450, y=610, width=266, height=40)

        # ENTRY BINDS
        entry_search.bind("<FocusIn>", self.on_entry_focus_in_search)
        entry_search.bind("<FocusOut>", self.on_entry_focus_out_search)
        entry_id.bind("<FocusIn>", self.on_entry_focus_in_id)
        entry_id.bind("<FocusOut>", self.on_entry_focus_out_id)
        entry_payment.bind("<FocusIn>", self.on_entry_focus_in_payment)
        entry_payment.bind("<FocusOut>", self.on_entry_focus_out_payment)
        entry_date.bind("<FocusIn>", self.on_entry_focus_in_date)
        entry_date.bind("<FocusOut>", self.on_entry_focus_out_date)

        self.tree.bind("<Double-1>", self.on_tree_double_click)

        # BUTTON
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        update_button = MacButton(self, text="Update", font=self.font, justify="center",
                                  command=self.update_subscriptions)
        search_button = MacButton(self, text="Search", font=self.font, justify="center",
                                  command=self.search_subscriptions)
        clear_button = MacButton(self, text="Clear", font=self.font, justify="center", command=self.clear_entries)
        search_button.place(x=800, y=665, width=266, height=55)
        update_button.place(x=450, y=665, width=266, height=55)
        clear_button.place(x=450, y=740, width=266, height=55)
        close_button.place(x=450, y=815, width=266, height=55)

        self.display_all_subscriptions()

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

    def on_entry_focus_in_payment(self, event):
        if self.entry_payment_var.get() == "Payment (True or False)":
            self.entry_payment_var.set("")

    def on_entry_focus_out_payment(self, event):
        if not self.entry_payment_var.get():
            self.entry_payment_var.set("Payment (True or False)")

    def on_entry_focus_in_date(self, event):
        if self.entry_date_var.get() == "Date of Payment":
            self.entry_date_var.set("")

    def on_entry_focus_out_date(self, event):
        if not self.entry_date_var.get():
            self.entry_date_var.set("Date of Payment")

    def on_tree_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(*selected_item)['values']
            if item_values:
                self.entry_id_var.set(item_values[0])
                self.entry_payment_var.set(item_values[1])
                self.entry_date_var.set(item_values[2])
        return

    def clear_entries(self):
        self.entry_search_var.set("Search")
        self.entry_id_var.set("ID")
        self.entry_payment_var.set("Payment (True or False)")
        self.entry_date_var.set("Date of Payment")
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
                         [
                             getattr(user, col_name.lower())
                             if col_name.lower() != 'username'
                             else getattr(user.usersubs, 'username')
                             for user in variable
                         ]), 100, )
                self.tree.column(col_name, width=col_width + 20, stretch=False)
            for user in variable:
                self.tree.insert("", tk.END, values=[
                    getattr(user, col_name.lower())
                    if col_name.lower() != 'username'
                    else getattr(user.usersubs, 'username')
                    for col_name in self.columns
                ])
            return
        except KeyError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found'
            self.tree.delete(*self.tree.get_children())
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = "Invalid Entry"
            self.tree.delete(*self.tree.get_children())

    def display_all_subscriptions(self):
        session = Session()
        subscriptions = session.query(Subscription).all()
        self.tree_implementation(subscriptions)
        session.close()
        return

    def search_subscriptions(self):
        search_text = self.entry_search_var.get().strip()
        if search_text == "Search":
            self.display_all_subscriptions()
            return
        session = Session()
        subscriptions = session.query(Subscription).filter(
            (Subscription.id.ilike(f'%{search_text}%')) |
            (Subscription.date.ilike(f'%{search_text}%')) |
            (Subscription.user_id.ilike(f'%{search_text}%')) |
            (Subscription.usersubs.has(User.username.ilike(f'%{search_text}%')))
        ).all()
        self.tree_implementation(subscriptions)
        session.close()
        return

    def update_subscriptions(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(*selected_item)['values']
            if item_values:
                new_id = self.entry_id_var.get()
                new_payment = self.entry_payment_var.get()
                if new_payment.lower() == 'true':
                    new_payment = True
                else:
                    new_payment = False
                new_date = self.entry_date_var.get()

                session = Session()
                subscription_to_update = session.query(Subscription).filter_by(id=item_values[0]).first()
                if subscription_to_update:
                    try:
                        if subscription_to_update.id != new_id:
                            subscription_to_update.id = new_id
                        if subscription_to_update.payment != new_payment:
                            subscription_to_update.payment = new_payment
                        if str(subscription_to_update.date) == new_date:
                            pass
                        elif new_date.lower().strip() == 'none':
                            subscription_to_update.date = None
                        else:
                            subscription_to_update.date = datetime.utcnow()
                        session.commit()
                        session.close()
                        self.display_all_subscriptions()
                        self.label_message['fg'] = "#296108"
                        self.label_message['text'] = 'Subscription Updated Succesfully'
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
