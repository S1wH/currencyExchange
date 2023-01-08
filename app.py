import tkinter as tk
import requests
from bs4 import BeautifulSoup


class App:
    def __init__(self):
        x_pixels = 800
        y_pixels = 600
        self.currency_list = ['ruble', 'dollar', 'euro', 'yen', 'yuan']
        self.currency_code = ['RUB', 'USD', 'EUR', 'JPY', 'CNY']

        window = tk.Tk()
        window.geometry(f'{x_pixels}x{y_pixels}')
        window.title('Currency Exchange')

        main_label = tk.Label(text='Currency Exchange App', font=('Arial', 20))
        main_label.pack(anchor='n', pady=10)

        choose_label = tk.Label(text='Choose your currency:', font=('Arial', 15))
        choose_label.pack(anchor='n', pady=10)

        variable = tk.StringVar(window)
        variable.set(self.currency_list[0])
        opt = tk.OptionMenu(window, variable, *self.currency_list)
        opt.pack(anchor='n', pady=10)
        opt.config(width=18, font=('Arial', 12))

        choose_label2 = tk.Label(text='Choose the currency you want to exchange money into:', font=('Arial', 15))
        choose_label2.pack(anchor='n', pady=20)

        variable2 = tk.StringVar(window)
        variable2.set(self.currency_list[1])
        opt2 = tk.OptionMenu(window, variable2, *self.currency_list)
        opt2.pack(anchor='n')
        opt2.config(width=18, font=('Arial', 12))

        input_label = tk.Label(text='Input the amount of money you want to exchange:', font=('Arial', 15))
        input_label.pack(anchor='n', pady=10)

        entry = tk.Entry()
        entry.pack(anchor='n')

        button_exchange = tk.Button(text='Exchange!', command=self.exchangeCurrency)
        button_exchange.config(width=18, font=('Arial', 14))
        button_exchange.pack(anchor='n', pady=20)

        output_label = tk.Label(text="", font=('Arial', 15))
        output_label.pack(anchor='n', pady=10)

        self.currency1 = variable
        self.currency2 = variable2
        self.output = output_label
        self.input_entry = entry
        self.url = 'https://cbr.ru/currency_base/daily/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/100.0.4896.160 YaBrowser/22.5.2.615 Yowser/2.5 Safari/537.36',
            'upgrade-insecure-requests': '1'}
        self.info = self.getHtml()
        window.mainloop()

    def exchangeCurrency(self):
        if self.currency1.get() != self.currency2.get():
            try:
                money = int(self.input_entry.get())
                prices = self.findPrice()
                if prices[0] is None:
                    self.output['text'] = round(money / prices[1], 2)
                elif prices[1] is None:
                    self.output['text'] = round(money * prices[0], 2)
                else:
                    self.output['text'] = round(money * prices[0] / prices[1], 2)
            except ValueError:
                self.output['text'] = 'Something went wrong'

    def findPrice(self):
        price1 = None
        price2 = None
        if self.currency1.get() == 'ruble':
            price2 = self.getContent(self.currency2.get())
        elif self.currency2.get() == 'ruble':
            price1 = self.getContent(self.currency1.get())
        else:
            price1 = self.getContent(self.currency1.get())
            price2 = self.getContent(self.currency2.get())
        return [price1, price2]

    def getHtml(self, params=None):
        r = requests.get(self.url, headers=self.headers, params=params)
        return r

    def getContent(self, cur):
        amount = 0
        price = 0
        soup = BeautifulSoup(self.info.text, 'lxml')
        items = soup.find_all('tr')
        for item in items:
            if self.currency_code[self.currency_list.index(cur)] in item.text:
                for index, value in enumerate(item):
                    if index == 5:
                        amount = int(value.get_text())
                    if index == 9:
                        price = float(value.get_text().replace(',', '.'))
        return price / amount
