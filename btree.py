

class Btree:
    """
    B-Tree with an order of 3. Sorts in lexicographical order
    """
    ORDER = 3 # specifies max number of children per node 
              # (order - 1) = max number of data points per node

    def __init__(self, meh):
        self.meh = meh
        self.__keys # array of keys
        self.__root # entry point into the btree
        self.__depth

    def find(self, elementNumber):
        """
        Given an element number, returns the k'th element in 
        the B-tree in lexicographical order. 
        If k is out-of-bounds throw an exception.
        """

    def splitNode(self):
        """
        Splits the data from the node. 
        Will also shift the data to the far left of the node to be availble to new data.
        """
    
    def insert(self):
        """
        Insert a new node into the Tree
        """


    
    
