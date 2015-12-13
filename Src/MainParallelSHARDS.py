"""
-------------------------------------------------------
PySHARDS Cache Curve Modeling

This is a Python implementation of SHARDS, an extension
of Mattson's MRC construction formulated by Waldspurger et al.
in their 2015 paper "Efficient MRC Construction with SHARDS".

This particular implementation uses additional estimation
techniques to process the trace in parallel.
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: December 2, 2015
-------------------------------------------------------
"""

import MainParallelSHARDSUtilities
import MainSequentialSHARDSUtilities
from time import clock

TRACE_FILE_NAME = "filteredTrace03.txt"
PARDA_OUTPUT_FILENAME = "seq3.hist"

if __name__ == '__main__':
    
    t1 = clock()
    estimatedParallelCurve = MainParallelSHARDSUtilities.go(TRACE_FILE_NAME)
    t2 = clock()
    print("Parallel SHARDS curve constructed in: {0} seconds".format(t2-t1))
    
    t1 = clock()
    estimatedSequentialCurve = MainSequentialSHARDSUtilities.ClassicLRUSHARDS(TRACE_FILE_NAME)
    t2 = clock()
    print("Sequential SHARDS curve constructed in: {0} seconds".format(t2-t1))
    exactCurve = MainSequentialSHARDSUtilities.GenerateExactMRCFromTrace(PARDA_OUTPUT_FILENAME)
    
    estimatedParallelCurve.SetSecondaryCurveBuckets(estimatedSequentialCurve.GetBuckets())
    estimatedParallelCurve.SetTertiaryCurveBuckets(exactCurve.GetBuckets())
    estimatedParallelCurve.CreateCacheCurve()