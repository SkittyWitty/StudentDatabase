

from btreeNode import BtreeNode

class NullNode(BtreeNode):
    def find(self, key):
        return None