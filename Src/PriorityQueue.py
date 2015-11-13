"""
-------------------------------------------------------
PySHARDS Cache Curve Modeling: Priority Queue class
-------------------------------------------------------
The sample set maintains a priority queue in order to track
potential eviction candidates. 

This is the class definition for this priority queue. The
queue holds tuples (Li, Ti) where Li is a disk reference
and Ti is the threshold value (hash) of that reference.

The higher the threshold of a tuple, the higher the priority
of that tuple.
-------------------------------------------------------
Author:  Tom LaMantia
Email:   tom.lamantia@mail.utoronto.ca
Version: November 12, 2015
-------------------------------------------------------
"""
import operator

class PriorityQueue:
    
    def __init__(self):
        """
        -------------------------------------------------------
        The constructor for the PriorityQueue class
        -------------------------------------------------------
        Preconditions: None
        Postconditions: Initializes an empty priority queue (Python list)
        -------------------------------------------------------
        """
        self.queue = list()
        return
    
    def Enqueue(self, location, threshold):
        """
        -------------------------------------------------------
        Priority queue enqueue operation
        -------------------------------------------------------
        Preconditions: location - some referenced disk address
                        threshold - the hash of location
        Postconditions: Inserts this value into our priority queue.
        -------------------------------------------------------
        """
        value = (location, threshold)
        self.queue.append(value)
        self.queue.sort(key=operator.itemgetter(1))
        return
    
    def Dequeue(self):
        """
        -------------------------------------------------------
        Priority queue dequeue operation
        -------------------------------------------------------
        Preconditions: None
        Postconditions: Returns and removes the highest priority tuple
                        from the queue.
        -------------------------------------------------------
        """
        result = self.queue.pop()
        return result
    
    def PrettyPrint(self):
        """
        -------------------------------------------------------
        Prints the sample set
        -------------------------------------------------------
        Preconditions: None
        Postconditions: Priority Queue is pretty printed to console.
        -------------------------------------------------------
        """
        print(self.queue)
        
        return
    
    