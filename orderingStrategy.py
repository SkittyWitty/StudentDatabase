
"""
Contains all possible stratgies that may be used by the Student Database
"""

def orderByGpa(incomingPartition, currentPartition):
    # Order Database by GPA known the be the second value in a data entry partition
    return incomingPartition.value1 < currentPartition.value1

def orderbyRedID(incomingPartition, currentPartition):
    # Order Database by Red ID known the be the second value in a data entry partition
    return incomingPartition.value2 < currentPartition.value2

def orderByName(incomingPartition, currentPartition):
    # Order Database by Name known the be the second value in a data entry partition
    return incomingPartition.key < currentPartition.key