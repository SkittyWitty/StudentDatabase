from btree import Btree
from student import Student

class StudentDatabase:
    def __init__(self, meh):
        self.meh = meh

    def addNewStudent(self, name, redId, gpa):
        """
        Adds a new student into the database (Btree)
        """

    def generateRedId(self):
        """
        Generates a unique RedID
        """
        return "123"

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
    The main function called when pacman.py is run
    from the command line:

    > python pacman.py

    See the usage string for more details.

    > python pacman.py --help
    """
    print ("hi")
    #args = readCommand( sys.argv[1:] ) # Get game components based on input
    #//runGames( **args )

    # import cProfile
    # cProfile.run("runGames( **args )")
    pass