from EarningsCalculator import TimeFrame, af

# read in the data
filename = input('What is the name of the file that you want to read in (must be extended version)? \n')

if '.' in filename:
    # get first half
    filename = filename.split('.')[0]

    # append xlsx extension
    filename = filename + '.xlsx'
else:
    filename = filename + '.xlsx'

# get the start and end times
start_date = input('\nStart date (mm/dd/yyyy): \n')
end_date = input('End date (mm/dd/yyyy): \n')

timeframe = TimeFrame(filename, start_date, end_date)

print(f"\nAverage Assets: {af(timeframe.average_funds)}")
print(f"Outside Investment: {af(timeframe.outside_investment)}")
print(f"Total Profit: {af(timeframe.total_profits)}")
print(f"Percent Return: {timeframe.percent_earnings}")
