'''
This will sort data by desired headers.
It was used to sort a 4000+ row csv into individual
potential client information.
'''

import pandas as pd
import csv

# input the filepath
name = input('What is the file called? \n')

# get information for naming the new files
new_name = input('What do you want your sorted text file to be called? \n')

# get old file into dataframe and a list
data = pd.read_csv(name, header=0)
df = pd.DataFrame(data)
print('DataFrame created')
header_list = df.columns.values.tolist()

# find the desired header to sort by (a while statement is used to keep the code from breaking)
while True:
    sorting_choice_str = input('Which header do you want to sort by?\n')
    if sorting_choice_str.lower() in header_list:
        sorting_index = header_list.index(sorting_choice_str)
        print('Header found')
        break
    else:
        print('Column label not found. Please enter again.')

# Create an empty list
Row_list = []

# Iterate over each row
for i in range((df.shape[0])):

    # Using iloc to access the values of
    # the current row denoted by "i"
    Row_list.append(list(df.iloc[i, :]))

print('New list created')

# find all the variations in the desired column
duty_list = []
for n in Row_list:
    try:
        if n[sorting_index] not in duty_list:
            duty_list.append(n[sorting_index])
            print('New Duty found: ' + str(n[sorting_index]))
    except IndexError:
        continue

# create a new file for every variation
for action in duty_list:
    stuff = str(action)
    # sometimes the name becomes a filepath, which confuses the computer
    try:
        new_indexed_file = open(str(new_name) + stuff + '.csv', mode='w')
    except FileNotFoundError:
        continue
    writer = csv.writer(new_indexed_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in Row_list:
        if len(i) > 1:
            if action in i[sorting_index]:
                writer.writerow(i)
    new_indexed_file.close()
    print(str(action) + ' file has been written.')

print('Done!')
