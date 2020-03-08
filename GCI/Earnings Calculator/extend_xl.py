import pandas as pd
from datetime import datetime as dt
from EarningsCalculator import calculate_new_cash

'''
NOTE:
- these columns have been hardcoded into the script for simplicity
- they are just the start column and end column of the equity data
'''
START_COL = 16
END_COL = 192


# read in the data
filename = input('What is the name of the file that you want to read in? \n')

if '.' in filename:
    # get first half
    filename = filename.split('.')[0]

    # append xlsx extension
    filename = filename + '.xlsx'
else:
    filename = filename + '.xlsx'

# load into a df
df = pd.read_excel(filename, headers=0)


# get the tickers
headers = list(df.columns.values)
tickers_raw = headers[START_COL: END_COL]
tickers = [ticker.split(' ')[0] for ticker in tickers_raw]

# set the old information to empty (will be updated)
old_cash = 0
old_total_fund = 0
old_investment_list = [0 for i in range(END_COL - START_COL)]

old_date = dt(2000, 1, 1)

# create new columns to add
outside_investments = []
profits = []
profit_percentages = []
for index, row in df.iterrows():
    # get all variables necessary for calculation
    new_total_fund = row['Total Fund (Cash+Equity)']
    equity = row['Total Equity']
    new_investment_list = row[START_COL: END_COL]

    new_date = row['Date']
    new_cash = calculate_new_cash(new_total_fund, equity, old_cash, old_investment_list, new_investment_list, old_date, new_date, tickers)

    # calculate the fund difference and profit percentage
    profit = new_total_fund - new_cash - old_total_fund
    try:
        percent_profit = profit / old_total_fund
    except ZeroDivisionError:
        percent_profit = 0

    # append data to new lists
    outside_investments.append(new_cash)
    profits.append(profit)
    profit_percentages.append(percent_profit)

    # set the old information to the new information
    old_cash = row['Total Cash']
    old_date = new_date
    old_total_fund = new_total_fund
    old_investment_list = new_investment_list


# add columns to dataframe
df.insert(9, "Outside Investment", outside_investments, True)
df.insert(10, "Monthly Profit", profits, True)
df.insert(11, "Profit percentage", profit_percentages, True)

# export dataframe to excel
new_filename = filename = filename.split('.')[0] + ' extended.xlsx'
df.to_excel(new_filename, index=False)
