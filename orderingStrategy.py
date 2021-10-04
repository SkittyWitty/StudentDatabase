
"""
 Defintion
"""

def orderByGpa(incomingPartition, currentPartition):
    return incomingPartition.value1 < currentPartition.value1

def orderbyRedID(incomingPartition, currentPartition):
    return incomingPartition.value2 < currentPartition.value2

def orderByName(incomingPartition, currentPartition):
    return incomingPartition.key < currentPartition.key