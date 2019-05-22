import pandas
from collections import Counter
from docx import Document

# instructions:
print('This program is extremely easy to use. \n \
To begin, label the column of the college in the csv "college". \n \
Then, simply save the program and answer the following prompts. \n')
name = input('What is the file called? \n')
new_file = input('What do you want your sorted text file to be called? \n')

data = pandas.read_csv(name, header = 0)
col = data.college
c = Counter(col)
c_alpha = sorted(c.keys())
doc = Document()
doc.save(new_file + '.docx')
for place in c_alpha:
    number_of_students = c[place]
    if number_of_students > 1:
        line = str(place + ' - ' + str(number_of_students))
    else:
        line = str(place)
    doc.add_paragraph(line)
doc.save(new_file +'.docx')
print('Finished! Your new file is called ' + new_file + '.docx.')
