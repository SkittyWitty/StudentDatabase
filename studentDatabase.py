from btree import Btree
import orderingStrategy

class StudentDatabase:
    """
    Interface for the user to store and access information about students.
    """
    def __init__(self, orderingStrategy=orderingStrategy.orderByName):
        # Initially empty database where all student information will be kept
        self.database = Btree((), orderingStrategy)
        
        # Where redId assignments will begin
        self.__lastRedId = 0

        # Index markers for pulling data from retrieved items
        self.__gpaIndex = 0
        self.__redIdIndex = 1
        self.__valueListIndex = 1 # index where the student data is located within a student item

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
        newStudent = (name, [gpa, self.__lastRedId])
        self.database.update([newStudent])

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
        # Acquires all items using the databases built in item view, filters items using a function that checks if a student's GPA less than 2.85
        studentsOnProbrationList = dict(filter(lambda item: item[self.__valueListIndex][self.__gpaIndex] < 2.85, self.database.items()))
        print(studentsOnProbrationList)

    def printPerfectGradeStudents(self):
        """
        description
            Prints out the names of students with a GPA of 4.0
            in the list from the back to the front of the list. 
            i.e Z-A
        """
        # Acquires all items using the databases built in item view,, filters items using a function that checks if a student's GPA is 4.0
        studentsWithPerfectGpaList = dict(filter(lambda item: item[self.__valueListIndex][self.__gpaIndex] == 4.0, self.database.items()))
        print(studentsWithPerfectGpaList)
    
    def retrieveStudentAtIndex(self, position):
        """
        description
            Retrieves a student at a given position in the list 
            prints out all student info
        params
            position - where in the list to fetch the student object
        return
            None
        """
        name, studentData = self.database.get(position)
        gpa, redId = studentData
        print("Student RedID "  + redId)
        print("Student Name: "  + name)
        print("Studen GPA: "    + gpa)

if __name__ == '__main__':
    """
    The main function called.
    """
    studentDatabase = StudentDatabase()
    print("Student Database Created")