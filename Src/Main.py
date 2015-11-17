"""
-------------------------------------------------------
PySHARDS Cache Curve Modeling

This is a Python implementation of SHARDS, an extension
of Mattson's MRC construction formulated by Waldspurger et al.
in their 2015 paper "Efficient MRC Construction with SHARDS".
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: November 12, 2015
-------------------------------------------------------
"""
import os
from LRUDistanceTree import LRUTree
from SampleSet import SampleSet
from Histogram import Histogram
from time import clock

PATH_TO_TRACE_DIR = os.path.normpath(os.path.join(os.getcwd(), ".."))

S_MAX = 1024
INDEX_OF_LAST_CHAR_IN_REF = 18

global SAMPLE_RATE

def GenerateExactMRC(fp):
    
    """
    Classic Mattson algorithm
    """
    mySampleSet = SampleSet(S_MAX)
    myHistogram = Histogram()
    myDistanceTree = LRUTree()

    thisReference = fp.readline().strip()
    while thisReference != "":

        thisReference = thisReference[0:INDEX_OF_LAST_CHAR_IN_REF]
        #print(thisReference)
        #We only sample those disk references which satisfy our sampling condition 

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
            myHistogram.IncrementBucket(-1)
        #If yes
        else:
            #Since the address is already in the sample set, it is also in the tree. Get the stack depth
            stackDistanceOfThisReference = myDistanceTree.GetDistanceOfElement(thisReference)
            # Remove it from the stack and re-push it (since the stack distance of this element is now 1)
            myDistanceTree.RemoveElement(thisReference)
            myDistanceTree.InsertElement(thisReference)
            
            #If this insertion caused a disk reference to be evicted, we update the sampling rate accordingly
            #if evictedElement != None:
                #SAMPLING_RATE = mySampleSet.GetTMax()
                
            # Update the histogram with the old stack depth of thisReference
            if myHistogram.BucketInHistogram(stackDistanceOfThisReference):
                myHistogram.IncrementBucket(stackDistanceOfThisReference)
            else:
                myHistogram.AddBucket(stackDistanceOfThisReference, 1)
           
        thisReference = fp.readline().strip()

    myHistogram.PrintDetailedInfo()
    myHistogram.CreateCacheCurve()
    return

def ClassicLRUSHARDS(fp):
    
    """
    Since this is fixed size SHARDS, start by sampling every reference. The sampling rate
    will be lowered accordingly as the SampleSet reaches maximum capacity.
    """
    SAMPLE_RATE = 1

    mySampleSet = SampleSet(S_MAX)
    myHistogram = Histogram()
    myDistanceTree = LRUTree()
    i = 0
    
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
                myHistogram.IncrementBucket(-1)
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
                if myHistogram.BucketInHistogram(stackDistanceOfThisReference):
                    myHistogram.IncrementBucket(stackDistanceOfThisReference)
                else:
                    myHistogram.AddBucket(stackDistanceOfThisReference, 1)
        if i % 10000 == 0:
            print(i)            
        thisReference = fp.readline().strip()

    myHistogram.PrintDetailedInfo()
    print(myHistogram.buckets)
    #Get the time again and calculate time elapsed
    t2 = clock()
    print("Time elapsed: {0}".format(t2 - t1))
    
    myHistogram.CreateCacheCurve()

    return

fp = open(os.path.join(PATH_TO_TRACE_DIR, "Traces","filteredTrace.txt"), "r", encoding = "utf-8")
ClassicLRUSHARDS(fp)
