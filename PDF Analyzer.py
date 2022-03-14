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

string = "providing policy"



######################################   Merges all original PDFs in the above folder
x = [a for a in os.listdir(folder) if a.endswith(".pdf")]
merger = PdfFileMerger()
for pdf in x:
    merger.append(open(pdf, 'rb'))
with open(r"C:\Users\horowitz-b\Documents\DHS\Python\temp\result.pdf", "wb") as fout:
    merger.write(fout)
 
##################################### Get list of page numbers with the string
obj = PyPDF2.PdfFileReader(r"C:\Users\horowitz-b\Documents\DHS\Python\temp\result.pdf")
NumPages = obj.getNumPages()

lst = []
for i in range(0, NumPages):
    PageObj = obj.getPage(i)
    Text = PageObj.extractText()
    if re.search(string,Text):
          lst.append(i)

#####################################Highlight the merged file where strings are    
doc = fitz.open(r"C:\Users\horowitz-b\Documents\DHS\Python\temp\result.pdf")         
for i in lst:
    page = doc[i] 
    ### SEARCH    
    text = string
    text_instances = page.searchFor(text)    
    ### HIGHLIGHT    
    for inst in text_instances:
        highlight = page.addHighlightAnnot(inst)     
    ### OUTPUT    
    doc.save("highlighted.pdf", garbage=4, deflate=True, clean=True) 
inputpdf = PdfFileReader(open("highlighted.pdf", "rb"))

##########################################Creat new PDFs with only pages with string highlights
arr = np.array(lst)
for i in arr:
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("document-page%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)

#####################################################Compile highlighted pages into final document        
x = [a for a in os.listdir(folder) if a.startswith("document-page")]
merger = PdfFileMerger()
for pdf in x:
    merger.append(open(pdf, 'rb'))
with open("final.pdf", "wb") as fout:
    merger.write(fout)
    
######################################################Delete files
dir = temp
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))



   






        

    
    
    
    
    
    
    