"""
-------------------------------------------------------
This program creates an exact MRC curve using my histogram
class by parsing the output of a Parda trace analysis.

This script allows us to compare the cache curves resulting
from my implementation of SHARDS against the actual cache curve.
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: November 10, 2015
-------------------------------------------------------
"""
import sys
sys.path.append("..")
import os
from Src.Histogram import Histogram

FIRST_LINE = 2
PATH_TO_TRACE_DIR = os.path.normpath(os.path.join(os.getcwd(), ".."))

fp = open(os.path.join(PATH_TO_TRACE_DIR, "Traces","seq.hist"), "r", encoding = "utf-8")

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

print(actualMRCHistogram.buckets)
actualMRCHistogram.CreateCacheCurve()
