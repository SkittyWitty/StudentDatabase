

from node import Node

class NullNode(Node):
    """
    Contains base functionaility that is mostly called when doing traverses.
    Will end the search and return an empty value in a format that Btree or BtreeNode will know how to handle.
    """
    def __init__(self):
        # Null node does not have any paritions or children
        self.partitionList = []
        self.children = []
    def partitionToString(self, index):
        return ""
    def find(self, key):
        # Your node is in another castle
        return None
    def isEmpty(self): 
        # Will alawys be empty
        return True
    def toString(self, list):
        # Pass will not have anything to contribute to the list
        pass
    def reverseList(self, list):
        # Pass will not have anything to contribute to the list
        pass
    def yieldNext(self):
        return None