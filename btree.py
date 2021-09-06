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
    def __init__(self, partition=None, isRoot=False):
        self.__order = 3
        self.__maxSubNodes = self.__order - 1

        self.children = [None, None, None]
        self.parent = None
        self.keyValuePairs = [partition, None] # partitions of the node

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
        return True when the node
        """
        if self.keyValuePairs == []:
            return True
        else:
            return False

    def isLeaf(self):
        """
        returns true when the node has no children
        """
        if self.children == []:
            return True
        else:
            return False


    def splitNode(self, partition):
        """
        Helper function to insert. 
        Splits the seperation values from the given node into new nodes.
        Will also shift the data to the far left of the node to be availble to new data.
        """



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

    def createNewRoot(self):
        """
        Creates a new root node that will become the parent of the current Node.
        New root is initialized with no key value pairs
        """
        self.isRoot = False # current node is not the root
        self.parent = BtreeNode(None, True) # current nodes parent is the new root

    
    def insert(self, incomingPartition):
        """
        Determines where data should go based on given seperator values. 
        Traverses and rebalances as it walks down to the level of leaf nodes. 
        """
        if self.isEmpty():
            # Node is empty
            self.keyValuePairs[0] = incomingPartition
        elif self.isFull(): 
            # Node is full
            if self.isRoot:
                self.createNewRoot()
            self.splitNode()
            self.parent.insert(incomingPartition) #insert into parent node
        else: # current node is half empty
            # Node has room 
            index = 3 # The last possible child 
            if self.isLeaf(): # insert partition
                self.setPartitionsInOrder(incomingPartition, index)
            else: # walk down nodes
                # find which child to walk into 3 possible outcomes
                for i, (partition) in enumerate(self.keyValuePairs):
                    if incomingPartition.getKey() < partition.getKey():
                        index = i
                        break
                return self.children[index].insert(partition)


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





    
    
