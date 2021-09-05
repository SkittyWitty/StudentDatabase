import pytest
import unittest

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from student import Student

class studentClassTests(unittest.TestCase):   
    def test_studdent_getters(self):
        studentName = "Min-slice"
        testStudent = Student(studentName, 4.0)

        assert testStudent.getName() == studentName
        assert testStudent.getGpa() == 4.0

    