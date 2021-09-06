import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from btree import Btree
from btree import BtreeNode
import pytest
import unittest

class BtreeNodesTest(unittest.TestCase):
    def test_insert_isFull(self):
        """
        Check that current node is no longer marked as root 
        and there is a node in the parent
        """


    def test_insert_isFull(self):
        """
        Inserts seperator correctly when current node is full
        """

    def test_insert_isHalfull(self):
        """
        Inserts seperator correct when current node is half full
        Reordering the seperators if need be
        """

    def test_splitNode(self):
        """
        Tests that the node is split properly when full
        """

    def test_isFull(self):
        """
        Test discerns that the node is full when there are 2 seperators in it
        """
        testBtree = BtreeNode()
        testBtree.seperators = [1,1]
        assert testBtree.isFull() == True

    def test_isEmpty(self):
        """
        Test discerns that the node is a leaf
        1.
        """
        testBtree = BtreeNode()
        testBtree.keyValuePairs = []
        assert testBtree.isEmpty() == True


class BtreeTests(unittest.TestCase):
    def test_btree_init(self):
        """
        Check that expected intialization variables 
        are set up to expected values
        """
        testBtree = Btree()


    def test_insert_empty(self):
        """
        When the BTree is empty a root node is created and 
        populated with the given seperator and data
        """
        testBtree = Btree()
        testSeperator = "Min-Slice"
        testData = 10
        testBtree.insert(testSeperator, testData)



