"""
-------------------------------------------------------
PySHARDS Cache Curve Modeling

Contains utilities used by the main program. This includes methods
for conducting SHARDS sampling and processing exact traces.
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: December 1, 2015
-------------------------------------------------------
"""

import sys
sys.path.append("..")
import os
from LRUDistanceTree import LRUTree
from SampleSet import SampleSet
from Histogram import Histogram
from time import clock

PATH_TO_TRACE_DIR = os.path.normpath(os.path.join(os.getcwd(), ".."))

S_MAX = 1024
INDEX_OF_LAST_CHAR_IN_REF = 18

global SAMPLE_RATE

def GenerateExactMRCFromTrace(exactTraceName):

    """
    -------------------------------------------------------
    This program creates an exact MRC curve using my histogram
    class by parsing the output of a Parda trace analysis.
    
    This allows us to compare the cache curves resulting
    from my implementation of SHARDS against the actual cache curve.
    -------------------------------------------------------
    """    
    
    FIRST_LINE = 2
    PATH_TO_TRACE_DIR = os.path.normpath(os.path.join(os.getcwd(), ".."))
    
    fp = open(os.path.join(PATH_TO_TRACE_DIR, "Traces", exactTraceName), "r", encoding = "utf-8")
    
    actualMRCHistogram = Histogram()
    
    for i in range(0,FIRST_LINE):
        thisRecord = fp.readline().strip()
    
    thisRecord = fp.readline().strip()
    while thisRecord != "" and thisRecord[0].isdigit():
        thisRecord = thisRecord.split()
        actualMRCHistogram.AddBucket(int(thisRecord[0]), int(thisRecord[1]))
        thisRecord = fp.readline().strip()
    
    #Need to add the infinite stack depth indicated at the end of the file
    thisRecord = fp.readline().split()
    actualMRCHistogram.AddBucket(-1, int(thisRecord[1]))
    
    return actualMRCHistogram

def ClassicLRUSHARDS(traceName):
    
    """
    Since this is fixed size SHARDS, start by sampling every reference. The sampling rate
    will be lowered accordingly as the SampleSet reaches maximum capacity.
    """
    SAMPLE_RATE = 0.5

    mySampleSet = SampleSet(S_MAX)
    SHARDSHistogram = Histogram()
    myDistanceTree = LRUTree()
    i = 0
    
    fp = open(os.path.join(PATH_TO_TRACE_DIR, "Traces",traceName), "r", encoding = "utf-8")
    
    #Get the current time
    t1 = clock()
    
    thisReference = fp.readline().strip()
    while thisReference != "":
        i += 1
        thisReference = thisReference[0:INDEX_OF_LAST_CHAR_IN_REF]

        #We only sample those disk references which satisfy our sampling condition 
        if (hash(thisReference) % 100) < SAMPLE_RATE:
 
            """
            Check if the disk reference is in our sample set
            """
            #If no
            if mySampleSet.FindElement(thisReference) == False:
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
        if i % 10000 == 0:
            print(i)            
        thisReference = fp.readline().strip()

    #SHARDSHistogram.PrintDetailedInfo()
    
    #Get the time again and calculate time elapsed
    t2 = clock()
    #print("Time elapsed: {0}".format(t2 - t1))

    return SHARDSHistogram