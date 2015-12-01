"""
-------------------------------------------------------
PySHARDS Cache Curve Modeling: Histogram Class
-------------------------------------------------------
This file contains the class definition for the Histogram. The
histogram is represented by a dictionary. Here, the keys for the
dictionary represent stack depths. The values for each key represent
the number of references with that stack depth. Here, -1 denotes
an infinite stack depth (reference seen for the first time).
Here {4:3} denotes that 3 references have a stack depth (distance) of 4.
Hence, {distance:number refs with that distance}
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: December 1, 2015
-------------------------------------------------------
"""
import matplotlib.pyplot as plt

class Histogram:
    
    def __init__(self):
        """
        -------------------------------------------------------
        The constructor for the Histogram class
        -------------------------------------------------------
        Preconditions: None
        Postconditions: Initializes an empty histogram
        -------------------------------------------------------
        """
        self.buckets = {-1:0}
        self.bucketsForExactCurve = None
        
        return

    def GetBuckets(self):
        """
        -------------------------------------------------------
        Getter method for the buckets dictionary.
        -------------------------------------------------------
        Preconditions: None
        Postconditions: Returns self.buckets
        -------------------------------------------------------
        """
        return self.buckets
    
    def SetBucketsForExactCurve(self, exactBuckets):
        """
        -------------------------------------------------------
        Setter method for the exact cache curve buckets.
        -------------------------------------------------------
        Preconditions: exactBuckets - a dictionary containing histogram
            buckets for the exact cache curve.
        Postconditions: Initializes bucketsForExactCurve.
        -------------------------------------------------------
        """
        self.bucketsForExactCurve = exactBuckets
        return
    
    def AddBucket(self, thisStackDistance, numOfElementsWithThisDistance):
        """
        -------------------------------------------------------
        Adds a new bucket to our histogram.
        -------------------------------------------------------
        Preconditions: thisStackDistance: an integer representing a
        stack distance.
        numOfElementsWithThisDistance: the number of elements with
        stack distance thisStackDistance
        Postconditions: Corresponding bucket is added to our histogram model.
        -------------------------------------------------------
        """
        self.buckets[thisStackDistance] = numOfElementsWithThisDistance
        
        return
    
    def BucketInHistogram(self, thisStackDistance):
        
        result = False
        if thisStackDistance in self.buckets.keys():
            result = True
        
        return result
    
    def IncrementBucket(self, stackDistanceToIncrement):
        """
        -------------------------------------------------------
        Increment the number of references which have a particular
        stack distance.
        -------------------------------------------------------
        Preconditions: stackDistanceToIncrement: an integer representing
        a given stack depth.
        Postconditions: The value mapped by stackDistanceToIncrement is
        incremented.
        -------------------------------------------------------
        """
        self.buckets[stackDistanceToIncrement] += 1
        
        return
    
    def PrintDetailedInfo(self):
        
        sortedBuckets = list(self.buckets.keys())
        sortedBuckets.sort()
        refCountSoFar = 0
        totalReferences = len(self.buckets)
        
        print("Dist            Refs             %Total Refs            Total References")
        
        for thisRef in sortedBuckets:
            
            numberRefsAtThisDepth = self.buckets[thisRef]
            percentOfTotalRefs = numberRefsAtThisDepth/totalReferences
            refCountSoFar += numberRefsAtThisDepth
            print("{0}            {1}            {2}            {3}".format(thisRef, numberRefsAtThisDepth, percentOfTotalRefs, refCountSoFar))
        
        return
    
    def CreateCacheCurve(self):
        
        """
        -------------------------------------------------------
        Uses Matplotlib to draw a cache curve from the histogram.
        
        This method uses the algorithm described in Mattson et al. (1970).
        -------------------------------------------------------
        Preconditions: None
        Postconditions: Displays the cache curve defined by the histogram
        -------------------------------------------------------
        """
        sortedBuckets = list(self.buckets.keys())
        sortedBuckets.sort()

        yAxis = list()
        nC = 0
        
        L = 0
        for i in sortedBuckets:
            L += self.buckets[i]

        for thisBucket in sortedBuckets:
            if thisBucket != -1:
                nC += self.buckets[thisBucket]
                yAxis.append(nC/L)
                
        for i in range(1,len(sortedBuckets)):
            sortedBuckets[i] *= 8
            sortedBuckets[i] /= 1024

        #Plot the exact cache curve
        plt.plot(sortedBuckets[1:], yAxis, "r-")
        plt.axis([0,sortedBuckets[-1] + 5 ,0,1.1])




        #Plot the estimated cache curve
        sortedBuckets = list(self.bucketsForExactCurve.keys())
        sortedBuckets.sort()

        yAxis = list()
        nC = 0
        
        L = 0
        for i in sortedBuckets:
            L += self.bucketsForExactCurve[i]

        for thisBucket in sortedBuckets:
            if thisBucket != -1:
                nC += self.bucketsForExactCurve[thisBucket]
                yAxis.append(nC/L)
                
        for i in range(1,len(sortedBuckets)):
            sortedBuckets[i] *= 8
            sortedBuckets[i] /= 1024

        #Plot the exact cache curve
        plt.plot(sortedBuckets[1:], yAxis, "g-")      
        
        plt.xlabel("Cache size (KB)")
        plt.ylabel("Cache Hits (%)")
        plt.show()
            
        return
    