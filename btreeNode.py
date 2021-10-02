

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
            Decides if node is overflowing when a request to insert occurs
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
