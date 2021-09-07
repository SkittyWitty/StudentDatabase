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
        self.__order = 3 # specifies max number of children per node 
                         # (order - 1) = max number of data points per node

        self.children = []
        self.parent = None
        self.keyValuePairs = [] # partitions of the node

        self.isRoot = isRoot # Allowed to have less than the required 
        self.__medianIndex = 1 # the index of the median will always be 1

    def traverse(self, myList):
        """
        Look through the data items in the node
        """ 
        for index in range(0,3):
            if len(self.children) > index:
                self.children[index].traverse(myList)
            if len(self.keyValuePairs) > index:
                myList.append(self.keyValuePairs[index].getKey())

        return myList

    def traverse(self, myList, filter):
        """
        Look through the data items in the node
        """ 
        for index in range(0,3):
            if len(self.children) > index:
                self.children[index].traverse(myList)
            if len(self.keyValuePairs) > index:
                if self.keyValuePairs[index].getValue() == filter:
                    myList.append(self.keyValuePairs[index].getKey())

        return myList

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
    
    def __createNewRoot(self):
        """
        Creates a new root node that will become the parent of the current Node.
        New root is initialized with no key value pairs
        """
        self.isRoot = False # current node is not the root
        self.parent = BtreeNode(True) # current nodes parent is the new root

    def findIndex(self, incomingPartition):
        # The last possible child 
        if(len(self.keyValuePairs) == 0):
            return 0

        index = len(self.keyValuePairs)

        for i, (partition) in enumerate(self.keyValuePairs):
            # Handle None case
            if (incomingPartition.getKey() < partition.getKey()):
                index = i
                break

        return index

    def isOverflowing(self):
        return len(self.keyValuePairs) == self.__order - 1

    def splitNode(self):
        """
        Helper function to insert. 
        Splits the seperation values from the given node into new nodes.
        Will also shift the data to the far left of the node to be availble to new data.
        """
		# Moves median up
        self.parent.insertKeyValues(self.keyValuePairs[self.__medianIndex])
        del self.keyValuePairs[self.__medianIndex]

        # Establish new right child node 
        newRightChild = BtreeNode()
        newRightChild.parent = self.parent
        # Everything on the right side of the median becomes current Nodes new children and keyValuePairs
        newRightChild.keyValuePairs = self.keyValuePairs[1:]
        newRightChild.children = self.children[1:]
        for child in newRightChild.children:
            child.parent = newRightChild

        self.keyValuePairs = self.keyValuePairs[:1]	
        self.children = self.children[:1]

        if self.parent.children:
            index_of_new_child = len(self.parent.keyValuePairs)
            for i, child in enumerate(self.parent.children):
                if child == self:
                    index_of_new_child = i + 1
                    break

            self.parent.children.insert(index_of_new_child, newRightChild)
            #self.parent.keyValuePairs[(len(self.parent.keyValuePairs) + 1)] = None

        else:
            self.parent.children = [self, newRightChild]

    def set_values(self, partitionList):
        index = 0
        for partition in partitionList:
            self.keyValuePairs[index] = partition
            index = index + 1
    
    def insertKeyValues(self, partition, index=None):
        if not self.keyValuePairs:
            self.keyValuePairs.insert(0, partition)
        else:
            if not index:
                index = self.findIndex(partition)

            self.keyValuePairs.insert(index, partition)

    def insert(self, incomingPartition):
        """
        Determines where data should go based on given seperator values. 
        Traverses and rebalances as it walks down to the level of leaf nodes. 
        """
        if self.isEmpty():
            # Node is empty
            self.insertKeyValues(incomingPartition)
        elif self.isOverflowing(): 
            # Node is full
            self.insertKeyValues(incomingPartition)
            if self.isRoot:
                self.__createNewRoot()
            self.splitNode()
        else: # current node is not overflowing
            # Node has room 
            index = self.findIndex(incomingPartition)
            if self.isLeaf(): # insert partition
                self.insertKeyValues(incomingPartition, index)
            else: # walk down nodes
                return self.children[index].insert(incomingPartition)


class Btree:
    """
    B-Tree with an order of 3. Sorts in lexicographical order
    """
    def __init__(self):
        """
        Initializes Btree data structure
        """
        self.__root  = None # entry point into the btree

    def insert(self, partition):
        """
        """
        if not self.__root:
            # Currently no root node add one
            self.__root = BtreeNode(True)
        
        self.__root.insert(partition) # start at top of tree and adjust to add new value

        if not self.__root.isRoot: # root might have changed
            self.__root = self.__root.parent

    def traverse(self): 
        """
        description
            Traverses all nodes within the tree adding there keys, in order, to a list.
        parameters
            NONE
        return 
            keyList - list of all keys in order within the 
        """
        keyList = []
        if(self.__root != self.__root.isEmpty()): # check if there is a root node with keys to print
            self.__root.traverse(keyList) # traverse the nodes starting at the root
        
        print (keyList)
        return keyList # Returning list for ease of testing

    def findElementNumber(self, elementNumber):
        """
        description
            Finds the element at the specified given number otherwise throw an exception
        parameters
            elementNumber -  
        return 
            keyList - list of all keys in order within the 
        """
        keyList = self.traverse()
        try:
            print (keyList[elementNumber-1])
            return keyList[elementNumber-1]
        except:
            print("Element Number is not valid")
            return None

    def traverseValueFilter(self, valueFilter, valueIndex=0):
        """
        description
            Traverses all nodes within the tree only adding keys
            of that match the value of the given filter.
        parameters
            valueFilter - the value you want to filter for
            valueIndex  - optional index of the value array
        return
            list of al 
        """
        filteredList = []

        return filteredList


    def search(self, query):
        """
        Given a k, returns the k'th element in 
        the B-tree in lexicographical order. 
        If k is out-of-bounds throw an exception.
        """
        if self.__root == self.__root.isEmpty(): # root is empty return None
            return None
        else:
            return self.__root.search(query)





    
    
