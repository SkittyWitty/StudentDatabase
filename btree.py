class BtreeNode:
    """
    Node in a B-tree of order 3. Meaning that 2 data items will be allowed in the node.
    """
    def __init__(self, leaf):
        self.__order = 3

        self.childern = []
        self.seperators = [] # seperation values to divide the node's subtrees
        self.data = [] # data objects that correspond to the keys
        
        # values must be tuples so they are not edited while in the Sorted Tree
        self.isRoot = False # Allowed to have less than the required 

    def traverse(self):
        """
        Look through the data items in the node
        """
        for i in range(self.__order - 1):
            if(self.isLeaf() == False): # not empty visit children
                self.childern[i].traverse() # traverse all subtrees

            # After getting to the bottom of the search print the keys
            print(self.seperators)
        
        # Print subtree of last child
        if(self.isLeaf == False):
            self.children[self.__order].traverse()          
    
    def search(k):
        """
        """
    
    def isLeaf(self):
        """
        When a node is empty with no seperators it is considered a leaf node.
        Get the status of current Node
        """
        if(self.seperators == []):
            return True
        else:
            return False

class Btree:
    """
    B-Tree with an order of 3. Sorts in lexicographical order
    """
    ORDER = 3 # specifies max number of children per node 
              # (order - 1) = max number of data points per node

    def __init__(self):
        self.__root  = BtreeNode() # entry point into the btree
        self.__order = 3

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

    def splitNode(self):
        """
        Splits the data from the node. 
        Will also shift the data to the far left of the node to be availble to new data.
        """
    
    def insert(self):
        """
        Insert a new node into the Tree
        """


    
    
