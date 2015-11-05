"""
-------------------------------------------------------
PySHARDS Cache Curve Modeling

This is a Python implementation of SHARDS, an extension
of Mattson's MRC construction formulated by Waldspurger et al.
in their 2015 paper "Efficient MRC Construction with SHARDS".
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: October 13, 2015
-------------------------------------------------------
"""
import os
from LRUDistanceTree import LRUTree
from SampleSet import SampleSet
from Histogram import Histogram

PATH_TO_TRACE_DIR = os.path.normpath(os.path.join(os.getcwd(), ".."))

T_MAX = 100

fp = open(os.path.join(PATH_TO_TRACE_DIR, "Traces","sample_trace.txt"), "r", encoding = "utf-8")

mySampleSet = SampleSet(T_MAX)
myHistogram = Histogram()
myDistanceTree = LRUTree()

#Here is a sample trace (I am using integer references for simplicity)
sampleTrace = [1,2,2,3,2,1,4,3,1,1]

#Iterate through address in the trace
for thisReference in sampleTrace:
    
    """
    Check if the disk reference is in our sample set
    If no
    """
    if mySampleSet.FindElement(thisReference) == False:
        #Insert the reference into the sample set
        mySampleSet.InsertElement(thisReference, hash(thisReference))
        #Insert the element into the distance tree
        myDistanceTree.InsertElement(thisReference)
        
        #If a miss occurs ("infinite" stack depth), record it in the histogram
        if myHistogram.BucketInHistogram(-1) == True:
            myHistogram.IncrementBucket(-1)
        else:
            myHistogram.AddBucket(-1,1)
    #Otherwise
    else:
        #Since the address is already in the sample set, it is also in the tree. Get the stack depth
        stackDistanceOfThisReference = myDistanceTree.GetDistanceOfElement(thisReference)
        #Remove it from the stack and re-push it (since the stack distance of this element is now 1)
        myDistanceTree.RemoveElement(thisReference)
        myDistanceTree.InsertElement(thisReference)
        
        #Update the histogram with the old stack depth of thisReference
        if myHistogram.BucketInHistogram(stackDistanceOfThisReference):
            myHistogram.IncrementBucket(stackDistanceOfThisReference)
        else:
            myHistogram.AddBucket(stackDistanceOfThisReference, 1)
                   
print(myHistogram.buckets)
myHistogram.CreateCacheCurve()
        



