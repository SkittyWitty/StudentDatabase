

from btreeNode import BtreeNode

class NullNode(BtreeNode):
    def find(self, key):
        return None

    def __repr__(self):
        return ""