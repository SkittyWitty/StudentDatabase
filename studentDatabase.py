from btree import Btree
from student import Student

class StudentDatabase:
    """
    Interface for the user to store and access information about students.
    """
    def __init__(self):
        self.database = Btree()
        
        # where redId assignments will begin
        self.__lastRedId = 0

    def addNewStudent(self, name, gpa):
        """
        description
            Adds a new student into the database (Btree)
        params
            name - name of the student to be added
            gpa - current gpa of the student to be added
        return 
            None
        """
        self.__lastRedId = self.__lastRedId + 1
        student = Student(name, gpa, self.__lastRedId)
        self.database.insert(student)

    def printProbationaryStudents(self):
        """
        description
            Prints out the Red IDs of students that are on probation 
            (GPA less than 2.85) from the front to the back of the list. 
            i.e A-Z
        params
            None
        return 
            None
        """
        probationaryRange = 2.85 # defined GPA range of students who are on probation
        operation = '<' # less than
        studentsOnProbrationList = self.database.traverse(operation, probationaryRange)
        print(studentsOnProbrationList) # printing list

    def printPerfectGradeStudents(self):
        """
        description
            Prints out the names of students with a GPA of 4.0
            in the list from the back to the front of the list. 
            i.e Z-A
        params
            None
        return 
            None
        """
        perfectGpa = 4.0 # defined as the perfect GPA
        requestedOperation = '=='
        studentsWithPerfectGpaList = self.database.traverse(requestedOperation, perfectGpa)
        print(studentsWithPerfectGpaList[::-1]) # reversing list to print from back to front
    
    def retrieveStudentAtPosition(self, position):
        """
        description
            Retrieves a student at a given position in the list 
            prints out all student info
        params
            position - where in the list to fetch the student object
        return
            None
        """
        studentAtGivenPosition = self.database.grabIndex(position)
        print("Student RedID "  + studentAtGivenPosition.getRedId())
        print("Student Name: "  + studentAtGivenPosition.getName())
        print("Studen GPA: "    + studentAtGivenPosition.getGpa())

if __name__ == '__main__':
    """
    The main function called.
    """
    studentDatabase = StudentDatabase()
    print("Student Database Created")

    pass