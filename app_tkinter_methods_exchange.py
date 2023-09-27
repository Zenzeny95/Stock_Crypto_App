"""
The 'ExchangePopupWindow' class represents a Tkinter popup window for exchanging currencies.

Class Methods:
- '__init__(self, master, title)': Initializes a new 'ExchangePopupWindow' instance.
    - 'master': The master Tkinter window to which this popup is associated.
    - 'title': The title of the popup window.

Methods:
- 'submited_data(self)': Validates and processes user-submitted data for currency exchange.

Note:
- This class represents a Tkinter popup window for exchanging currencies.
- Users can enter the amount, source currency, and target currency to perform the exchange.
- The exchange rate and result are displayed in a label within the popup window.
- Data validation is performed to ensure the entered values are valid for currency exchange.
"""

import tkinter as tk
from tkmacosx import Button as MacButton
from app_mixed_methods import Methods


class ExchangePopupWindow(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        width = 600
        height = 350
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        self.font = tk.font.Font(family="Helvetica", size=16)
        self.default_entry = 'Crypto/Currency'
        self.method = Methods()

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/800x350background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # BUTTONS
        submit_button = MacButton(self, font=self.font, justify='center', text='Submit', command=self.submited_data)
        close_button = MacButton(self, font=self.font, justify='center', text='Close Window', command=self.destroy)
        submit_button.place(x=30, y=230, width=200, height=40)
        close_button.place(x=30, y=290, width=200, height=40)

        # LABEL
        self.label = tk.Label(self, font=self.font, justify='center', text='', bg='#F1EFEF')
        self.label.place(x=260, y=0, width=322, height=335)

        # CHECKBOX
        self.checkbox_state = tk.IntVar()
        self.checkbox = tk.Checkbutton(self, font=self.font, justify='center', text='Currency to Crypto',
                                       fg='black', bg='#F1EFEF', offvalue=0, onvalue=1, variable=self.checkbox_state)
        self.checkbox.place(x=60, y=70, width=200, height=30)

        # ENTRIES
        self.entry_amount_var = tk.StringVar()
        self.entry_amount_var.set('Amount')
        self.entry_amount = tk.Entry(self, textvariable=self.entry_amount_var, borderwidth='1px', font=self.font,
                                     justify='center', bg='grey')
        self.entry_amount.place(x=30, y=30, width=200, height=30)

        self.entry1_var = tk.StringVar()
        self.entry1_var.set('Crypto/Currency')
        self.entry1 = tk.Entry(self, textvariable=self.entry1_var, borderwidth='1px', font=self.font,
                               justify='center', bg='grey')
        self.entry1.place(x=30, y=110, width=200, height=30)

        self.entry2_var = tk.StringVar()
        self.entry2_var.set('Crypto/Currency')
        self.entry2 = tk.Entry(self, textvariable=self.entry2_var, borderwidth='1px', font=self.font,
                               justify='center', bg='grey')
        self.entry2.place(x=30, y=160, width=200, height=30)

        # BINDS
        self.entry_amount.bind("<FocusIn>", self.on_entry_focus_in_amount)
        self.entry_amount.bind("<FocusOut>", self.on_entry_focus_out_amount)
        self.entry1.bind("<FocusIn>", self.on_entry_focus_in_entry1)
        self.entry1.bind("<FocusOut>", self.on_entry_focus_out_entry1)
        self.entry2.bind("<FocusIn>", self.on_entry_focus_in_entry2)
        self.entry2.bind("<FocusOut>", self.on_entry_focus_out_entry2)

    def on_entry_focus_in_amount(self, event):
        if self.entry_amount_var.get() == 'Amount':
            self.entry_amount_var.set('')

    def on_entry_focus_out_amount(self, event):
        if not self.entry_amount_var.get():
            self.entry_amount_var.set('Amount')

    def on_entry_focus_in_entry1(self, event):
        if self.entry1_var.get() == 'Crypto/Currency':
            self.entry1_var.set('')

    def on_entry_focus_out_entry1(self, event):
        if not self.entry1_var.get():
            self.entry1_var.set('Crypto/Currency')

    def on_entry_focus_in_entry2(self, event):
        if self.entry2_var.get() == 'Crypto/Currency':
            self.entry2_var.set('')

    def on_entry_focus_out_entry2(self, event):
        if not self.entry2_var.get():
            self.entry2_var.set('Crypto/Currency')

    def submited_data(self):
        try:
            result = []
            amount = float(self.entry_amount_var.get().strip())
            first = self.entry1_var.get().strip().upper()
            second = self.entry2_var.get().strip().upper()
            if amount <= 0:
                raise ValueError
            elif (len(first) != 3 or len(second) != 3) and not (first.isalpha() or second.isalpha()):
                raise ValueError
            else:
                if self.checkbox_state.get() == 0:
                    info = self.method.exchange_rate(first, second)
                    for value in info.values():
                        for key, val in value.items():
                            bendras = key + ": " + val
                            result.append(bendras)
                    rate = float(info['Realtime Currency Exchange Rate']['5. Exchange Rate'])
                    self.label['fg'] = '#0E82D3'
                    self.label['text'] = f'{result[0]}\n{result[1]}\n{result[2]}\n{result[3]}\n{result[4]}\n' \
                                         f'{result[5]}\n{result[6]}\n{result[7]}\n{result[8]}\n\n' \
                                         f'{amount} {first} = {(amount * rate):.2f} {second}'
                elif self.checkbox_state.get() == 1:
                    info = self.method.exchange_rate(second, first)
                    for value in info.values():
                        for key, val in value.items():
                            bendras = key + ": " + val
                            result.append(bendras)
                    rate = float(info['Realtime Currency Exchange Rate']['5. Exchange Rate'])
                    bid_price = 1 / float(info['Realtime Currency Exchange Rate']['8. Bid Price'])
                    ask_price = 1 / float(info['Realtime Currency Exchange Rate']['9. Ask Price'])
                    new_rate = 1 / rate
                    self.label['fg'] = '#0E82D3'
                    self.label['text'] = f'{result[0].replace("From", "To")}\n{result[1].replace("From", "To")}\n' \
                                         f'{result[2].replace("To", "From")}\n{result[3].replace("To", "From")}\n' \
                                         f'5. Exchange Rate: {new_rate}\n{result[5]}\n{result[6]}\n' \
                                         f'8. Bid Price: {bid_price}\n9. Ask Price: {ask_price}\n\n' \
                                         f'{amount} {first} = {(amount * new_rate)} {second}'
        except ValueError:
            self.label['fg'] = 'red'
            self.label['text'] = 'Invalid Entry'
        except AttributeError:
            self.label['fg'] = 'red'
            self.label['text'] = 'Mark The Checkbox\n To Convert Currency to Crypto\n\nIf Checkbox Is Marked:\n' \
                                 'Invalid Entry'
