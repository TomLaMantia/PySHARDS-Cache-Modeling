"""
-------------------------------------------------------
PySHARDS Cache Curve Modeling

This is a Python implementation of SHARDS, an extension
of Mattson's MRC construction formulated by Waldspurger et al.
in their 2015 paper "Efficient MRC Construction with SHARDS".
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: December 1, 2015
-------------------------------------------------------
"""
from Histogram import Histogram
import MainUtilities

estimatedCurve = MainUtilities.ClassicLRUSHARDS("filteredTrace2.txt")
exactCurve = MainUtilities.GenerateExactMRCFromTrace("seq2.hist")
estimatedCurve.SetBuckets(exactCurve.GetBuckets())
estimatedCurve.CreateCacheCurve()
