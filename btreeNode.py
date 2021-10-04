
from collections import namedtuple
from node import Node
from btreeNullNode import NullNode

Partition = namedtuple('Partition', ['key', 'value1', 'value2'], defaults=[0, None, None])

def orderByKey(incomingPartition, currentPartition):
    return incomingPartition.key < currentPartition.key

class BtreeNode(Node):
    """
    Node in a B-tree of order 3. 
    Meaning that (order - 1) = 2 data items will be allowed in the node.
    """
    def __init__(self, isRoot=False, orderingStrategy=orderByKey):
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

        self.children = [NullNode(), NullNode(), NullNode()]
        self.parent = None
        
        self.partitionList = [] # also referred to as partitions of the node
        self.isRoot = isRoot # Allowed to have less than the required 
        self.__medianIndex = 1 # the index of the median value when dealing with overflow d will always be 1

        # Default ordering strategy is to order by key
        self.orderingStrategy = orderingStrategy

    def partitionToString(self, index):
        """
        Converts given partition to a string
        """
        partition = self.partitionList[index]
        return str(partition.key) + ": " + str(partition.value1) + ", "+ str(partition.value2)

    def find(self, key):
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
        # Find the first key greater than or equal to k
        index = 0
        while (index < len(self.partitionList) and key > self.partitionList[index].key):
            index =+ 1
 
        # If the found key is equal to k, return this partition
        if (len(self.partitionList) > index and self.partitionList[index].key == key):
            return self.partitionList[index]
 
        # If the key is not found here and this is a leaf node
        if (self.__isLeaf() == True):
            return None
 
        # Go to the appropriate child
        return self.children[index].find(key)
 
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

    def toString(self, list):
        for index, child in enumerate(self.children):
            child.toString(list)
            if len(self.partitionList) > index: # adding nodes keys to the list
                list.append(self.partitionToString(index))

    def yieldNext(self):
        """
        Yield's as the Btree is traverse in-order
        """
        for index, child in enumerate(self.children):
            if type(child) != NullNode: # Null Nodes should not be visible to the user of the interface and therefore should not yield
                yield from child.yieldNext()
            if len(self.partitionList) > index: # adding nodes keys to the list
                yield self.partitionList[index]


    def __reverse(self, currentNode, reverseList):
        for index in range(2, -1, -1): # Reverse begins looking at the last most child and partition
            if len(currentNode.partitionList) > index:
                reverseList.append(currentNode.partitionList[index]) # adding nodes keys to the list prior to searching for more
            if len(currentNode.children) > index:
                self.__reverse(currentNode.children[index], reverseList) # continue traversing down if child is found


    def reverseList(self, list):
        index = 2
        for child in reversed(self.children):
            if len(self.partitionList) > index: # adding nodes keys to the list
                list.append(self.partitionToString(index))
            child.reverseList(list)
            index = index - 1

    def __isLeaf(self):
        """
        description
            Checks if the node has children
        params
            None        
        returns
            True when the node has no children
        """
        isLeaf = True
        for child in self.children:
            isLeaf = isLeaf and child.isEmpty()
        return isLeaf
            
    def __createNewRoot(self):
        """
        Creates a new root node that will become the parent of the current Node.
        New root is initialized with no key value pairs
        """
        self.isRoot = False # current node is not the root
        self.parent = BtreeNode(True, self.orderingStrategy) # current nodes parent is the new root

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
        # If an index is not found assume it is last in the order 
        index = len(self.partitionList)

        for i, (partition) in enumerate(self.partitionList):
            if self.orderingStrategy(incomingPartition, partition):
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

    def migrate(self, newParentNode, partitions, children):
        newParentNode.partitionList = partitions

        for index in range(0, self.__order):
            if(type is BtreeNode):
                child = children[index]
                child.parent = newParentNode
                newParentNode.children[index] = child
            else:
                newParentNode.children[index] = NullNode()

    def meh(self, indexOfNewChild, newRightChild):
        currentChild = self.parent.children[indexOfNewChild]
        if(type(currentChild) != NullNode):
            self.parent.children[indexOfNewChild+1] = currentChild
            self.parent.children[indexOfNewChild] = newRightChild
        else:
            self.parent.children[indexOfNewChild] = newRightChild

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
        newRightChild = BtreeNode(False, self.orderingStrategy)
        newRightChild.parent = self.parent

        # Everything on the right side of the median becomes 
        # the new right nodes children and partitionList
        self.migrate(newRightChild, self.partitionList[1:], self.children[1:])

        # Everything on the left side of the median becomes
        # current nodes new children and partitionList
        self.migrate(self, self.partitionList[:1], self.children[:1])

        # parent of current node has children ensure they are in the correct order
        if not self.parent.__isLeaf():
            indexOfNewChild = len(self.parent.partitionList)
            for i, child in enumerate(self.parent.children):
                if child == self:
                    indexOfNewChild = i + 1
                    break
            
            self.meh(indexOfNewChild, newRightChild)
            print("hi")
        else: # parent does not have children 
            self.parent.children = [self, newRightChild, NullNode()] # parent adopts current node and newly created right node
  
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
