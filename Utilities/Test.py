import sys
sys.path.append("..")
import os
import linecache
from multiprocessing import Process, Manager
from LRUDistanceTree import LRUTree
from SampleSet import SampleSet
from Histogram import Histogram

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

def Worker(myWorkerId, fileOffset, lengthToProcess, globalProcessReferenceDict):

    """
    Since this is fixed size SHARDS, start by sampling every reference. The sampling rate
    will be lowered accordingly as the SampleSet reaches maximum capacity.
    """
    SAMPLE_RATE = 1

    mySampleSet = SampleSet(S_MAX)
    SHARDSHistogram = Histogram()
    myDistanceTree = LRUTree()

    #Open the trace file
    fp = open(os.path.join(PATH_TO_TRACE_DIR, "Traces","filteredTrace2.txt"), "r", encoding = "utf-8")

    #Position the file pointer accordingly
    currentOffset = 0
    thisReference = fp.readline()
    while thisReference != "" and currentOffset < fileOffset:
        currentOffset += 1
        thisReference  = fp.readline()
       
    #Process the desired partition of the trace
    currentOffset = 0
    thisReference = fp.readline().strip()
    while thisReference != "" and currentOffset < lengthToProcess:

        thisReference = thisReference[0:INDEX_OF_LAST_CHAR_IN_REF]
        
        #We only sample those disk references which satisfy our sampling condition 
        if (hash(thisReference) % 100) < SAMPLE_RATE:
 
            """
            Check if the disk reference is in our sample set
            """
            #If no, this means we have a LOCAL infinity
            if mySampleSet.FindElement(thisReference) == False:
                
                #We must process this local infinity
                try:
                    lastProcessToAccess = globalProcessReferenceDict[globalProcessReferenceDict]
                    if lastProcessToAccess < myWorkerId:
                        #crunch approximate depth
                        approximateDepth = ((myWorkerId - lastProcessToAccess) * lengthToProcess) + currentOffset
                        
                        #This reuse distance needs to be scaled before it is inserted into the histogram
                        rescaleFactor = SAMPLE_RATE/100
                
                        stackDistanceOfThisReference /= rescaleFactor
                        stackDistanceOfThisReference = round(stackDistanceOfThisReference)
                 
                        # Remove it from the stack and re-push it (since the stack distance of this element is now 1)
                        myDistanceTree.RemoveElement(thisReference)
                        myDistanceTree.InsertElement(thisReference)
                     
                        # Update the histogram with the old stack depth of thisReference
                        if SHARDSHistogram.BucketInHistogram(stackDistanceOfThisReference):
                            SHARDSHistogram.IncrementBucket(stackDistanceOfThisReference)
                        else:
                            SHARDSHistogram.AddBucket(stackDistanceOfThisReference, 1)
                        
                    else:
                        #It is really a global infinity
                        #Insert the reference into the sample set
                        mySampleSet.InsertElement(thisReference, hash(thisReference))
                        #Insert the element into the distance tree
                        myDistanceTree.InsertElement(thisReference)
                        #A miss occurred ("infinite" stack depth), record it in the histogram
                        SHARDSHistogram.IncrementBucket(-1)
                except:
                    lastProcessToAccess = -1
                    #It really is a global infinity!
                    #It is really a global infinity
                    #Insert the reference into the sample set
                    mySampleSet.InsertElement(thisReference, hash(thisReference))
                    #Insert the element into the distance tree
                    myDistanceTree.InsertElement(thisReference)
                    #A miss occurred ("infinite" stack depth), record it in the histogram
                    SHARDSHistogram.IncrementBucket(-1)

            #If yes
            else:
                #Since the address is already in the sample set, it is also in the tree. Get the stack depth
                stackDistanceOfThisReference = myDistanceTree.GetDistanceOfElement(thisReference)
                 
                #This reuse distance needs to be scaled before it is inserted into the histogram
                rescaleFactor = SAMPLE_RATE/100
                
                stackDistanceOfThisReference /= SAMPLE_RATE/100
                stackDistanceOfThisReference = round(stackDistanceOfThisReference)
                 
                # Remove it from the stack and re-push it (since the stack distance of this element is now 1)
                myDistanceTree.RemoveElement(thisReference)
                myDistanceTree.InsertElement(thisReference)
                     
                # Update the histogram with the old stack depth of thisReference
                if SHARDSHistogram.BucketInHistogram(stackDistanceOfThisReference):
                    SHARDSHistogram.IncrementBucket(stackDistanceOfThisReference)
                else:
                    SHARDSHistogram.AddBucket(stackDistanceOfThisReference, 1)
                 
            #We need to update the global dictionary
            globalProcessReferenceDict[thisReference] = myWorkerId
        
        thisReference  = fp.readline().strip()
        currentOffset += 1

    return

def Consumer():
    
    return

def go():
    
    #Initialize our thread manager
    myManager = Manager()
    globalProcessReferenceDict = myManager.dict()
    
    fp = open(os.path.join(PATH_TO_TRACE_DIR, "Traces","filteredTrace2.txt"), "r", encoding = "utf-8")

    #Keep a list of each of the processes who are processing a piece of the trace
    workers = []
    tracePartitionLength = ChopTrace(GetNumberReferencesInFile(fp), NUMBER_OF_THREADS)
    #Start the worker threads!   
    for i in range(0, NUMBER_OF_THREADS):
        pid = Process(target = Worker, args = [i, i*tracePartitionLength, tracePartitionLength, globalProcessReferenceDict])
        pid.start()
        workers.append(pid)
             
    for thisWorker in workers:
        thisWorker.join()
    for thisWorker in workers:
        thisWorker.terminate()
    
    return

if __name__ == '__main__':
    go()
