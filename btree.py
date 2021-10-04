from collections.abc import MutableMapping
from btreeNode import BtreeNode
from btreeNode import orderByKey
from btreeNode import Partition

class Btree(MutableMapping):
# region Common dictionary interface
    """
    BTree data structure with a fixed order of 3.
    Sorts both in lexicographical and numerical order
    """
    def __init__(self, data=(), orderingStrategy=orderByKey):
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
        self.__orderingStrategy = orderingStrategy
        self.update(data)

    def __getitem__(self, key):
        findResult = self.__root.find(key) 
        if(findResult != None):
            return findResult.value1, findResult.value2
        else:
            raise Exception("There is no element at spot: " + key)

    def __delitem__(self, key):
        raise RuntimeError("Deletion not allowed")

    def __setitem__(self, key, value):
        """
        description
        parameters
        return 
        """
        if not self.__root:
            # Currently no root node? Create one
            self.__root = BtreeNode(True, self.__orderingStrategy)
        
        partition = self.__generatePartition(key, value)
        self.__root.insert(partition) # insertion begins at the top of the tree allow Btree Node to sort

        if not self.__root.isRoot: # root might have changed
            self.__root = self.__root.parent

        # Partition has been added keep track of the length 
        self.__totalPartitions = self.__totalPartitions + 1

    def __iter__(self):
        """
        External iterator for searching through the BTree 
        """
        currentNode = self.__root

        for item in self.__yieldNext(currentNode):
            yield item.key

    def __len__(self):
        """
        len()
        :return: Number of items in the BTree 
        """
        return self.__totalPartitions

    def __repr__(self):
        reprsentationString = []
        self.__root.traverseToString(reprsentationString)
        return reprsentationString
#endregion

# region Private BTree Functions
    def __generatePartition(self, key, value):
        """
        description
            Generate a partition to be placed inside the node
        return 
            Partition containing first value of data as the key
            and all other values placed into the value list of the partition
        """
        if(len(value) == 2):
            newPartition = Partition(key, value[0], value[1])
        else:
            raise Exception("BTree must requires 2 value items. No more no less.")

        return newPartition

    def __yieldNext(self, currentNode):
        """
        Yield's as the Btree is traverse in-order
        """
        for index in range(0, 3): # Traverse all 3 possibilities for children
            if len(currentNode.children) > index:
                yield from self.__yieldNext(currentNode.children[index]) # "yield from" will await what is yielded from the next function call
            if len(currentNode.partitionList) > index: 
                yield currentNode.partitionList[index] # yield returns the current partition

    def __reverse(self, currentNode, reverseList):
        for index in range(2, -1, -1): # Reverse begins looking at the last most child and partition
            if len(currentNode.partitionList) > index:
                reverseList.append(currentNode.partitionList[index]) # adding nodes keys to the list prior to searching for more
            if len(currentNode.children) > index:
                self.__reverse(currentNode.children[index], reverseList) # continue traversing down if child is found

#end region 

# region public functionaility added for the assignment
    def getReverse(self):
        """
        An internal iterator that will return a reverse list of partitions within the Btree
        """
        reverseList = []
        self.__reverse(self.__root, reverseList)  
        return reverseList
#end region



    
    
