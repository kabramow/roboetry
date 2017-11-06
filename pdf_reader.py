import PyPDF2


def ret_hello():
    return "hello"


def ret_goodbye():
    return "goodbye"


def pdf_info(pdf_name):
    # creating a pdf file object
    pdfFileObj = open(pdf_name, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # printing number of pages in pdf file
    print(pdfReader.numPages)

    # creating a page object
    pageObj = pdfReader.getPage(1)

    myString = pageObj.extractText()
    # extracting text from page
    print(myString)

    # closing the pdf file object
    pdfFileObj.close()