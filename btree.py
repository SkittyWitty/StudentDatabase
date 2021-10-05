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
            data - user is able to intialize the Btree with a set of data
            orderingStrategy - how the Btree will be ordered. Default is "order by key"
        """
        self.__totalPartitions = 0 # keeps track of the length of the BTree
        self.__root = None # entry point into the btree
        self.__orderingStrategy = orderingStrategy
        self.__order = 3 # specifies max number of children per node 

        self.update(data)

    def __getitem__(self, key):
        """
        description
        parameters
        return 
        """
        findResult = self.__root.find(key) 
        if(findResult != None):
            return findResult.value1, findResult.value2
        else:
            raise Exception("There is no element at spot: " + key)

    def __delitem__(self, key):
        """
        deletion is currently not supported.
        """
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
        return External iterator for searching through the BTree in-order
        """
        for item in self.__root.yieldNext():
            yield item.key

    def __len__(self):
        """
        usage: len(btreeObject)
        return Number of items in the BTree 
        """
        return self.__totalPartitions

    def __repr__(self):
        """
        usage: print(btreeObject)
        return an in-order string representation of the Btree
        """
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

    def __toString(self, currentNode, stringList):
        """
        description
            Recurses through each of the children to stringify and append their parition data to the stringList
        params
            currentNode - node that will have it's children searched and partitions added to the list
            stringList - used to append stringified partitions as they are found
        """
        for index, child in enumerate(currentNode.children):
            self.__toString(child, stringList) # Continue search for all children
            if len(currentNode.partitionList) > index: # partition in the node exists add it to the list
                stringList.append(currentNode.partitionToString(index))

    def __reverse(self, currentNode, reverseList):
        """
        description
            Recurses through each of the children in reverse order to stringify and append their parition data to the reverseList
        params
            currentNode - node that will have it's children searched and partitions added to the list
            reverseList - used to append stringified partitions as they are found
        """
        index = self.__order - 1 # Order is 3 giving a max index of 2 when accessing an array
        for child in reversed(currentNode.children):
            if len(currentNode.partitionList) > index: # appending earlier to capture high value elements first
                reverseList.append(currentNode.partitionToString(index))
            self.__reverse(child, reverseList)
            index = index - 1
#end region 

# region public functionaility added for the assignment
    def toString(self):
        """
        description
            public facing function of toString, will kick off recursion from the
            root node and keep all found elements in a string list
        return
            list of all nodes in-order stringified
        """ 
        stringList = []
        self.__toString(self.__root, stringList)
        return stringList

    def getReverse(self):
        """
        description
            An internal iterator that will return a reverse list of partitions within the Btree
        return 
            List of partitions in reverse
        """
        reverseList = []
        self.__reverse(self.__root, reverseList)
        return reverseList
#end region



    
    
