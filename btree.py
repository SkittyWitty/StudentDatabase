import operator # Used to handle traverse filtering

class BtreeNodePartition:
    """
    Contains the key, value pair of one partion of a BTree's node.
    To act only as an abstract class. 

    Class protects from editing as BTree balance would be disturbed by 
    changing key/value pairs
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def getKey(self):
        """
        description:
            public accessor for the key
        param
            None
        return
            key that has been stored in the partition
        """
        return self.key

    def getValue(self):
        """
        description:
            public accessor for the value
        param
            None
        return
            value that has been stored in the partition
        """
        return self.value


class BtreeNode:
    """
    Node in a B-tree of order 3. 
    Meaning that (order - 1) = 2 data items will be allowed in the node.
    """
    def __init__(self, isRoot=False):
        """
        description
            initializes the BtreeNode by creating an empty node
            with no children or key/value pairs
        params
            isRoot - specifies if this node ia the root of a tree
        return
            None
        """
        self.__order = 3 # specifies max number of children per node 
        self.__maxKeys = self.__order - 1 # max number of key/value pairs per node

        self.children = []
        self.parent = None
        
        self.keyValuePairs = [] # also referred to as partitions of the node
        self.isRoot = isRoot # Allowed to have less than the required 
        self.__medianIndex = 1 # the index of the median value when dealing with overflow d will always be 1

    def traverse(self, keyList, operatorFilter, filter=None):
        """
        description:
            Visit each child and partition in the node 
            adding each key visited to a list
        param:
            keyList -   list of all keys that will be added to
                        each recursive call
        return
            keyList (see params)
        """ 
        for index in range(0, self.__order): # Traverse all 3 possibilities of children
            if len(self.children) > index:
                self.children[index].traverse(keyList, operatorFilter, filter) # continue traversing down if child is found
            if len(self.keyValuePairs) > index: # adding nodes keys to the list
                if filter != None and operatorFilter(self.keyValuePairs[index].getValue()[0], filter): # Optional filter
                    keyList.append(self.keyValuePairs[index].getKey())
                elif filter == None: # Otherwise add all keys to the list
                    keyList.append(self.keyValuePairs[index].getKey())

        return keyList

    def isEmpty(self):
        """
        description
            checks if node is empty by checking number of partitioning
            key/value pairs within the node
        params
            None
        return 
            True when the node
        """
        if self.keyValuePairs == []: # check for empty list
            return True
        else:
            return False

    def __isLeaf(self):
        """
        description
            Checks if the node has children
        params
            None        
        returns
            True when the node has no children
        """
        if self.children == []:
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

    def __findIndex(self, incomingPartition):
        """
        description
            
        params
            partition - partition to be inserted
            index - where in the order the partition would be placed in the list 
                    of key/value pairs (ignoring max keys limiter)
        return
            possible recursion to walk down the children 
            nodes to find a place to insert itself 
        """
        # Handle case for 
        if(len(self.keyValuePairs) == 0):
            return 0

        # If an index is not found assume it is last in the order 
        index = len(self.keyValuePairs)

        for i, (partition) in enumerate(self.keyValuePairs):
            if (incomingPartition.getKey() < partition.getKey()):
                index = i
                break

        return index

    def __isOverflowing(self):
        """
        definition
            decides if node is overflowing when a request to insert occurs
            Checks if number key/value pairs is already at it's limit
            max key
        params
            None
        return
            True if the node will be overflowing
        """
        return self.__isLeaf() and len(self.keyValuePairs) == self.__maxKeys

    def __splitNode(self):
        """
        definition 
            Helper function to insert. 
            Splits the seperation values from the given node into new nodes.
            Will also shift the data to the far left of the node to be availble to new data.
        params
            None
        return 
            None
        """
		# Moves median up
        self.parent.__insertKeyValues(self.keyValuePairs[self.__medianIndex])
        del self.keyValuePairs[self.__medianIndex]

        # Establish new right child node 
        newRightChild = BtreeNode()
        newRightChild.parent = self.parent
        # Everything on the right side of the median becomes 
        # the new right nodes children and keyValuePairs
        newRightChild.keyValuePairs = self.keyValuePairs[1:]
        newRightChild.children = self.children[1:]
        for child in newRightChild.children:
            child.parent = newRightChild

        # Everything on the left side of the median becomes
        # current nodes new children and keyValuePairs
        self.keyValuePairs = self.keyValuePairs[:1]	
        self.children = self.children[:1]

        # parent of current node has children ensure they are in the correct order
        if self.parent.children:
            indexOfNewChild = len(self.parent.keyValuePairs)
            for i, child in enumerate(self.parent.children):
                if child == self:
                    indexOfNewChild = i + 1
                    break

            self.parent.children.insert(indexOfNewChild, newRightChild)
        else: # parent does not have children 
            self.parent.children = [self, newRightChild] # parent adopts current node and newly created right node
  
    def __insertKeyValues(self, partition, index=None):
        """
        description
            
        params
            partition - partition to be inserted
            index - where in the order the partition would be placed in the list 
                    of key/value pairs (ignoring max keys limiter)
        return
            possible recursion to walk down the children 
            nodes to find a place to insert itself 
        """
        if not self.keyValuePairs:
            self.keyValuePairs.insert(0, partition)
        else:
            if not index:
                index = self.__findIndex(partition)

            self.keyValuePairs.insert(index, partition)

    def insert(self, incomingPartition):
        """
        description
            Determines where data should go based on given seperator values. 
            Traverses and rebalances as it walks down to the level of leaf nodes.
        params
            incomingPartition - the partition that will be added to the Btree
        return
            possible recursion to walk down the children 
            nodes to find a place to insert itself 
        """
        if self.isEmpty():
            # Node is empty
            self.__insertKeyValues(incomingPartition)
        elif self.__isOverflowing(): 
            # Node is full
            self.__insertKeyValues(incomingPartition)
            if self.isRoot:
                self.__createNewRoot()
            self.__splitNode()
        else: # current node has room
            index = self.__findIndex(incomingPartition)
            # decide to insert partition or continue search
            if self.__isLeaf(): # insert partition
                self.__insertKeyValues(incomingPartition, index)
            else: # walk down nodes via recursion
                return self.children[index].insert(incomingPartition)

class Btree:
    """
    BTree data structure with a fixed order of 3.
    Sorts both in lexicographical and numerical order
    """
    def __init__(self):
        """
        description
            Initializes Btree data structure by starting it at the root.
        params
            None
        return
            None
        """
        self.__root  = None # entry point into the btree

    def insert(self, partition):
        """
        description
            Traverses all nodes within the tree adding there keys, in order, to a list.
        parameters
            valueFilter(optional) - filter values of the list
        return 
            keyList - list of all keys in order within the 
        """
        if not self.__root:
            # Currently no root node add one
            self.__root = BtreeNode(True)
        
        self.__root.insert(partition) # start at top of tree and adjust to add new value

        if not self.__root.isRoot: # root might have changed
            self.__root = self.__root.parent

    def traverse(self, requestedOperator='==', valuefilter=None): 
        """
        description
            Traverses all nodes within the tree adding there keys, in order, to a list.
        parameters
            valueFilter(optional)        - filter values of the list
            requestedOperator (optional) - operation that should be performed with filter value while traversing
        return 
            keyList - list of all keys in order within the 
        """
        operatorFilter = self.__getFilterOperator(requestedOperator)

        keyList = []
        if(self.__root != self.__root.isEmpty()): # check if there is a root node with keys to print
            self.__root.traverse(keyList, operatorFilter, valuefilter) # traverse the nodes starting at the root
        
        return keyList 

    def __getFilterOperator(comparator, selectedOperation):
        """
        description
            Mapping of all filter operations.
            # TODO: figure out this function can be added to operator class itself to keep things OO
        params
            comparator - what incoming value will be compared to
            seletedOperation - what operation will be used to do the comparing
        return 
            a function that will filter based on user given specifications
        """
        operations = {'>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            '==': operator.eq}

        return operations[selectedOperation]

    def grabIndex(self, index):
        """
        description 
            Given an index, returns the index of the item in 
            the B-tree in order. If index is out-of-bounds throws an exception.
        parameters
            index - list item number to retrieve
        return
            BtreeNodePartition that matches the index provided
        """
        keyList = self.traverse() # obtain a list of keys
        if(len(keyList) > index):
            return (keyList[index-1]) # subtract 1 to account for list indices starting at 0
        else:
            raise Exception("There is no element at spot: " + index)





    
    
