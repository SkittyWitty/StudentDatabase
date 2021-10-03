import unittest
#from unittest.mock import MagicMock

import os
import sys
import inspect

# Obtain system path to student file to import Student object
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from studentDatabase import StudentDatabase

class StudentClassTests(unittest.TestCase):   
    def test_addNewStudents(self):
        """
        """
        # Use a dictionary as a makeshift database data structure for testing
        studentDatabase = StudentDatabase()
        studentDatabase.database = dict()

        # Check that intial student was added as expected
        studentDatabase.addNewStudent("Jay-Z", 4.0)
        gpa, redId = studentDatabase.database["Jay-Z"]
        assert(gpa == 4.0)
        assert(redId == 1) # RedID generated by Student Database and intiated at 1

        # Check that additional students may be added
        studentDatabase.addNewStudent("Tupac", 4.0)
        studentDatabase.addNewStudent("Naz", 2.0)
        studentDatabase.addNewStudent("Vinny", 2.0)
        studentDatabase.addNewStudent("Min-slice", 4.0)

        # Check that database is expected size after adding students
        assert(len(studentDatabase.database) == 5)

        # Check that red ID increases in the order they were added
        gpa, redId = studentDatabase.database["Min-slice"]
        assert(redId == 5)


    def test_printPerfectGradeStudents(self):
        """
        Checks that 4.0 is the GPA being passed to filter
        Checks that requested operation is =
           - Assumed that there is nothing above a 4.0 at SDSU
        """
        # Use a dictionary as a makeshift database data structure for testing
        studentDatabase = StudentDatabase()
        studentDatabase.database = dict()

        # Use mock to mock the traverse that returns a filtered list
        #testStudentDatabase.printPerfectGradeStudents()
        


    def test_printProbationaryStudents(self):

        # Use a dictionary as a makeshift database data structure for testing
        studentDatabase = StudentDatabase()
        studentDatabase.database = dict()

        # Use mock to mock the traverse that returns a filtered list
        #testStudentDatabase.printProbationaryStudents()
        
    def test_retrieveStudentAtIndex(self):
        # Use a dictionary as a makeshift database data structure for testing
        studentDatabase = StudentDatabase()
        studentDatabase.database = dict()

        # Use mock to mock the traverse that returns a filtered list
        #testStudentDatabase.retrieveStudentAtPosition(1)
        
    