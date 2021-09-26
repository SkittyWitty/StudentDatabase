import unittest

import os
import sys
import inspect

# Obtain system path to student file to import Student object
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from studentDatabase import StudentDatabase

class StudentClassTests(unittest.TestCase):   
    def test_studentDatabase_getters(self):
        """
        Tests getters at the student level and inherited BtreeNodePartition Level
        """
        testStudentDatabase = StudentDatabase()
        testStudentDatabase.addNewStudent("Jay-z", 4.0)
        testStudentDatabase.addNewStudent("Tupac", 4.0)
        testStudentDatabase.addNewStudent("Naz", 2.0)
        testStudentDatabase.addNewStudent("Vinny", 2.0)
        testStudentDatabase.addNewStudent("Min-slice", 4.0)

        # Need a way to test list that is only printed and not in a variable
        testStudentDatabase.printProbationaryStudents()
        testStudentDatabase.printPerfectGradeStudents()
        testStudentDatabase.retrieveStudentAtPosition(1)

    