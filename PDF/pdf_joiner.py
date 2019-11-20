
'''
At some point, I get annoyed with having so many separate PDF
files and being unable to put them together, so I used the PyPDF
library to build a program to put them together.
'''

# import necessary modules
try:
    from PyPDF2 import PdfFileReader, PdfFileWriter
except ImportError:
    from pyPdf import PdfFileReader, PdfFileWriter

# puts together PDFs
def pdf_cat(input_files, output_file):
    input_streams = []
    output_stream = open(output_file, 'wb')
    try:
        # First open all the files, then produce the output file, and
        # finally close the input files. This is necessary because
        # the data isn't read from the input files until the write
        # operation. Thanks to
        # https://stackoverflow.com/questions/6773631/problem-with-closing-python-pypdf-writing-getting-a-valueerror-i-o-operation/6773733#6773733
        for input_file in input_files:
            input_streams.append(open(input_file, 'rb'))
        writer = PdfFileWriter()
        for reader in map(PdfFileReader, input_streams):
            for n in range(reader.getNumPages()):
                writer.addPage(reader.getPage(n))
        writer.write(output_stream)
    finally:
        for f in input_streams:
            f.close()

# create a list of pdf filepaths
input_files = []

# prompt for filepaths
while True:
    new_file = input('Enter a file that you want to join below: \n\
otherwise, write "I am done") \n')
    # create a breaking method
    if "i am done" in new_file.lower():
        break
    elif new_file in input_files:
        print('You have already selected that article.')
    else:
        input_files.append(new_file)

new_file_name = input('What would you like to call your new file? \n')
if '.pdf' not in new_file_name.lower():
    new_file_name += '.pdf'

# put PDFs together
pdf_cat(input_files, new_file_name)
