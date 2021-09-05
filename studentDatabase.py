from btree import Btree
from student import Student

class StudentDatabase:
    """
    Interface for the user to store and access information about students.
    """
    def __init__(self):
        self.database = Btree()

    def addNewStudent(self, name, gpa):
        """
        Adds a new student into the database (Btree)
        """
        student = Student(name, gpa)
        self.database.insert(name, student)

    def printProbrationStudnets(self):
        """
        Prints out the Red IDs of students that are on probation 
        (GPA less than 2.85) from the front to the back of the list. 
        i.e A-Z
        """

    def printPerfectGradeStudents(self):
        """
        Prints out the names of students with a GPA of 4.0
        in the list from the back to the front of the list. 
        i.e Z-A
        """
    

if __name__ == '__main__':
    """
    The main function called.
    """
    meh = StudentDatabase()
    print("Student Database Created")

    pass