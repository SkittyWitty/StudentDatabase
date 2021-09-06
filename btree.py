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
        self.__medianIndex = 1 # the index of the median will always be 1

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
        if self.keyValuePairs == [None, None] or self.keyValuePairs == []:
            return True
        else:
            return False

    def isLeaf(self):
        """
        returns true when the node has no children
        """
        if self.children == [] or self.children == [None, None, None]:
            return True
        else:
            return False
    
    def __setPartitionsInOrder(self, partition):
        """
        Orders the seperators in the node and places them in the order.
        Note that python is able to lexicographically sort character by character using compairson operators
        automatically. Therefore this function supports numbers and strings as keys.
        """
        incomingkey = partition.getKey()
        existingPartitionsKey = self.keyValuePairs[0].getKey()
        if(incomingkey > existingPartitionsKey):
             # incoming seperator is bigger
            self.keyValuePairs[1] = partition
        else:
            # incoming seperator is smaller
            self.keyValuePairs[1] = self.keyValuePairs[0]
            self.keyValuePairs[0] = partition

    def __createNewRoot(self):
        """
        Creates a new root node that will become the parent of the current Node.
        New root is initialized with no key value pairs
        """
        self.isRoot = False # current node is not the root
        self.parent = BtreeNode(None, True) # current nodes parent is the new root


    def findIndex(self, incomingPartition):
        index = 3 # The last possible child 

        for i, (partition) in enumerate(self.keyValuePairs):
            # Handle None case
            if incomingPartition.getKey() < partition.getKey():
                index = i
                break

        return index

    def isOverflowing(self):
        return len(self.keyValuePairs) == self.__order

    def __insertMeh(self, partition):
        """
        Ignores the partition limit rule to be able to sort for median
        """
        index = self.findIndex(partition)
        self.keyValuePairs.insert(index, partition)

    def splitNode(self, incomingPartition):
        """
        Helper function to insert. 
        Splits the seperation values from the given node into new nodes.
        Will also shift the data to the far left of the node to be availble to new data.
        """
		# Moves median up
        self.parent.insert(self.keyValuePairs[self.__medianIndex]) #TODO ASSUMING LAST ELEMENT IS THE MEDIAN
        self.keyValuePairs[self.__medianIndex]  = None # delete the median 
        assert self.keyValuePairs[1] == None
        assert self.parent.keyValuePairs[1] == None
        assert len(self.keyValuePairs) < 3

        # Create new right child node
        newRightChild = BtreeNode(incomingPartition) #TODO ASSUMING incoming parition is the right
        newRightChild.parent = self.parent
        #newRightChild.keyValuePairs[0] = self.keyValuePairs[self.__medianIndex:]
        if(not self.isLeaf()): #if there is existing children give them a new parent
            newRightChild.children[0] = self.children[self.__medianIndex:] # grab all the children to the left of the median
            for child in newRightChild.children: # Tell new children who there parents are
                child.parent = newRightChild
            self.keyValuePairs[-1] = self.keyValuePairs[:self.__medianIndex]	#Current node becomes new left node
            self.children[-1] = self.children[:self.__medianIndex]

        if self.parent.children != [None, None, None]: # Parent has children
            indexOfNewChild = self.parent.keyValuePairs[-1] # end if availible slots
            for i, children in enumerate(self.parent.children):
                if children == self:
                    indexOfNewChild = i + 1
                    break

            self.parent.children.insert(indexOfNewChild, newRightChild)
        else: # Parent does NOT have children
            self.parent.children = ([self, newRightChild])
    
    def insert(self, incomingPartition):
        """
        Determines where data should go based on given seperator values. 
        Traverses and rebalances as it walks down to the level of leaf nodes. 
        """
        if self.isEmpty():
            # Node is empty
            self.keyValuePairs[0] = incomingPartition
        elif self.keyValuePairs[0] != None and self.keyValuePairs[1] != None: 
            # Node is full
            if self.isRoot:
                self.__createNewRoot()
            self.splitNode(incomingPartition)
            #self.parent.insert(incomingPartition) # insert into parent node
        else: # current node is not overflowing
            # Node has room 
            if self.isLeaf(): # insert partition
                self.__setPartitionsInOrder(incomingPartition)
            else: # walk down nodes
                index = self.findIndex()
                return self.children[index].insert(incomingPartition)


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





    
    
