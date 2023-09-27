"""
The 'InvestmentGLPopupWindow' class represents a Tkinter popup window for investment gain/loss calculation.

Class Methods:
- '__init__(self, master, title)': Initializes a new 'InvestmentGLPopupWindow' instance.
    - 'master': The master Tkinter window to which this popup is associated.
    - 'title': The title of the popup window.

Methods:
- 'submited_data(self)': Validates and processes user-submitted data for investment gain/loss calculation.

Note:
- This class represents a Tkinter popup window for investment gain/loss calculation.
- Users can enter investment details, including sum, date, stock, and crypto.
- The gain/loss calculation result is displayed in a label within the popup window.
- Data validation is performed to ensure the entered values are valid for calculation.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
from datetime import datetime
from app_mixed_methods import Methods


class InvestmentGLPopupWindow(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        width = 600
        height = 300
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.default_crypto = 'Crypto Abbreviation'
        self.default_stock = 'Stock Abbreviation'
        self.method = Methods()

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/600x300background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # BUTTONS
        submit_button = MacButton(self, font=self.font, justify='center', text='Submit', command=self.submited_data)
        close_button = MacButton(self, font=self.font, justify='center', text='Close Window', command=self.destroy)
        submit_button.place(x=60, y=230, width=176, height=50)
        close_button.place(x=370, y=230, width=176, height=50)

        # ENTRIES
        self.entry_sum_var = tk.StringVar()
        self.entry_sum_var.set('Investment Sum ($)')
        self.entry_sum = tk.Entry(self, textvariable=self.entry_sum_var, borderwidth='1px', font=self.font,
                                  justify='center', bg='grey')
        self.entry_sum.place(x=20, y=20, width=247, height=30)

        self.entry_date_var = tk.StringVar()
        self.entry_date_var.set('Investment Date (YYYY-MM-DD)')
        self.entry_date = tk.Entry(self, textvariable=self.entry_date_var, borderwidth='1px', font=self.font,
                                   justify='center', bg='grey')
        self.entry_date.place(x=20, y=70, width=247, height=30)

        self.entry_stock_var = tk.StringVar()
        self.entry_stock_var.set('Stock Abbreviation')
        self.entry_stock = tk.Entry(self, textvariable=self.entry_stock_var, borderwidth='1px', font=self.font,
                                    justify='center', bg='grey')
        self.entry_stock.place(x=20, y=120, width=247, height=32)

        self.entry_crypto_var = tk.StringVar()
        self.entry_crypto_var.set('Crypto Abbreviation')
        self.entry_crypto = tk.Entry(self, textvariable=self.entry_crypto_var, borderwidth='1px', font=self.font,
                                     justify='center', bg='grey')
        self.entry_crypto.place(x=20, y=180, width=247, height=30)

        # Binds
        self.entry_sum.bind("<FocusIn>", self.on_entry_focus_in_sum)
        self.entry_sum.bind("<FocusOut>", self.on_entry_focus_out_sum)
        self.entry_crypto.bind("<FocusIn>", self.on_entry_focus_in_crypto)
        self.entry_crypto.bind("<FocusOut>", self.on_entry_focus_out_crypto)
        self.entry_date.bind("<FocusIn>", self.on_entry_focus_in_date)
        self.entry_date.bind("<FocusOut>", self.on_entry_focus_out_date)
        self.entry_stock.bind("<FocusIn>", self.on_entry_focus_in_stock)
        self.entry_stock.bind("<FocusOut>", self.on_entry_focus_out_stock)
        self.entry_stock.bind("<Key>", self.on_entry_key_stock)
        self.entry_crypto.bind("<Key>", self.on_entry_key_crypto)
        self.entry_stock.bind("<FocusOut>", self.on_entry_focus_out_st)
        self.entry_crypto.bind("<FocusOut>", self.on_entry_focus_out_cr)

        # LABELS
        label_or = tk.Label(self, font=self.font, justify='center', text="OR", fg='black', bg='#F1EFEF')
        self.label_result = tk.Label(self, font=self.font, justify='center', text='', fg='#0E82D3', bg='#F1EFEF')
        label_or.place(x=40, y=155, width=205, height=20)
        self.label_result.place(x=300, y=20, width=260, height=172)

    def on_entry_focus_in_sum(self, event):
        if self.entry_sum_var.get() == 'Investment Sum ($)':
            self.entry_sum_var.set('')

    def on_entry_focus_out_sum(self, event):
        if not self.entry_sum_var.get():
            self.entry_sum_var.set('Investment Sum ($)')

    def on_entry_focus_in_crypto(self, event):
        if self.entry_crypto_var.get() == 'Crypto Abbreviation':
            self.entry_crypto_var.set('')

    def on_entry_focus_out_crypto(self, event):
        if not self.entry_crypto_var.get():
            self.entry_crypto_var.set('Crypto Abbreviation')

    def on_entry_focus_in_date(self, event):
        if self.entry_date_var.get() == 'Investment Date (YYYY-MM-DD)':
            self.entry_date_var.set('')

    def on_entry_focus_out_date(self, event):
        if not self.entry_date_var.get():
            self.entry_date_var.set('Investment Date (YYYY-MM-DD)')

    def on_entry_focus_in_stock(self, event):
        if self.entry_stock_var.get() == 'Stock Abbreviation':
            self.entry_stock_var.set('')

    def on_entry_focus_out_stock(self, event):
        if not self.entry_stock_var.get():
            self.entry_stock_var.set('Stock Abbreviation')

    def on_entry_key_stock(self, event):
        self.entry_crypto.config(state="disabled")

    def on_entry_focus_out_st(self, event):
        if not self.entry_stock.get():
            self.entry_stock.delete(0, "end")
            self.entry_stock.insert(0, self.default_stock)
        if self.entry_stock_var.get() == self.default_stock:
            self.entry_crypto.config(state="normal")

    def on_entry_key_crypto(self, event):
        self.entry_stock.config(state="disabled")

    def on_entry_focus_out_cr(self, event):
        if not self.entry_crypto.get():
            self.entry_crypto.delete(0, "end")
            self.entry_crypto.insert(0, self.default_crypto)
        if self.entry_crypto_var.get() == self.default_crypto:
            self.entry_stock.config(state="normal")

    def submited_data(self):
        try:
            amount = self.entry_sum_var.get()
            date = self.entry_date_var.get()
            stock = self.entry_stock_var.get()
            crypto = self.entry_crypto_var.get()
            if float(amount) <= 0:
                raise ValueError("Amount Has To Be More Than 0")
            date_list = date.split("-")
            for date_elem in date_list:
                if not date_elem.isdigit():
                    raise TypeError("Date Is Invalid")
            if len(date_list) == 3:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                weekend = datetime.weekday(date_obj)
                if weekend == 5:
                    self.label_result['fg'] = "red"
                    self.label_result['text'] = 'Selected day is Saturday'
                    return
                elif weekend == 6:
                    self.label_result['fg'] = "red"
                    self.label_result['text'] = 'Selected day is Sunday'
                    return
            if crypto == self.default_crypto or crypto == " ":
                skaiciavimas = self.method.calculate_investment_gain_loss(amount=float(amount),
                                                                          start_date=date, stock=stock)
                if skaiciavimas['pel_nuo'] > 0:
                    self.label_result['fg'] = '#0E82D3'
                    self.label_result['text'] = f"Investment of {amount}$ on {date}\n" \
                                                f"Purchase {stock} shares - {skaiciavimas['akcijos']:.2f} units\n" \
                                                f"Current shares value - {skaiciavimas['dabartine']:.2f}$\n" \
                                                f"Profit - {skaiciavimas['pel_nuo']:.2f}$"
                elif skaiciavimas['pel_nuo'] < 0:
                    self.label_result['fg'] = '#0E82D3'
                    self.label_result['text'] = f"Investment of  {amount}$ on {date}\n" \
                                                f"Purchase {stock} shares - {skaiciavimas['akcijos']:.2f} units\n" \
                                                f"Current shares value - {skaiciavimas['dabartine']:.2f}$\n" \
                                                f"Loss - {skaiciavimas['pel_nuo']:.2f}$"
                else:
                    self.label_result['fg'] = '#0E82D3'
                    self.label_result['text'] = f"Investment of  {amount}$ on {date}\n" \
                                                f"Purchase {stock} shares - {skaiciavimas['akcijos']:.2f} units\n" \
                                                f"Current shares value - {skaiciavimas['dabartine']:.2f}$\n" \
                                                f"Same value"
            elif stock == self.default_stock or stock == " ":
                skaiciavimas = self.method.calculate_investment_gain_loss(amount=float(amount),
                                                                          start_date=date, crypto=crypto)
                if skaiciavimas['pel_nuo'] > 0:
                    self.label_result['fg'] = '#0E82D3'
                    self.label_result['text'] = f"Investment of  {amount}$ on {date}\n" \
                                                f"Purchase {crypto} coins - {skaiciavimas['zetonai']:.2f} units\n" \
                                                f"Current coins value- {skaiciavimas['dabartine']:.2f}$\n" \
                                                f"Profit - {skaiciavimas['pel_nuo']:.2f}$"
                elif skaiciavimas['pel_nuo'] < 0:
                    self.label_result['fg'] = '#0E82D3'
                    self.label_result['text'] = f"Investment of  {amount}$ on {date}\n" \
                                                f"Purchase {crypto} coins - {skaiciavimas['zetonai']:.2f} units\n" \
                                                f"Current coins value - {skaiciavimas['dabartine']:.2f}$\n" \
                                                f"Loss - {skaiciavimas['pel_nuo']:.2f}$"
                else:
                    self.label_result['fg'] = '#0E82D3'
                    self.label_result['text'] = f"Investment of  {amount}$ on {date}\n" \
                                                f"Purchase {crypto} coins - {skaiciavimas['zetonai']:.2f} units\n" \
                                                f"Current coins value - {skaiciavimas['dabartine']:.2f}$\n" \
                                                f"Same value"
        except KeyError:
            self.label_result['fg'] = "red"
            self.label_result['text'] = "Invalid Entry"
        except ValueError:
            self.label_result['fg'] = "red"
            self.label_result['text'] = "Invalid Entry"
        except TypeError:
            self.label_result['fg'] = "red"
            self.label_result['text'] = "Invalid Entry"
        except (IndexError, AttributeError):
            self.label_result['fg'] = "red"
            self.label_result['text'] = "No Data"
