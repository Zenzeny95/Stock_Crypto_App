"""
   A class representing a tkinter popup window for making stock price predictions using a pre-trained machine
   learning model.

   Methods:
       __init__(self, master, title):
           Initializes the PredictionsPopupWindow with the specified master window and title.

       on_entry_focus_in_equity(self, event):
           Handles the focus-in event for the equity entry field.

       on_entry_focus_out_equity(self, event):
           Handles the focus-out event for the equity entry field.

       create_sequences(data, sequence_length):
           Creates sequences from the given data for input to the machine learning model.

       prepared_data(self, company):
           Prepares the stock data for making predictions.

       display_future_prices(self, latest_data, predictions):
           Displays the future stock price predictions on a chart.

       display_chart(self, df):
           Displays a chart of predicted stock prices.

       refresh_results(self):
           Refreshes the predictions based on user input and displays the results or error messages.

   Note:
       This class is designed to create a GUI popup window that allows users to input a stock symbol (equity)
       and see predictions for the stock's prices over the next 30 days using a pre-trained machine learning model.
   """

import tkinter as tk
from tkmacosx import Button as MacButton
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tensorflow.keras.models import load_model
from app_api_stocks_requests import ApiDataStocks, pd


class PredictionsPopupWindow(tk.Toplevel):
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
        self.api_data_stocks = ApiDataStocks()

        # BACKGROUND
        self.background_image = tk.PhotoImage(file="background/1600x880background.png")
        background_label = tk.Label(self, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # CHART FRAME
        self.chart_frame = tk.Frame(self)
        self.chart_frame.place(x=530, y=90, width=1050, height=770)

        # LABEL
        label = tk.Label(self, font=self.font, justify='center', fg='black', bg='#F1EFEF')
        label['text'] = f'ML Price Prediction\n\n' \
                        f'1. Equity (IBM, TSLA etc..)\n\n' \
                        f'2. Prediction is made for the next 30 days.\n'
        self.label_message = tk.Label(self, text='Enter Information and Submit to See Results',
                                      anchor="n", justify="center", font=self.font_label, bg='SystemButtonFace',
                                      highlightthickness=0, fg="#0E82D3")
        self.label_message.place(x=550, y=30, width=550, height=40)
        label.place(x=10, y=30, width=500, height=320)

        # ENTRIES
        self.entry_equity_var = tk.StringVar()
        self.entry_equity_var.set("Equity")
        entry_equity = tk.Entry(self, textvariable=self.entry_equity_var, font=self.font, borderwidth="1px",
                                fg="#ffffff", justify="center", bg="grey")
        entry_equity.place(x=150, y=420, width=266, height=40)

        # ENTRY BINDS
        entry_equity.bind("<FocusIn>", self.on_entry_focus_in_equity)
        entry_equity.bind("<FocusOut>", self.on_entry_focus_out_equity)

        # BUTTON
        close_button = MacButton(self, text="Close Window", font=self.font, justify="center", command=self.destroy)
        submit_button = MacButton(self, text="Submit", font=self.font, justify="center", command=self.refresh_results)
        close_button.place(x=150, y=765, width=266, height=55)
        submit_button.place(x=150, y=695, width=266, height=55)

    def on_entry_focus_in_equity(self, event):
        if self.entry_equity_var.get() == "Equity":
            self.entry_equity_var.set("")

    def on_entry_focus_out_equity(self, event):
        if not self.entry_equity_var.get():
            self.entry_equity_var.set("Equity")

    @staticmethod
    def create_sequences(data, sequence_length):
        sequences = []
        for i in range(len(data) - sequence_length + 1):
            sequence = data[i:i + sequence_length]
            sequences.append(sequence)
        return np.array(sequences)

    def prepared_data(self, company):
        df_stock = self.api_data_stocks.day_data_company(company)
        df_stock['timestamp'] = pd.to_datetime(df_stock['timestamp'])
        df_stock.set_index('timestamp', drop=True, inplace=True)
        df_stock.drop('volume', axis=1, inplace=True)
        latest_data = df_stock.iloc[-1:]
        sequence_length = 150
        sequence = self.create_sequences(df_stock.to_numpy(), sequence_length)[-1]

        return latest_data, sequence

    def display_future_prices(self, latest_data, predictions):
        current_date = latest_data.index[0]
        date_range = [current_date + datetime.timedelta(days=i) for i in range(1, 31)]
        df_future_prices = pd.DataFrame(predictions, index=date_range, columns=["Predicted Close"])
        self.display_chart(df_future_prices)

    def display_chart(self, df):
        fig, ax = plt.subplots(figsize=(10, 5))

        current_date = datetime.datetime.now()
        date_range = [current_date + datetime.timedelta(days=i) for i in range(len(df))]

        ax.plot(date_range, df['Predicted Close'], color='orange', label='Predicted Close')

        ax.grid(True)
        ax.legend()
        ax.set_title('Predicted Prices Chart')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')

        ymin, ymax = ax.get_ylim()
        ax.set_ylim(ymin - 0, ymax + 0)
        max_visible_ticks = 8
        ax.xaxis.set_major_locator(plt.MaxNLocator(max_visible_ticks))

        chart_frame = self.chart_frame
        for widget in chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def refresh_results(self):
        try:
            self.label_message['fg'] = "#0E82D3"
            self.label_message['text'] = 'Enter Information and Submit to See Results'
            equity = self.entry_equity_var.get().strip().upper()
            latest_data, sequence = self.prepared_data(equity)
            loaded_model = load_model('LSTM_model.h5')
            predictions = []
            for _ in range(30):
                next_prediction = loaded_model.predict(np.expand_dims(sequence, axis=0))
                predictions.append(next_prediction[0][0])
                sequence = np.roll(sequence, shift=-1)
                sequence[-1] = next_prediction[0][0]

            self.display_future_prices(latest_data, predictions)
        except ValueError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'Invalid Entry'
        except KeyError:
            self.label_message['fg'] = "red"
            self.label_message['text'] = 'No Data Found\n Check Entries'
