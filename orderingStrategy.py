
"""
 Defintion
"""

from btree import Partition

def orderByName(incomingPartition, currentPartition):
    return incomingPartition.value1 < currentPartition.value2
    

def orderByGpa(incomingPartition, currentPartition):
    return incomingPartition.value2 < currentPartition.value2
