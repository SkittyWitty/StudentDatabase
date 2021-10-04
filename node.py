from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self):
        pass
    def partitionToString(self, index):
        pass
    def find(self, key):
        pass
    def isEmpty(self):
        pass
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