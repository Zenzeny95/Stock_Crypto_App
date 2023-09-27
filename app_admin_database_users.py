import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk
from tkmacosx import Button as MacButton
from model import engine, User, Password, Subscription
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Session = sessionmaker(bind=engine)


class PopupWindowUsers(tk.Toplevel):
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
        self.columns = ['id', 'name', 'username', 'email', 'dob', 'created']

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/1200x880background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # LABEL
        self.label_message = tk.Label(self, text='Here You Can Add, Update, Delete or Search Users',
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
        entry_search.place(x=800, y=600, width=266, height=40)

        self.entry_id_var = tk.StringVar()
        self.entry_id_var.set("ID")
        entry_id = tk.Entry(self, textvariable=self.entry_id_var, font=self.font, borderwidth="1px", fg="#ffffff",
                            justify="center", bg="grey")
        entry_id.place(x=50, y=520, width=320, height=40)

        self.entry_name_var = tk.StringVar()
        self.entry_name_var.set("Name")
        entry_name = tk.Entry(self, textvariable=self.entry_name_var, font=self.font, borderwidth="1px", fg="#ffffff",
                              justify="center", bg="grey")
        entry_name.place(x=50, y=570, width=320, height=40)

        self.entry_username_var = tk.StringVar()
        self.entry_username_var.set("Username")
        entry_username = tk.Entry(self, textvariable=self.entry_username_var, font=self.font, borderwidth="1px",
                                  fg="#ffffff", justify="center", bg="grey")
        entry_username.place(x=50, y=620, width=320, height=40)

        self.entry_email_var = tk.StringVar()
        self.entry_email_var.set("Email")
        entry_email = tk.Entry(self, textvariable=self.entry_email_var, font=self.font, borderwidth="1px", fg="#ffffff",
                               justify="center", bg="grey")
        entry_email.place(x=50, y=670, width=320, height=40)

        self.entry_dob_var = tk.StringVar()
        self.entry_dob_var.set("Date of Birth")
        entry_dob = tk.Entry(self, textvariable=self.entry_dob_var, font=self.font, borderwidth="1px", fg="#ffffff",
                             justify="center", bg="grey")
        entry_dob.place(x=50, y=720, width=320, height=40)

        self.entry_created_var = tk.StringVar()
        self.entry_created_var.set("User Created")
        entry_created = tk.Entry(self, textvariable=self.entry_created_var, font=self.font, borderwidth="1px",
                                 fg="#ffffff", justify="center", bg="grey")
        entry_created.place(x=50, y=770, width=320, height=40)

        self.entry_password_var = tk.StringVar()
        self.entry_password_var.set("Password (Only When Insert Used)")
        entry_password = tk.Entry(self, textvariable=self.entry_password_var, font=self.font, borderwidth="1px",
                                  fg="#ffffff", justify="center", bg="grey")
        entry_password.place(x=50, y=820, width=320, height=40)

        # ENTRY BINDS
        entry_search.bind("<FocusIn>", self.on_entry_focus_in_search)
        entry_search.bind("<FocusOut>", self.on_entry_focus_out_search)
        entry_id.bind("<FocusIn>", self.on_entry_focus_in_id)
        entry_id.bind("<FocusOut>", self.on_entry_focus_out_id)
        entry_name.bind("<FocusIn>", self.on_entry_focus_in_name)
        entry_name.bind("<FocusOut>", self.on_entry_focus_out_name)
        entry_username.bind("<FocusIn>", self.on_entry_focus_in_username)
        entry_username.bind("<FocusOut>", self.on_entry_focus_out_username)
        entry_email.bind("<FocusIn>", self.on_entry_focus_in_email)
        entry_email.bind("<FocusOut>", self.on_entry_focus_out_email)
        entry_dob.bind("<FocusIn>", self.on_entry_focus_in_dob)
        entry_dob.bind("<FocusOut>", self.on_entry_focus_out_dob)
        entry_created.bind("<FocusIn>", self.on_entry_focus_in_created)
        entry_created.bind("<FocusOut>", self.on_entry_focus_out_created)
        entry_password.bind("<FocusIn>", self.on_entry_focus_in_password)
        entry_password.bind("<FocusOut>", self.on_entry_focus_out_password)

        self.tree.bind("<Double-1>", self.on_tree_double_click)

        # BUTTON
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        delete_button = MacButton(self, text="Delete", font=self.font, justify="center", command=self.delete_users)
        update_button = MacButton(self, text="Update", font=self.font, justify="center", command=self.update_users)
        insert_button = MacButton(self, text="Insert", font=self.font, justify="center", command=self.insert_users)
        search_button = MacButton(self, text="Search", font=self.font, justify="center", command=self.search_users)
        clear_button = MacButton(self, text="Clear", font=self.font, justify="center", command=self.clear_entries)
        search_button.place(x=800, y=675, width=266, height=55)
        insert_button.place(x=450, y=515, width=266, height=55)
        update_button.place(x=450, y=585, width=266, height=55)
        delete_button.place(x=450, y=655, width=266, height=55)
        clear_button.place(x=450, y=725, width=266, height=55)
        close_button.place(x=450, y=805, width=266, height=55)

        self.display_all_users()

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

    def on_entry_focus_in_name(self, event):
        if self.entry_name_var.get() == "Name":
            self.entry_name_var.set("")

    def on_entry_focus_out_name(self, event):
        if not self.entry_name_var.get():
            self.entry_name_var.set("Name")

    def on_entry_focus_in_username(self, event):
        if self.entry_username_var.get() == "Username":
            self.entry_username_var.set("")

    def on_entry_focus_out_username(self, event):
        if not self.entry_username_var.get():
            self.entry_username_var.set("Username")

    def on_entry_focus_in_email(self, event):
        if self.entry_email_var.get() == "Email":
            self.entry_email_var.set("")

    def on_entry_focus_out_email(self, event):
        if not self.entry_email_var.get():
            self.entry_email_var.set("Email")

    def on_entry_focus_in_dob(self, event):
        if self.entry_dob_var.get() == "Date of Birth":
            self.entry_dob_var.set("")

    def on_entry_focus_out_dob(self, event):
        if not self.entry_dob_var.get():
            self.entry_dob_var.set("Date of Birth")

    def on_entry_focus_in_created(self, event):
        if self.entry_created_var.get() == "User Created":
            self.entry_created_var.set("")

    def on_entry_focus_out_created(self, event):
        if not self.entry_created_var.get():
            self.entry_created_var.set("User Created")

    def on_entry_focus_in_password(self, event):
        if self.entry_password_var.get() == "Password (Only When Insert Used)":
            self.entry_password_var.set("")

    def on_entry_focus_out_password(self, event):
        if not self.entry_password_var.get():
            self.entry_password_var.set("Password (Only When Insert Used)")

    def on_tree_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(*selected_item)['values']
            if item_values:
                self.entry_id_var.set(item_values[0])
                self.entry_name_var.set(item_values[1])
                self.entry_username_var.set(item_values[2])
                self.entry_email_var.set(item_values[3])
                self.entry_dob_var.set(item_values[4])
                self.entry_created_var.set(item_values[5])
        return

    @staticmethod
    def do_id_exists(session, new_id):
        user = session.query(User).filter_by(id=new_id).first()
        if user:
            return True
        return False

    @staticmethod
    def do_username_exists(session, new_username):
        user = session.query(User).filter_by(username=new_username).first()
        if user:
            return True
        return False

    @staticmethod
    def do_email_exists(session, new_email):
        user = session.query(User).filter_by(email=new_email).first()
        if user:
            return True
        return False

    def clear_entries(self):
        self.entry_search_var.set("Search")
        self.entry_id_var.set("ID")
        self.entry_name_var.set("Name")
        self.entry_username_var.set("Username")
        self.entry_email_var.set("Email")
        self.entry_dob_var.set("Date of Birth")
        self.entry_created_var.set("User Created")
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

    def display_all_users(self):
        session = Session()
        users = session.query(User).all()
        self.tree_implementation(users)
        session.close()
        return

    def search_users(self):
        search_text = self.entry_search_var.get().strip()
        if search_text == "Search":
            self.display_all_users()
            return
        session = Session()
        users = session.query(User).filter(
            (User.id.ilike(f'%{search_text}%')) |
            (User.name.ilike(f'%{search_text}%')) |
            (User.username.ilike(f'%{search_text}%')) |
            (User.email.ilike(f'%{search_text}%')) |
            (User.dob.ilike(f'%{search_text}%')) |
            (User.created.ilike(f'%{search_text}%'))
        ).all()
        self.tree_implementation(users)
        session.close()
        return

    def update_users(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(*selected_item)['values']
            if item_values:
                new_id = self.entry_id_var.get()
                new_name = self.entry_name_var.get()
                new_username = self.entry_username_var.get()
                new_email = self.entry_email_var.get()
                new_dob = self.entry_dob_var.get()
                new_created = self.entry_created_var.get()

                session = Session()
                user_to_update = session.query(User).filter_by(id=item_values[0]).first()
                if user_to_update:
                    if user_to_update.id != new_id and \
                            self.do_id_exists(session, new_id) is True:
                        self.label_message['fg'] = "red"
                        self.label_message['text'] = 'ID Exists'
                        session.close()
                        return
                    if user_to_update.username != new_username and \
                            self.do_username_exists(session, new_username) is True:
                        self.label_message['fg'] = "red"
                        self.label_message['text'] = 'Username Exists'
                        session.close()
                        return
                    if user_to_update.email != new_email and \
                            self.do_email_exists(session, new_email) is True:
                        self.label_message['fg'] = "red"
                        self.label_message['text'] = 'Email Exists'
                        session.close()
                        return
                    try:
                        if user_to_update.id != new_id:
                            user_to_update.id = new_id
                        if user_to_update.name != new_name:
                            user_to_update.name = new_name
                        if user_to_update.username != new_username:
                            user_to_update.username = new_username
                        if user_to_update.email != new_email:
                            user_to_update.email = new_email
                        if user_to_update.dob != new_dob:
                            user_to_update.dob = new_dob
                        new_created_date = datetime.strptime(new_created, '%Y-%m-%d %H:%M:%S.%f')
                        if user_to_update.created != new_created_date:
                            user_to_update.created = new_created_date
                        session.commit()
                        session.close()
                        self.tree.item(*selected_item, values=(new_id, new_name, new_username,
                                                               new_email, new_dob, new_created))
                        self.label_message['fg'] = "#296108"
                        self.label_message['text'] = 'User Updated Succesfully'
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

    def insert_users(self):
        new_id = self.entry_id_var.get()
        new_name = self.entry_name_var.get()
        new_username = self.entry_username_var.get()
        new_email = self.entry_email_var.get()
        new_dob = self.entry_dob_var.get()
        new_password = self.entry_password_var.get()
        if new_password == "Password (Only When Insert Used)":
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Password Provided'
            return
        new_created = self.entry_created_var.get()
        try:
            new_created = datetime.strptime(new_created, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Incorrect Creation Date Entry'
            return

        session = Session()
        if self.do_id_exists(session, new_id):
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'ID Exists'
            session.close()
            return
        if self.do_username_exists(session, new_username):
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Username Exists'
            session.close()
            return
        if self.do_email_exists(session, new_email):
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Email Exists'
            session.close()
            return
        try:
            new_user = User(
                id=new_id,
                name=new_name,
                username=new_username,
                email=new_email,
                dob=new_dob,
                created=new_created
            )

            session.add(new_user)

            new_user_password = Password(
                hash_password=new_password,
                userpass=new_user,
            )

            new_user_password.set_password(new_password)
            session.add(new_user_password)

            user_subscription = Subscription(
                payment=False,
                usersubs=new_user,
            )

            session.add(user_subscription)

            session.commit()
            session.close()

            self.tree.insert('', tk.END, values=(new_id, new_name, new_username, new_email, new_dob, new_created))
            self.clear_entries()

            self.label_message['fg'] = "#296108"
            self.label_message['text'] = 'User Inserted Succesfully'
            return
        except (AttributeError, KeyError, TypeError, ValueError):
            session.rollback()
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Insert Failed. Try Again'
            return

    def delete_users(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(*selected_item)['values']
            if item_values:
                user_id_to_delete = item_values[0]

                session = Session()
                user_to_delete = session.query(User).filter_by(id=user_id_to_delete).first()
                if user_to_delete:
                    try:
                        session.delete(user_to_delete)
                        session.commit()
                        session.close()

                        self.tree.delete(*selected_item)
                        self.clear_entries()

                        self.label_message['fg'] = "#296108"
                        self.label_message['text'] = 'User Deleted Succesfully'
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
