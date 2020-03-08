import pandas as pd
import yfinance as yf
from datetime import datetime as dt
from datetime import timedelta


class TimeFrame:
    def __init__(self, excel_file, start, finish):
        df = pd.read_excel(excel_file, headers=0)
        headers = list(df.columns.values)

        self.start = self.handle_date(start)
        self.finish = self.handle_date(finish)

        # get data from the relevant timeframe
        final_rows = []
        for index, row in df.iterrows():
            row_unix = row['Date'].timestamp()

            # check how it aligns with the timeframe
            if row_unix >= self.start and row_unix <= self.finish:
                final_rows.append(list(row))

        self.data = pd.DataFrame(final_rows, columns=headers)

        self.total_profits = sum(self.data['Monthly Profit'])

        self.average_funds = average(self.data['Total Fund (Cash+Equity)'])
        self.outside_investment = sum(self.data['Outside Investment'])
        self.earnings_proportion = self.total_profits / self.average_funds
        self.percent_earnings = f"{round(self.earnings_proportion * 100, 2)}%"

    # take the date and make it into a general unix time
    def handle_date(self, date_raw):
        date = date_raw.split('/')
        month = int(date[0])
        day = int(date[1])
        if len(str(date[2])) == 2:
            year = int(f"20{date[2]}")
        elif len(str(date[2])) == 4:
            year = int(date[2])

        unix_time = dt(year, month, day).timestamp()

        return unix_time


def average(my_list):
    average = sum(my_list) / len(my_list)
    return average


def get_price(ticker, date):
    data = yf.download(ticker, start=(date - timedelta(days=3)), end=date)

    # get closing price
    price = float(data.iloc[[-1]]['Close'])

    return price


# create a function to calculate difference between the new and old investment list
def find_investments(old_investment_list, new_investment_list, old_date, new_date, tickers):
    buys = 0
    sells = 0

    # iterate through all investments
    for i in list(range(0, len(old_investment_list))):
        old = old_investment_list[i]
        new = new_investment_list[i]

        # find if the share amounts of changed significantly
        if old != 0 and new != 0:
            # get the share prices and amounts
            ticker = tickers[i]

            # get the old shares
            try:
                old_price_per_share = get_price(ticker, old_date)
            except IndexError:
                continue
            old_shares = old / old_price_per_share

            # get the new shares
            try:
                new_price_per_share = get_price(ticker, new_date)
            except IndexError:
                continue
            new_shares = new / new_price_per_share

            if old_shares <= 1.1 * new_shares:
                buys += (new_shares - old_shares) * average([new_price_per_share, old_price_per_share])
            elif old_shares >= 1.1 * new_shares:
                sells += (old_shares - new_shares) * average([new_price_per_share, old_price_per_share])
        else:
            if old == 0 and new != 0:
                buys += new
            elif new == 0 and old != 0:
                sells += old

    # return buys and sells as a tuple
    return (buys, sells)


# create a function to calculate the new cash from a set of inputs
def calculate_new_cash(total_fund, equity, old_cash, old_investment_list, new_investment_list, old_date, new_date, tickers):
    buys, sells = find_investments(old_investment_list, new_investment_list, old_date, new_date, tickers)
    new_cash = total_fund - equity - old_cash + buys - sells

    return new_cash


def af(num):
    if 'float' in str(type(num)):
        num = round(num, 2)
    elif 'str' in str(type(num)):
        num = round(float(num), 2)
    accounting_formatted_number = f"${'{:,.2f}'.format(num)}"
    return accounting_formatted_number
