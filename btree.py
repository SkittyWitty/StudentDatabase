class BtreeNodePartition:
    """
    Contains the key, value pair of one partion of a BTree's node
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def getKey(self):
        """
        public accessor for the key
        """
        return self.key

    def getValue(self):
        """
        public accessor for the value
        """
        return self.value

    def __setKey(self, key):
        """
        private method for setting the key
        """
        self.key = key

    def __setValue(self, value):
        """
        private method for setting the value
        """
        self.value = value


class BtreeNode:
    """
    Node in a B-tree of order 3. Meaning that 2 data items will be allowed in the node.
    """
    def __init__(self, isRoot=False):
        self.__order = 3
        self.__maxSubNodes = self.__order - 1

        self.children = [None, None, None]
        self.parent = None
        self.keyValuePairs = [None, None] # partitions of the node

        self.isRoot = isRoot # Allowed to have less than the required 

    def traverse(self):
        """
        Look through the data items in the node
        """
        for i in range(self.__order - 1):
            if(self.isEmpty() == False): # not empty visit children
                self.children[i].traverse() # traverse all subtrees

            # After getting to the bottom of the search print the keys
            print(self.keyValuePairs)
        
        # Print subtree of last child
        if(self.isEmpty() == False):
            self.children[self.__order].traverse()          
    
    def search(k):
        """
        """
    
    def isEmpty(self):
        """
        When a node is empty with no keys it is considered a leaf node.
        Get the status of current Node
        """
        if(self.keyValuePairs == []):
            return True
        else:
            return False

    def splitNode(self):
        """
        Helper function to insert. 
        Splits the seperation values from the given node into new nodes.
        Will also shift the data to the far left of the node to be availble to new data.
        """
        # Create new node
        # decides what values 

    def insertSeperation(self):
        """
        Inserts a seperation value into a node ignoring the order restriction.
        """
    
    def insertData(self, partition):
        print("Meh")

    def isFull(self):
        return len(self.keyValuePairs) == self.__maxSubNodes

    def setPartitionsInOrder(self, partition):
        """
        Orders the seperators in the node lexicographically and places them in the 
        """
        incomingkey = partition.getKey()
        existingPartitionsKey = self.keyValuePairs[0].getKey()
        if(existingPartitionsKey < incomingkey):
            # incoming seperator is smaller
            self.keyValuePairs[1] = self.keyValuePairs[0]
            self.keyValuePairs[0] = partition
        else:
             # incoming seperator is bigger
            self.keyValuePairs[1] = partition

    
    def insert(self, partition):
        """
        Determines where data should go based on given seperator values. 
        Traverses and rebalances as it walks down to the level of leaf nodes. 
        """
        if self.isEmpty():
            # Node is empty
            self.keyValuePairs[0] = partition
        elif self.isFull(): 
            # Node is full
            self.splitNode()
            # Insert data into Node, use seperator values to determine order/if reordering if needed
        else: 
            # Node has room 
            self.setPartitionsInOrder(partition)


class Btree:
    """
    B-Tree with an order of 3. Sorts in lexicographical order
    """
    def __init__(self):
        """
        """
        self.__root  = None # entry point into the btree
        self.__order = 3    # specifies max number of children per node 
                            # (order - 1) = max number of data points per node

    def insert(self, partition):
        """
        """
        if not self.__root:
            # Currently no root node add one
            self.__root = BtreeNode(True)
        
        self.__root.insert(partition) # start at top of tree and adjust to add new value

        if not self.__root.isRoot: # root might have changed change
            self.__root = self.__root.parent

    def traverse(self): 
        """
        Start at root.
        """
        if(self.__root != self.__root.isEmpty()):
            self.__root.traverse()

    def search(self, k):
        """
        Given a k, returns the k'th element in 
        the B-tree in lexicographical order. 
        If k is out-of-bounds throw an exception.
        """
        if self.__root == self.__root.isEmpty(): # root is empty return false
            return False
        else:
            return self.__root.search(k)





    
    
