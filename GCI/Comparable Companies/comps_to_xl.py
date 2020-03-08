# finding implied prices is useless --> just plug it into a template THIS IS A SCRAPER

import comps as c
# import statistics as s
import pandas as pd
from datetime import datetime as dt


# input primary company and filename
filename = input('What would you like to call your excel file? \n')
primary = input('What is the ticker for the primary company? \n')

# handle for different filename errors
if '.' in filename:
    # get first half
    filename = filename.split('.')[0]

    # append xlsx extension
    filename = filename + '.xlsx'
else:
    filename = filename + '.xlsx'

# input any number of tickers to compare
tickers = []

# add primary ticker last
tickers.append(primary.upper())

while True:
    print('\n')
    new_ticker = input('What ticker do you want to add to your Comparable Companies Analysis \
(write "no more tickers" to finish list)? \n')
    if "no more tickers" in new_ticker.lower():
        break
    elif new_ticker in tickers:
        # check if ticker already in list
        print(f'Ticker already selected. Here are your comparable companies so far: {tickers}')
    else:
        # only use the uppercase string for tickers
        tickers.append(new_ticker.upper())


# create a companies list automatically edit
companies = []


# run the comps from the tickers
def get_ticker_data(ticker):
    print('\n')
    print(f"Finding {ticker} data...")
    new_company = c.Company(ticker)
    companies.append(new_company)


# get data with multiprocessing to make it faster
for ticker in tickers:
    get_ticker_data(ticker)


# reassign primary to a company
primary = companies[0]

# create a basic dataframe with raw comps data
basic_data = []
basic_headers = [
    'Name', 'Market Cap', 'EV/Sales TTM', 'EV/EBITDA TTM', 'EV/EBIT TTM', 'EV/FCF TTM', 'P/E', '', 'D/E', 'Beta']


# load the data into a dataframe by iterating through the companies list
for company in companies:
    row = [
        f"{company.name} ({company.ticker})", company.market_cap, company.ev_to_revenue, company.ev_to_ebitda, company.ev_to_ebit, company.ev_to_fcf,
        company.price_to_earnings, '', company.debt_to_equity, company.beta]
    basic_data.append(row)


basic_df = pd.DataFrame(basic_data)

basic_df.columns = basic_headers

'''
# add industry averages and medians to the basic df to get a main df
industry_averages = [' ', 'Industry Average']
for header in basic_headers[2:-3]:
    average = c.af_average(basic_df[header])

    # select formatting using header index
    header_index = basic_headers[2:].index(header)
    if header_index > 1:
        industry_averages.append(round(float(average.replace('$', '')), 1))
    else:
        industry_averages.append(average)

industry_medians = [' ', 'Industry Median']
for header in basic_headers[2:-3]:
    median = c.af_median(basic_df[header])

    # select formatting using header index
    header_index = basic_headers[2:].index(header)
    if header_index > 1:
        industry_medians.append(round(float(median.replace('$', '')), 1))
    else:
        industry_medians.append(median)

# create a main data table
industry_data = [industry_averages, industry_medians]
industry_df = pd.DataFrame(industry_data)
main_df = basic_df
main_df.append(industry_df)
'''
main_df = basic_df

# create data table with primary information
primary_data_title = f"{primary.name} Data"
primary_data = [[primary_data_title, ''],
                ['Mkt Cap', c.af(primary.market_cap)],
                ['Preferred Equity', c.af(primary.preferred_stock)],
                ['Minority Interest', c.af(primary.minority_interest)],
                ['Total Debt', c.af(primary.total_debt)],
                ['Cash & Cash Equiv.', c.af(primary.cash_and_cash_equivalents)],
                ['Shares Outstanding', primary.shares_outstanding],
                ['Revenue', c.af(primary.revenue)],
                ['EBITDA', c.af(primary.ebitda)],
                ['EBIT', c.af(primary.ebit)],
                ['FCF', c.af(primary.fcf)],
                ['EPS', c.af(primary.eps)],
                ['', ''],
                ['Enterprise Value', c.af(primary.enterprise_value)]]
primary_df = pd.DataFrame(primary_data)


