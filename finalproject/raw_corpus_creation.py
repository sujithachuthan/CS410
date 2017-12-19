#Raw Corpus Creation - Created on Tue Nov 28 10:58:45 2017

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import PDFPageAggregator
from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.layout import LAParams
from io import StringIO
import os
import sys

if(len(sys.argv) != 2):
    print ('Usage: Pass Arguments - Path Of PDF Input Directory')
    sys.exit(1)

print ("Input PDFS File Name & Path is " + sys.argv[1])

#Extracts Text Content from the PDF Files
def getPDFContent(path):
    
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    retstr = StringIO()

    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
       
    # Process each page contained in the document.
    for page in doc.get_pages():
        interpreter.process_page(page)

    pdfstring = retstr.getvalue()
    retstr.close()
    
    fp.close()
    device.close()
    
    return pdfstring

#This part of the program loops through all PDF Files in the directory
# and extracts texts from PDFS that have Suggested Reading / Additional Reading
# slides present as content
for dirname, dirnames, filenames in os.walk(sys.argv[1]):
    # print path to all subdirectories first.
    # for subdirname in dirnames:
        # print(os.path.join(dirname, subdirname))
        
    # print path to all filenames.
    for filename in filenames:
        print(os.path.join(dirname, filename))

        filename, file_extension = os.path.splitext(os.path.join(dirname, filename))

        if(file_extension == ".pdf") :
            print("Going to extract PDF Contents")
            finalfileName = filename + file_extension
            pdfString = getPDFContent(finalfileName)
            if(pdfString.find('Suggested Reading') != -1 or pdfString.find('Additional Reading') != -1 ) :
                print("Going to create corpus")
                corpusTmpFileName = filename + "tmp.txt"
                myFileNew = open(corpusTmpFileName, 'w', encoding='ascii', errors='ignore')
                myFileNew.write(pdfString.rstrip())
                myFileNew.close()
        
                myLine = ""    
                myFileRead = open(corpusTmpFileName,"r")
                line = myFileRead.readline()
                myLine += line.strip() + " "
                cnt = 1
                
                while line:
                   #print("Line {}: {}".format(cnt, line.strip()))
                   myLine += line.strip() + " "
                   line = myFileRead.readline()           
                   
                
                corpusFinFileName = filename + ".txt"
                myFinFile = open(corpusFinFileName,"w")
                myFileRead.close()
                os.remove(corpusTmpFileName)
                    
                myFinFile.write(myLine + "\n")

myFinFile.close()


