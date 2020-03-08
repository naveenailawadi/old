import pandas as pd
from datetime import datetime as dt


# create a function to calculate difference between the new and old investment list
def find_investments(old_investment_list, new_investment_list):
    buys = 0
    sells = 0
    for i in list(range(0, len(old_investment_list))):
        old = old_investment_list[i]
        new = new_investment_list[i]
        if old == 0 and new != 0:
            buys += new
        elif new == 0 and old != 0:
            sells += old

    # return buys and sells as a tuple
    return (buys, sells)


# create a function to calculate the new cash from a set of inputs
def calculate_new_cash(total_fund, equity, old_cash, old_investment_list, new_investment_list):
    buys, sells = find_investments(old_investment_list, new_investment_list)
    new_cash = total_fund - equity - old_cash + buys - sells

    return new_cash


def average(my_list):
    average = sum(my_list) / len(my_list)
    return average


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


def af(num):
    if 'float' in str(type(num)):
        num = round(num, 2)
    elif 'str' in str(type(num)):
        num = round(float(num), 2)
    accounting_formatted_number = f"${'{:,.2f}'.format(num)}"
    return accounting_formatted_number
