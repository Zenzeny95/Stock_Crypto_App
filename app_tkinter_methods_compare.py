"""
The 'InvestmentsComaprePopupWindow' class represents a Tkinter popup window for comparing investments.

Class Methods:
- '__init__(self, master, title)': Initializes a new 'InvestmentsComaprePopupWindow' instance.
    - 'master': The master Tkinter window to which this popup is associated.
    - 'title': The title of the popup window.

Methods:
- 'submited_data(self)': Validates and processes user-submitted data for comparing investments.

Note:
- This class represents a Tkinter popup window for comparing investments using various parameters.
- It includes methods for handling user interactions, such as focus events and data submission.
- Users can compare investments in stocks and cryptocurrencies based on their inputs.
- The comparison results are displayed in a label within the popup window.
- Data validation is performed to ensure the entered values are valid for comparison.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
from datetime import datetime
from app_mixed_methods import Methods


class InvestmentsComaprePopupWindow(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        width = 600
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.default_crypto1 = 'Crypto Abbreviation1'
        self.default_stock1 = 'Stock Abbreviation1'
        self.default_crypto2 = 'Crypto Abbreviation2'
        self.default_stock2 = 'Stock Abbreviation2'
        self.method = Methods()

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/600x600background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # BUTTONS
        submit_button = MacButton(self, font=self.font, justify='center', text='Submit', command=self.submited_data)
        close_button = MacButton(self, font=self.font, justify='center', text='Close Window', command=self.destroy)
        submit_button.place(x=210, y=370, width=176, height=50)
        close_button.place(x=210, y=430, width=176, height=50)

        # ENTRIES
        self.entry_sum_var = tk.StringVar()
        self.entry_sum_var.set('Investment Sum ($)')
        self.entry_sum = tk.Entry(self, textvariable=self.entry_sum_var, borderwidth='1px', font=self.font,
                                  justify='center', bg='grey')
        self.entry_sum.place(x=10, y=220, width=247, height=30)

        self.entry_date_var = tk.StringVar()
        self.entry_date_var.set('Investment Date (YYYY-MM-DD)')
        self.entry_date = tk.Entry(self, textvariable=self.entry_date_var, borderwidth='1px', font=self.font,
                                   justify='center', bg='grey')
        self.entry_date.place(x=340, y=220, width=247, height=30)

        self.entry_stock_var1 = tk.StringVar()
        self.entry_stock_var1.set('Stock Abbreviation1')
        self.entry_stock1 = tk.Entry(self, textvariable=self.entry_stock_var1, borderwidth='1px', font=self.font,
                                     justify='center', bg='grey')
        self.entry_stock1.place(x=10, y=270, width=247, height=32)

        self.entry_stock_var2 = tk.StringVar()
        self.entry_stock_var2.set('Stock Abbreviation2')
        self.entry_stock2 = tk.Entry(self, textvariable=self.entry_stock_var2, borderwidth='1px', font=self.font,
                                     justify='center', bg='grey')
        self.entry_stock2.place(x=10, y=320, width=247, height=32)

        self.entry_crypto_var1 = tk.StringVar()
        self.entry_crypto_var1.set('Crypto Abbreviation1')
        self.entry_crypto1 = tk.Entry(self, textvariable=self.entry_crypto_var1, borderwidth='1px', font=self.font,
                                      justify='center', bg='grey')
        self.entry_crypto1.place(x=340, y=270, width=247, height=32)

        self.entry_crypto_var2 = tk.StringVar()
        self.entry_crypto_var2.set('Crypto Abbreviation2')
        self.entry_crypto2 = tk.Entry(self, textvariable=self.entry_crypto_var2, borderwidth='1px', font=self.font,
                                      justify='center', bg='grey')
        self.entry_crypto2.place(x=340, y=320, width=247, height=30)

        # Binds
        self.entry_sum.bind("<FocusIn>", self.on_entry_focus_in_sum)
        self.entry_sum.bind("<FocusOut>", self.on_entry_focus_out_sum)
        self.entry_crypto1.bind("<FocusIn>", self.on_entry_focus_in_crypto1)
        self.entry_crypto1.bind("<FocusOut>", self.on_entry_focus_out_crypto1)
        self.entry_crypto2.bind("<FocusIn>", self.on_entry_focus_in_crypto2)
        self.entry_crypto2.bind("<FocusOut>", self.on_entry_focus_out_crypto2)
        self.entry_date.bind("<FocusIn>", self.on_entry_focus_in_date)
        self.entry_date.bind("<FocusOut>", self.on_entry_focus_out_date)
        self.entry_stock1.bind("<FocusIn>", self.on_entry_focus_in_stock1)
        self.entry_stock1.bind("<FocusOut>", self.on_entry_focus_out_stock1)
        self.entry_stock2.bind("<FocusIn>", self.on_entry_focus_in_stock2)
        self.entry_stock2.bind("<FocusOut>", self.on_entry_focus_out_stock2)

        self.entry_stock1.bind("<Key>", self.on_entry_key_stock1)
        self.entry_crypto1.bind("<Key>", self.on_entry_key_crypto1)
        self.entry_stock1.bind("<FocusOut>", self.on_entry_focus_out_st1)
        self.entry_crypto1.bind("<FocusOut>", self.on_entry_focus_out_cr1)

        self.entry_stock2.bind("<Key>", self.on_entry_key_stock2)
        self.entry_crypto2.bind("<Key>", self.on_entry_key_crypto2)
        self.entry_stock2.bind("<FocusOut>", self.on_entry_focus_out_st2)
        self.entry_crypto2.bind("<FocusOut>", self.on_entry_focus_out_cr2)

        # LABELS
        self.label_result = tk.Label(self, font=self.font, justify='center', text='', fg='black', bg='#F1EFEF')
        self.label_result.place(x=0, y=0, width=594, height=191)

    def on_entry_focus_in_sum(self, event):
        if self.entry_sum_var.get() == 'Investment Sum ($)':
            self.entry_sum_var.set('')

    def on_entry_focus_out_sum(self, event):
        if not self.entry_sum_var.get():
            self.entry_sum_var.set('Investment Sum ($)')

    def on_entry_focus_in_crypto1(self, event):
        if self.entry_crypto_var1.get() == 'Crypto Abbreviation1':
            self.entry_crypto_var1.set('')

    def on_entry_focus_out_crypto1(self, event):
        if not self.entry_crypto_var1.get():
            self.entry_crypto_var1.set('Crypto Abbreviation1')

    def on_entry_focus_in_crypto2(self, event):
        if self.entry_crypto_var2.get() == 'Crypto Abbreviation2':
            self.entry_crypto_var2.set('')

    def on_entry_focus_out_crypto2(self, event):
        if not self.entry_crypto_var2.get():
            self.entry_crypto_var2.set('Crypto Abbreviation2')

    def on_entry_focus_in_date(self, event):
        if self.entry_date_var.get() == 'Investment Date (YYYY-MM-DD)':
            self.entry_date_var.set('')

    def on_entry_focus_out_date(self, event):
        if not self.entry_date_var.get():
            self.entry_date_var.set('Investment Date (YYYY-MM-DD)')

    def on_entry_focus_in_stock1(self, event):
        if self.entry_stock_var1.get() == 'Stock Abbreviation1':
            self.entry_stock_var1.set('')

    def on_entry_focus_out_stock1(self, event):
        if not self.entry_stock_var1.get():
            self.entry_stock_var1.set('Stock Abbreviation1')

    def on_entry_focus_in_stock2(self, event):
        if self.entry_stock_var2.get() == 'Stock Abbreviation2':
            self.entry_stock_var2.set('')

    def on_entry_focus_out_stock2(self, event):
        if not self.entry_stock_var2.get():
            self.entry_stock_var2.set('Stock Abbreviation2')

    def on_entry_key_stock1(self, event):
        self.entry_crypto2.config(state="disabled")

    def on_entry_focus_out_st1(self, event):
        if not self.entry_stock1.get():
            self.entry_stock1.delete(0, "end")
            self.entry_stock1.insert(0, self.default_stock1)
        if self.entry_stock_var1.get() == self.default_stock1:
            self.entry_crypto2.config(state="normal")

    def on_entry_key_stock2(self, event):
        self.entry_crypto1.config(state="disabled")

    def on_entry_focus_out_st2(self, event):
        if not self.entry_stock2.get():
            self.entry_stock2.delete(0, "end")
            self.entry_stock2.insert(0, self.default_stock2)
        if self.entry_stock_var2.get() == self.default_stock2:
            self.entry_crypto1.config(state="normal")

    def on_entry_key_crypto1(self, event):
        self.entry_stock2.config(state="disabled")

    def on_entry_focus_out_cr1(self, event):
        if not self.entry_crypto1.get():
            self.entry_crypto1.delete(0, "end")
            self.entry_crypto1.insert(0, self.default_crypto1)
        if self.entry_crypto_var1.get() == self.default_crypto1:
            self.entry_stock2.config(state="normal")

    def on_entry_key_crypto2(self, event):
        self.entry_stock1.config(state="disabled")

    def on_entry_focus_out_cr2(self, event):
        if not self.entry_crypto2.get():
            self.entry_crypto2.delete(0, "end")
            self.entry_crypto2.insert(0, self.default_crypto2)
        if self.entry_crypto_var2.get() == self.default_crypto2:
            self.entry_stock1.config(state="normal")

    def submited_data(self):
        try:
            amount = float(self.entry_sum_var.get().strip())
            date = self.entry_date_var.get().strip()
            stock1 = self.entry_stock_var1.get().strip().upper()
            stock2 = self.entry_stock_var2.get().strip().upper()
            crypto1 = self.entry_crypto_var1.get().strip().upper()
            crypto2 = self.entry_crypto_var2.get().strip().upper()
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
            if (crypto1 == self.default_crypto1.upper() or crypto1 == " ") and \
                    (crypto2 == self.default_crypto2.upper() or crypto2 == " "):
                res = self.method.investment_compare(amount=amount, start_date=date, stock1=stock1, stock2=stock2)
                self.label_result['fg'] = '#0E82D3'
                self.label_result['text'] = f"Investment {amount}$\n Date: {date}\n Shares: {stock1} & {stock2}:\n\n" \
                                            f"{stock1} shares count - {res[0]['akcijos']:.2f} units        " \
                                            f"{stock2} shares count  - {res[1]['akcijos']:.2f} units\n" \
                                            f"Current {stock1} value - {res[0]['dabartine']:.2f}$        " \
                                            f"Current {stock2} value - {res[1]['dabartine']:.2f}$"
            elif (stock1 == self.default_stock1.upper() or stock1 == " ") and \
                    (stock2 == self.default_stock2.upper() or stock2 == " "):
                res = self.method.investment_compare(amount=amount, start_date=date, crypto1=crypto1, crypto2=crypto2)
                self.label_result['fg'] = '#0E82D3'
                self.label_result['text'] = f"Investment {amount}$\n Date: {date}\n Coins: {crypto1} & {crypto2}:\n\n" \
                                            f"{crypto1} coins count - {res[0]['zetonai']:.2f} units        " \
                                            f"{crypto2} coins count - {res[1]['zetonai']:.2f} units\n" \
                                            f"Current {crypto1} value - {res[0]['dabartine']:.2f}$        " \
                                            f"Current {crypto2} value - {res[1]['dabartine']:.2f}$"
            elif (stock2 == self.default_stock2.upper() or stock2 == " ") and \
                    (crypto2 == self.default_crypto2.upper() or crypto2 == " "):
                res = self.method.investment_compare(amount=amount, start_date=date, stock1=stock1, crypto1=crypto1)
                self.label_result['fg'] = '#0E82D3'
                self.label_result['text'] = f"Investment {amount}$\n Date: {date}\n " \
                                            f"Share's/Coin's: {stock1} & {crypto1}:\n\n" \
                                            f"{stock1} share's count - {res[0]['akcijos']:.2f} units        " \
                                            f"{crypto1} coin's count - {res[1]['zetonai']:.2f} units\n" \
                                            f"Current {stock1} value - {res[0]['dabartine']:.2f}$        " \
                                            f"Current {crypto1} value - {res[1]['dabartine']:.2f}$"
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
