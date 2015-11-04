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

PATH_TO_TRACE_DIR = os.path.normpath(os.path.join(os.getcwd(), ".."))

T_MAX = 5

fp = open(os.path.join(PATH_TO_TRACE_DIR, "Traces","sample_trace.txt"), "r", encoding = "utf-8")

mySampleSet = SampleSet(T_MAX)

#Testing sample set eviction algorithm

#thisAddress = fp.readline().strip()
for i in range(0,5):
    #print(thisAddress)
    #thisAddress = fp.readline().strip()
    mySampleSet.InsertElement(hex(i), 2*i)
    
mySampleSet.PrettyPrint()
mySampleSet.InsertElement(hex(5), 2*i)
mySampleSet.PrettyPrint()    

