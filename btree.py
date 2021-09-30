from collections import UserDict, namedtuple
import operator # Used to handle traverse filtering
import collections

Partition = namedtuple('Partition', ['key', 'valueList'], defaults=['0', [None, None]])

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
        
        self.partitionList = [] # also referred to as partitions of the node
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
        for index in range(0, self.__order): # Traverse all 3 possibilities for children
            if len(self.children) > index:
                self.children[index].traverse(keyList, operatorFilter, filter) # continue traversing down if child is found
            if len(self.partitionList) > index: # adding nodes keys to the list
                if filter != None and operatorFilter(self.partitionList[index].getValue()[0], filter): # Optional filter
                    keyList.append(self.partitionList[index].key)
                elif filter == None: # Otherwise add all keys to the list
                    keyList.append(self.partitionList[index].key)

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
        if self.partitionList == []: # check for empty list
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
        if(len(self.partitionList) == 0):
            return 0

        # If an index is not found assume it is last in the order 
        index = len(self.partitionList)

        for i, (partition) in enumerate(self.partitionList):
            if (incomingPartition.key < partition.key):
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
        return self.__isLeaf() and len(self.partitionList) == self.__maxKeys

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
        self.parent.__insertKeyValues(self.partitionList[self.__medianIndex])
        del self.partitionList[self.__medianIndex]

        # Establish new right child node 
        newRightChild = BtreeNode()
        newRightChild.parent = self.parent
        # Everything on the right side of the median becomes 
        # the new right nodes children and partitionList
        newRightChild.partitionList = self.partitionList[1:]
        newRightChild.children = self.children[1:]
        for child in newRightChild.children:
            child.parent = newRightChild

        # Everything on the left side of the median becomes
        # current nodes new children and partitionList
        self.partitionList = self.partitionList[:1]	
        self.children = self.children[:1]

        # parent of current node has children ensure they are in the correct order
        if self.parent.children:
            indexOfNewChild = len(self.parent.partitionList)
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
        if not self.partitionList:
            self.partitionList.insert(0, partition)
        else:
            if not index:
                index = self.__findIndex(partition)

            self.partitionList.insert(index, partition)

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

class Btree(UserDict):
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
        self.__totalPartitions = 0 # keeps track of the length of the BTree

        self.__root = None # entry point into the btree

#region Common dictionary interface - Implemented
    def __len__(self):
        """
        len()
        :return: Number of items in the BTree 
        """
        return self.__totalPartitions

    def __next__(self):
        pass

    def __iter__(self):
        """
        External iterator for searching through the BTree 
        """
        whoDeservesBetter = ['cat', 'noir']
        for who in whoDeservesBetter:
            yield who

    def update(self, data):
        """
        description
            Traverses all nodes within the tree 
        parameters
            valueFilter(optional) - filter values of the list
        return 
            keyList - list of all keys in order within the 
        """
        if not self.__root:
            # Currently no root node add one
            self.__root = BtreeNode(True)
        
        partition = self.__generatePartition(data)
        self.__root.insert(partition) # start at top of tree and adjust to add new value

        if not self.__root.isRoot: # root might have changed
            self.__root = self.__root.parent

        # Partition has been added keep track of the length 
        self.__totalPartitions = self.__totalPartitions + 1

    def values(self):
        """
        Return a new view of the dictionary’s values. 
        
        returns an iterator over just the values.

        This is the toArray() method
        """
        pass

    def get(self, key):
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
        if(len(keyList) > key):
            return (keyList[key-1]) # subtract 1 to account for list indices starting at 0
        else:
            raise Exception("There is no element at spot: " + key)

    def __reversed__(self):
        """
        reversed()
        :return: reverse iterator over the keys of the dictionary. Shortcut for reversed(d.keys()).
        """
        raise RuntimeError("reversed iterator is not implemented")
#endRegion

#region Common dictionary interface - Not Implemented/Supported
    def __list__(self):
        """
        list()
        :return: a list of all the keys used in the dictionary d.
        """
        raise RuntimeError("return a list of all elments not implemented")

    def setdefault(self, key, default):
        """
        setdefault
        If key is in the dictionary, return its value. 
        If not, insert key with a value of default and return default. default defaults to None.
        """
        raise RuntimeError("return a list of all elments not implemented")

    def clear(self):
        """
        clear
        Remove all items from the BTree.
        """
        raise RuntimeError("clearing of Btree not implemented")

    def copy(self):
        """
        copy
        Return a shallow copy of the BTree.
        """
        raise RuntimeError("copying of Btree not implemented")

    def pop(self, s = None):
        """
        Function to stop pop from BTree
        """
        raise RuntimeError("Deletion not allowed")
         
    def popitem(self, s = None):
        """
        Function to stop popitem from BTree
        """
        raise RuntimeError("Deletion not allowed")


#endregion

    
    def __generatePartition(self, data):
        """
        description
            Generate a partition to be placed inside the node
        parameters
            data - what is requested to be placed into the BTree
        return 
            Partition containing first value of data as the key
            and all other values placed into the value list of the partition
        """
        # Assume first index is the key
        newPartition = Partition(data[0])

        # All values after the key are assumed to be 
        # values and placed into partitions valueList
        for value in data[1:]:
            newPartition.valueList.insert(value)

        return newPartition


    def traverse(self, requestedOperator='==', valuefilter=None): 
        """
        description
            Internal Iterator that intakes a search strategy 
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




    
    
