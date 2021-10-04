

from node import Node

class NullNode(Node):
    def __init__(self):
        self.partitionList = []
    def partitionToString(self, index):
        return ""
    def find(self, key):
        return None
    def isEmpty(self): 
        # does it have partitions
        return True
    def toString(self, list):
        pass
    def reverseList(self, list):
        pass
    def yieldNext(self):
        return None
    def __isLeaf(self):
        pass
    def __createNewRoot(self):
        pass
    def __findIndex(self, incomingPartition):
        pass
    def __isOverflowing(self):
        pass
    def __splitNode(self):
        pass
    def __insertKeyValues(self, partition, index=None):
        pass
    def insert(self, incomingPartition):
        pass