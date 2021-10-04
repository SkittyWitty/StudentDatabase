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
        self.__order = 3 # specifies max number of children per node 

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
        for item in self.__root.yieldNext():
            yield item.key

    def __len__(self):
        """
        len()
        :return: Number of items in the BTree 
        """
        return self.__totalPartitions

    def __repr__(self):
        representationString = []
        self.__toString(self.__root, representationString)
        return representationString
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

    def __toString(self):
        """
        description
        param
        return
        """ 
        stringList = []
        self.__root.toString(stringList)
        return stringList
#end region 

# region public functionaility added for the assignment
    def getReverse(self):
        """
        An internal iterator that will return a reverse list of partitions within the Btree
        """
        list = []
        self.__root.reverseList(list)
        return list
#end region



    
    
