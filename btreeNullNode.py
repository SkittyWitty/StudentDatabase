

from btreeNode import BtreeNode

class NullNode(BtreeNode):
    def find(self, key):
        return None

    def partitionToString(self, index):
        return ""

    def __repr__(self):
        return ""
