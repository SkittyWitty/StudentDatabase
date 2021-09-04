
class Student:
    """
    Interface for a readable student object
    """
    def __init__(self, name, redId, gpa):
        self.name = name
        self.redId = redId
        self.__gpa = gpa

    def getName(self):
        return self.name
    
    def getRedId(self):
        return self.redId
    
    def getGpa(self):
        return self.__gpa
    
