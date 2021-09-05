
from btree import BtreeSubNodeData

class Student(BtreeSubNodeData):
    """
    Interface for a readable student object
    """
    def __init__(self, name, gpa):
        # Creating a tuple to represent student data so it is immutable by outsiders
        studentData = (gpa, self.generateRedId)

        # markers for where in the tuple specific data is located
        self.gpaIndex = 0
        self.redIdIndex = 1

        # Using the student's name as the key and the tuple as the data
        super().__init__(name, studentData)


    def getName(self):
        return super().getKey()
    
    def getRedId(self):
        return super().getValue()[self.redIdIndex]
    
    def getGpa(self):
        return super().getValue()[self.gpaIndex]

    def generateRedId(self):
        """
        Generates a unique sequence of numbers to be used as a students RedID
        """
        return "123"
    
