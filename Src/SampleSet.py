"""
-------------------------------------------------------
PySHARDS Cache Curve Modeling: SampleSet class
-------------------------------------------------------
This file contains the class definition for the set
of sampled disk references.
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: November 04, 2015
-------------------------------------------------------
"""
from PriorityQueue import PriorityQueue

class SampleSet:
    
    def __init__(self, initialMaxCardinality):
        """
        -------------------------------------------------------
        The constructor for the SampleSet class
        -------------------------------------------------------
        Preconditions: None
        Postconditions: Initializes an empty SampleSet (Python dictionary)
        -------------------------------------------------------
        """
        self.sMax = initialMaxCardinality
        self.tMax = None
        self.tMaxLocation = None
        self.data = dict()
        self.evictionCandiates = PriorityQueue()
        
        return
    
    def GetTMax(self):
        """
        -------------------------------------------------------
        Getter method for tMax
        -------------------------------------------------------
        Preconditions: None
        Postconditions: Returns self.tMax
        -------------------------------------------------------
        """
        return self.tMax
    
    def UpdateTMax(self, newTMax):
        
        self.tMax = newTmax
        
        return
    
    def InsertElement(self, thisLocation, thisThreshold):
        """
        -------------------------------------------------------
        Inserts an element into the SampleSet
        -------------------------------------------------------
        Preconditions: 
            thisLocation: the location which is now being sampled
            thisThreshhold: the hash value of thisLocation
        Postconditions: 
            Inserts thisLocation and its associated threshold value
            into the sample set. tMax and its associated location are also
            updated if thisThreshold exceeds the current tMax. If this insertion
            makes the cardinality exceed sMax, then the location with threshold
            tMax is evicted.
            Returns: evictedElement - the location Li of the tuple <li, ti> which
            was evicted to make space for the new tuple inserted.
        -------------------------------------------------------
        """
        evictedElement = None
        #Insert the value into the sample set
        self.data[thisLocation] = thisThreshold
        #Insert the value into the priority queue
        self.evictionCandiates.Enqueue(thisLocation, thisThreshold)
          
        if len(self.data) > self.sMax:
            #Remove evicted element from the distance tree in user program!
            evictedElement = self.tMaxLocation
            del self.data[self.tMaxLocation]
            
            #Need to update tMax, tMax location
            evictedTuple = self.evictionCandiates.Dequeue()
            self.tMaxLocation = evictedTuple[0]
            self.tMax = evictedTuple[1]
        else:
            #Update the threshold (if necessary)
            if (self.tMax == None) or (thisThreshold > self.tMax):
                evictedTuple = self.evictionCandiates.Dequeue()
                self.tMaxLocation = evictedTuple[0]
                self.tMax = evictedTuple[1]
                
        return evictedElement
    
    def FindElement(self, thisTargetLocation):
        """
        -------------------------------------------------------
        Determines if a target location is in the SampleSet
        -------------------------------------------------------
        Preconditions: 
            thisTargetLocation - the location to be queried in the SampleSet
        Postconditions: 
            Returns - True if thisTargetLocation is in the SampleSet,
            False otherwise.
        -------------------------------------------------------
        """
        #result = False
        
        try:
            value = self.data[thisTargetLocation]
            result = True
        except:
            result = False
        
        return result
    
    def PrettyPrint(self):
        """
        -------------------------------------------------------
        Prints the sample set
        -------------------------------------------------------
        Preconditions: None
        Postconditions: Sample set is pretty printed to console.
        -------------------------------------------------------
        """
        for thisLocation in self.data.keys():
            print("<{0} {1}> ".format(thisLocation, self.data[thisLocation]),end='')
        print()
        
        return
    