
from btree import BtreeNodePartition

class Student(BtreeNodePartition):
    """
    Interface for a readable student object.
    Values of a student are private
    """
    def __init__(self, name, gpa, redId):
        """
        description
            retrieves the name from the student object by fetching 
            it out of the underlying BTreeNodePartition
        param
            name - name of the student
            gpa - grade point average of student
            redID - unique identifier
        return 
            None
        """
        # Creating a tuple to represent student data so it is immutable by outsiders
        studentData = (gpa, redId)

        # markers for where in the tuple specific data is located
        self.gpaIndex = 0
        self.redIdIndex = 1

        # Using the student's name as the key and the tuple as the data
        super().__init__(name, studentData)

    def getName(self):
        """
        description
            retrieves the name from the student object by fetching 
            it out of the underlying BTreeNodePartition
        param
            None
        return 
            Name
        """
        return super().getKey()
    
    def getGpa(self):
        """
        description
            retrieves the name from the student object by fetching 
            it out of the underlying BTreeNodePartition
        param
            None
        return 
            Name
        """
        return super().getValue()[self.gpaIndex]

    def getRedId(self):
        """
        description
            retrieves the name from the student object by fetching 
            it out of the underlying BTreeNodePartition
        param
            None
        return 
            Name
        """
        return super().getValue()[self.redIdIndex]
    
