import os
import sys
import inspect

# Obtain system path to btree files to import Btree Objects
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from btree import Btree
from btree import Partition
import unittest

"""
    Some tests have written diagrams used for visualizations 
    for tests that will be provided upon request
    - Mindy DeWaal
"""
class BtreeTest(unittest.TestCase):
   def get_length_test(self):
       pass

    