# process high, average, median, and low for price for all EV ratios in terms of ratio and price
'''
# load all into individual lists
ev_to_revenue_list = basic_df['EV/Revenue TTM'].to_list()
ev_to_ebit_list = basic_df['EV/EBIT TTM'].to_list()
ev_to_ebitda_list = basic_df['EV/EBITDA TTM'].to_list()
ev_to_fcf_list = basic_df['EV/FCF TTM'].to_list()


# spread df
spread_data = [['High', max(ev_to_revenue_list), max(ev_to_ebit_list), max(ev_to_ebitda_list), max(ev_to_fcf_list)],
               ['Average', c.average(ev_to_revenue_list), c.average(ev_to_ebit_list), c.average(ev_to_ebitda_list), c.average(ev_to_fcf_list)],
               ['Median', s.median(ev_to_revenue_list), s.median(ev_to_ebit_list), s.median(ev_to_ebitda_list), s.median(ev_to_fcf_list)],
               ['Low', min(ev_to_revenue_list), min(ev_to_ebit_list), min(ev_to_ebitda_list), min(ev_to_fcf_list)]]

spread_df = pd.DataFrame(spread_data)

# create sector price projection
sector_price_projections_data = []

for row in spread_data:
    # map the items to rows
    header = row[0]
    ev_to_revenue = row[1]
    ev_to_ebit = row[2]
    ev_to_ebitda = row[3]
    ev_to_fcf = row[4]

    # create projections
    ev_to_revenue_projection = c.project_price(ev_to_revenue, primary.ev_to_revenue, primary.shares_outstanding)

    ev_to_ebit_projection = c.project_price(ev_to_ebit, primary.ev_to_ebit, primary.shares_outstanding)

    ev_to_ebitda_projection = c.project_price(ev_to_ebitda, primary.ev_to_ebitda, primary.shares_outstanding)

    ev_to_fcf_projection = c.project_price(ev_to_revenue, primary.ev_to_fcf, primary.shares_outstanding)

    # append projections to new row
    new_row = [header, ev_to_revenue_projection, ev_to_ebit_projection, ev_to_ebitda_projection, ev_to_fcf_projection]

    sector_price_projections_data.append(new_row)

# load into sector price projections df
sector_price_df = pd.DataFrame(sector_price_projections_data)


# create primary price projections
primary_price_projections_data = [[' ', 'High', 'Average', 'Median', 'Low'],
                                  ['Current Price', primary.price_per_share, primary.price_per_share, primary.price_per_share, primary.price_per_share]]

# output implied prices and add them to the primary price projections data
comps_output = ['Comps Output']

for row in sector_price_projections_data:
    # get rid of the row label
    projections = row[1:]

    # get average of projections (using function to deal with formatting)
    average = c.af_average(projections)

    # append the average to the comps output
    comps_output.append(average)

primary_price_projections_data.append(comps_output)

# load primary price projections data into a dataframe
primary_price_projections_df = pd.DataFrame(primary_price_projections_data)
'''

# structure and export to an excel file

# create engine, worksheet, and add a title

with pd.ExcelWriter(filename) as writer:
    workbook = writer.book
    sheet_title = f"{primary.name} Comps"
    worksheet = workbook.add_worksheet(sheet_title)
    writer.sheets[sheet_title] = worksheet

    # write excel sheet
    num_companies = len(companies)
    title_data = [[primary.name], ['Comparable Companies Analysis'], ['<Sector>'], [str(dt.today()).split(' ')[0]], ['<Quantity Measured in (please check)>']]
    title_df = pd.DataFrame(title_data)
    title_df.to_excel(writer, sheet_name=sheet_title, startrow=0, startcol=1, index=False, header=False)
    main_df.to_excel(writer, sheet_name=sheet_title, startrow=num_companies + 2, startcol=2, index=False)
    primary_df.to_excel(writer, sheet_name=sheet_title, startrow=num_companies + 10, startcol=1, index=False, header=False)
    # spread_df.to_excel(writer, sheet_name=sheet_title, startrow=num_companies + 9, startcol=5, index=False, header=False)
    # sector_price_df.to_excel(writer, sheet_name=sheet_title, startrow=num_companies + 14, startcol=5, index=False, header=False)
    # primary_price_projections_df.to_excel(writer, sheet_name=sheet_title, startrow=num_companies + 19, startcol=4, index=False, header=False)
    writer.save()
