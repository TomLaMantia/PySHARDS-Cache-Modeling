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

if __name__ == '__main__':
    MainParallelSHARDSUtilities.go()