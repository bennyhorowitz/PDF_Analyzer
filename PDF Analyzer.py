# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 09:45:48 2022

@author: horowitz-b
"""

import os
import numpy as np
import PyPDF2
import fitz
from PyPDF2 import PdfFileMerger 
from PyPDF2 import PdfFileReader, PdfFileWriter
import re

path = 'management_directorate.pdf'
folder = r"C:\Users\horowitz-b\Documents\DHS\Python"
temp = r"C:\Users\horowitz-b\Documents\DHS\Python\temp"

os.chdir(r"C:\Users\horowitz-b\Documents\DHS\Python")

string = "Mission support programs"

###################################Download PDFs from webpage
# import requests
# from bs4 import BeautifulSoup


# os.chdir(r"C:\Users\horowitz-b\Documents\DHS\Python")
  
# # URL from which pdfs to be downloaded
# url = "https://www.dhs.gov/publication/congressional-budget-justification-fy-2022"
  
# # Requests URL and get response object
# response = requests.get(url)
  
# # Parse text obtained
# soup = BeautifulSoup(response.text, 'html.parser')
  
# # Find all hyperlinks present on webpage
# links = soup.find_all('a')
  
# i = 0
  
# # From all links check for pdf link and
# # if present download file
# for link in links:
#     if ('.pdf' in link.get('href', [])):
#         i += 1
#         print("Downloading file: ", i)
  
#         # Get response object for link
#         response = requests.get(link.get('href'))
  
#         # Write content in pdf file
#         pdf = open("pdf"+str(i)+".pdf", 'wb')
#         pdf.write(response.content)
#         pdf.close()
#         print("File ", i, " downloaded")
  
# print("All PDF files downloaded")



######################################   Merges all original PDFs in the above folder
x = [a for a in os.listdir(folder) if a.endswith(".pdf")]
merger = PdfFileMerger()
for pdf in x:
    merger.append(open(pdf, 'rb'))
with open("result.pdf", "wb") as fout:
    merger.write(fout)
    
########################################Remove blank pages


 
##################################### Get list of page numbers with the string
obj = PyPDF2.PdfFileReader("result.pdf")
NumPages = obj.getNumPages()

lst = []
for i in range(0, NumPages):
    PageObj = obj.getPage(i)
    Text = PageObj.extractText()
    if re.search(string,Text):
          lst.append(i)

       
#####################################Highlight the merged file where strings are    
doc = fitz.open("result.pdf")         
for i in lst:
    page = doc[i] 
    ### SEARCH    
    text = string
    text_instances = page.searchFor(text)    
    ### HIGHLIGHT    
    for inst in text_instances:
        highlight = page.addHighlightAnnot(inst)     
    ### OUTPUT    
doc.save("highlighted.pdf")#, garbage=4, deflate=True, clean=True) 
inputpdf = PdfFileReader(open("highlighted.pdf", "rb"))


##########################################Creat new PDFs with only pages with string highlights
inputpdf = PdfFileReader(open("highlighted.pdf", "rb"))
arr = np.array(lst)
for i in arr:
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("pdf%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)

#####################################################Compile highlighted pages into final document        
x = [a for a in os.listdir(folder) if a.startswith("pdf")]
merger = PdfFileMerger()
for pdf in x:
    merger.append(open(pdf, 'rb'))
with open("final.pdf", "wb") as fout:
    merger.write(fout)
    
######################################################Delete files
dir = temp
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))



   






        

    
    
    
    
    
    
    