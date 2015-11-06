"""
-------------------------------------------------------
PySHARDS Cache Curve Modeling

I downloaded some trace data from the SNIA IOTTA repository.
These traces are quite large, and contain a lot of data we do
not need for constructing cache curves. 

This utility program extracts the disk read addresses from the
trace and writes them to a text file. This text file can then act
as a trace input for my SHARDS implementation
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: November 5, 2015
-------------------------------------------------------
"""

filePtrRead = open("firstORIGINALTrace.csv", "r", encoding="utf-8")
filePtrWrite = open("filteredTrace.csv", "w", encoding='utf-8')

currentLinesProcessed = 0

thisLine = filePtrRead.readline()
while thisLine != "":
    thisLineSplit = thisLine.split()
    if thisLineSplit[0] == "DiskRead,":
        filePtrWrite.write(str(thisLineSplit[5]) + '\n')
        print(thisLineSplit)
        
    currentLinesProcessed += 1
    if currentLinesProcessed % 100 == 0:
        print("Lines Processed: {0}".format(currentLinesProcessed))
    
    thisLine = filePtrRead.readline()
    
filePtrRead.close()
filePtrWrite.close()