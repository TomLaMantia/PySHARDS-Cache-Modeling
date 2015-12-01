import sys
sys.path.append("..")
import os
import linecache
from multiprocessing import Process, Lock, Queue

PATH_TO_TRACE_DIR = os.path.normpath(os.path.join(os.getcwd(), ".."))
NUMBER_OF_THREADS = 2

def GetNumberReferencesInFile(fp):
    
    result = 1
    thisLine = fp.readline()
    while thisLine != "":
        result += 1;
        thisLine = fp.readline()
    
    result -= 1
    
    return result

def ChopTrace(numberOfReferences, numberOfThreads):
    return numberOfReferences//numberOfThreads

def Worker(myWorkerId, fileOffset, lengthToProcess):
    fp = open(os.path.join(PATH_TO_TRACE_DIR, "Traces","filteredTrace2.txt"), "r", encoding = "utf-8")
    
    #Position the file pointer accordingly
    currentOffset = 0
    thisLine = fp.readline()
    while thisLine != "" and currentOffset < fileOffset:
        currentOffset += 1
        thisLine  = fp.readline()
    
    #Process the desired partition of the trace
    currentOffset = 0
    thisLine = fp.readline()
    while thisLine != "" and currentOffset < lengthToProcess:
        print("{0}    {1}".format(thisLine, myWorkerId))
        thisLine  = fp.readline()
    
    return

def Consumer():
    
    return

def go():
    
    fp = open(os.path.join(PATH_TO_TRACE_DIR, "Traces","filteredTrace2.txt"), "r", encoding = "utf-8")
#     print(linecache.getline(os.path.join(PATH_TO_TRACE_DIR, "Traces","filteredTrace2.txt"),5))
#     result = GetNumberReferencesInFile(fp)
#     print(result)
    
    workers = []
    print(ChopTrace(GetNumberReferencesInFile(fp), 2))
#     for i in range(0,NUMBER_OF_THREADS):
#         pid = Process(target = Worker, args = [i])
#         pid.start()
#         workers.append(pid)
#         
#     for thisWorker in workers:
#         thisWorker.join()
#     for thisWorker in workers:
#         thisWorker.terminate()
    
    return

if __name__ == '__main__':
    go()
