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

TRACE_FILE_NAME = "filteredTrace2.txt"
PARDA_OUTPUT_FILENAME = "seq2.hist"

if __name__ == '__main__':
    estimatedCurve = MainParallelSHARDSUtilities.go(TRACE_FILE_NAME)
    
    exactCurve = MainSequentialSHARDSUtilities.GenerateExactMRCFromTrace(PARDA_OUTPUT_FILENAME)
    estimatedCurve.SetExactCurveBuckets(exactCurve.GetBuckets())
    estimatedCurve.CreateCacheCurve()