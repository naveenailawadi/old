import pandas as pd
import csv

name = input('What is the file called? \n')
new_name = input('What do you want your sorted text file to be called? \n')
data = pd.read_csv(name, header=0)
df = pd.DataFrame(data)
# Create an empty list
Row_list = []

# Iterate over each row
for i in range((df.shape[0])):

    # Using iloc to access the values of
    # the current row denoted by "i"
    Row_list.append(list(df.iloc[i, :]))

revised_row_list = []
for student_data in Row_list:
    revised_student_data = []
    revised_student_data_two = []
    student = student_data[0]
    grad_year = student_data[1]
    parents = student_data[2]
    parent_emails = student_data[3]
    grade_level = student_data[4]
    if ',' in parents:
        revised_student_data = [student,
                                grad_year,
                                parents[:parents.find(',')],
                                parent_emails[: parent_emails.find(',')],
                                grade_level]
        # round 2
        revised_student_data_two = [student,
                                    grad_year,
                                    parents[parents.find(', ') + 2:],
                                    parent_emails[parent_emails.find(', ') + 2:],
                                    grade_level]
    else:
        revised_student_data = [student,
                                grad_year,
                                parents,
                                parent_emails,
                                grade_level]
        # append big list
    revised_row_list.append(revised_student_data)
    revised_row_list.append(revised_student_data_two)

grade_list = []
for n in revised_row_list:
    try:
        if n[4] not in grade_list:
            grade_list.append(n[4])
    except IndexError:
        continue

for grade in grade_list:
    new_indexed_file = open(str(new_name) + str(grade) + '.csv', mode='w')
    writer = csv.writer(new_indexed_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in revised_row_list:
        if len(i) > 1:
            if grade in i[4]:
                writer.writerow(i)
    new_indexed_file.close()
    print(str(grade) + ' grade file has been written.')

print('Done!')

