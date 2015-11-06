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
        #Insert the value
        self.data[thisLocation] = thisThreshold
          
        if len(self.data) > self.sMax:
            #Lower global threshold in user program!
            #Remove evicted element from the distance tree in user program!
            evictedElement = self.tMaxLocation
            del self.data[self.tMaxLocation]
            
            #Need to update tMax, tMax location
            thisPair = self.data.popitem()
            self.data[thisPair[0]] = thisPair[1]
            self.tMax = thisPair[1]
            self.tMaxLocation = thisPair[0]
            for thisLi in self.data.keys():
                if self.data[thisLi] > self.tMax:
                    self.tMax = self.data[thisLi]
                    self.tMaxLocation = thisLi
        else:
            #Update the threshold (if necessary)
            if (self.tMax == None) or (thisThreshold > self.tMax):
                self.tMaxLocation = thisLocation
                self.tMax = thisThreshold
                
        return evictedElement
    
    def RemoveElement(self, thisLocation):
        """
        -------------------------------------------------------
        Removes an element from the SampleSet
        -------------------------------------------------------
        Preconditions: 
            thisLocation - the location to be removed from the SampleSet
        Postconditions: 
            thisLocation is removed from the sample set and tMax
            is updated if thisLocation had a threshold equal to the
            previous tMax.
        -------------------------------------------------------
        """
        thisLocationThreshold = self.data[thisLocation]
        
        #Remove the element
        result = self.data[thisLocation]
        del self.data[thisLocation]
        
        #Update tMax, if necessary
        if thisLocationThreshold == self.tMax:
            
            thisPair = self.data.popitem()
            self.data[thisPair[0]] = thisPair[1]
            thisTempTMaxLocation = thisPair[0]
            
            for thisLocation in self.data.keys():
                thisResult = self.data[thisLocation]
                if thisResult > thisTempTMaxLocation:
                    self.tMaxLocation = thisLocation
                    self.tMax = self.data[thisLocation]
        
        return result
    
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
        result = False
        
        if thisTargetLocation in self.data.keys():
            result = True
        
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
    