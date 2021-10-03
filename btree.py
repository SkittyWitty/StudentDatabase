from collections.abc import MutableMapping

from btreeNode import BtreeNode
from btreeNode import Partition
import operator # Used to handle traverse filtering


class Btree(MutableMapping):
# region Common dictionary interface
    """
    BTree data structure with a fixed order of 3.
    Sorts both in lexicographical and numerical order
    """
    def __init__(self, data=()):
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
            self.__root = BtreeNode(True)
        
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

        for item in self.yieldNext(currentNode):
            yield item.key

    def yieldNext(self, currentNode):
        for index in range(0, 3): # Traverse all 3 possibilities for children
            if len(currentNode.children) > index:
                yield from self.yieldNext(currentNode.children[index]) # continue traversing down if child is found
            if len(currentNode.partitionList) > index: # adding nodes keys to the list
                yield currentNode.partitionList[index]

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
#end region 

    # Internal traverse
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




    
    
