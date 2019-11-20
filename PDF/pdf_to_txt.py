import PyPDF2
from tika import parser

# obtain filepath
filepath = input('What is the PDF called? \n')

# get text from filepath
text = ''
pdfFileObject = open(filepath, 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
count = pdfReader.numPages
if count == 0:
    count += 1
for i in range(count):
    page = pdfReader.getPage(i)
    text += page.extractText()

# name the file
name = filepath[:-4]

print('PyPDF2 output snippet: ')
print(text[:100])

# write document with tika
sufficient = input('Try with tika? (yes or no) \n')
if 'yes' in sufficient.lower():
    raw = parser.from_file(filepath)
    text = raw['content']

# write document with pypdf
print('writing document... \n')
doc = open(name + ".txt", "w")
doc.write(text)
doc.close()
