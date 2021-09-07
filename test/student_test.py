import pytest
import unittest

import os
import sys
import inspect

# Obtain system path to student file to import Student object
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from student import Student

class StudentClassTests(unittest.TestCase):   
    def test_student_getters(self):
        """
        Tests getters at the student level and inherited BtreeNodePartition Level
        """
        studentName = "Min-slice"
        testStudent = Student(studentName, 4.0, 1)

        assert testStudent.getName() == studentName
        assert testStudent.getGpa() == 4.0

        # Still able to access from the BtreeNodePartition
        assert testStudent.getKey() == studentName
        assert testStudent.getValue() == (4.0, 1)

    