"""
-------------------------------------------------------
PySHARDS Cache Curve Modeling: LRUDistanceTree Class
-------------------------------------------------------
This file contains the class definition for the LRU 
distance tree, which holds referenced locations in the sample set
and their corresponding stack distance.

Each entry is a two tuple <Li, Di> where Li is the location of
some referenced location and Di is the current stack depth of that location.
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: October 13, 2015
-------------------------------------------------------
"""

class LRUTree:
    
    def __init__(self):
        """
        -------------------------------------------------------
        The constructor for the LRUTreeClass
        -------------------------------------------------------
        Preconditions: None
        Postconditions: Initializes an empty LRU distance tree
        -------------------------------------------------------
        """
        self.data = dict()
        return
    
    def InsertElement(self, locationToInsert):
        """
        -------------------------------------------------------
        Inserts a new reference, depth pair into the tree
        -------------------------------------------------------
        Preconditions:
            locationToInsert - the value of the referenced
        location to insert into the distance tree.
        Postconditions:
            <locationToInsert, 0> is added to the distance tree
            and each distance already in the tree has its corresponding
            stack distance incremented.
        -------------------------------------------------------
        """
        #Increment stack distances of existing elements
        for thisLocation in self.data.keys():
            self.data[thisLocation] += 1
        
        #Insert the new value into the tree
        self.data[locationToInsert] = 1
        
        return

    def RemoveElement(self, locationToRemove):
        """
        -------------------------------------------------------
        Removes a reference from the tree
        -------------------------------------------------------
        Preconditions:
            locationToRemove - the value of the referenced
        location to remove from the distance tree.
        Postconditions:
            The reference is removed from the tree. Furthermore, when
            <locationToRemove, di> is removed, all references with distance
            initially greater than di must be decremented.
        -------------------------------------------------------
        """
        distanceOfElementToRemove = self.data[locationToRemove]
        
        #Update the stack depths to reflect impending removal. 
        for thisLocation in self.data.keys():
            if self.data[thisLocation] > distanceOfElementToRemove:
                self.data[thisLocation] -= 1
        
        #Remove the desired reference
        del self.data[locationToRemove]
    
        return
    
    def GetDistanceOfElement(self, thisLocation):
        """
        -------------------------------------------------------
        Lookup reuse distance in the tree
        -------------------------------------------------------
        Preconditions:
            locationToRemove - the value of the referenced
        location to query
        Postconditions:
            Returns the reuse distance of locationToRemove
        -------------------------------------------------------
        """
        return self.data[thisLocation]
    
    def PrettyPrint(self):
        """
        -------------------------------------------------------
        Prints the distance tree
        -------------------------------------------------------
        Preconditions: None
        Postconditions: Distance tree is pretty printed to console.
        -------------------------------------------------------
        """
        for thisReference in self.data.keys():
            print("<{0} {1}> ".format(thisReference, self.data[thisReference]),end='')
        print()
        
        return