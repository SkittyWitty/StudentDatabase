import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from btree import Btree
from btree import BtreeNode
from btree import BtreeNodePartition
import pytest
import unittest

class BtreeNodesTest(unittest.TestCase):
    def reset_variables(self, testNode):
        """
        Resets commonly used variables in the BtreeNode
        """
        testNode.keyValuePairs = [None, None]

    def test_initialization(self):
        """
        Initialization of a BtreeNode places variables in the expected areas
        """
        testKey = "Min-slice"
        testValue = 123
        testPartition = BtreeNodePartition(testKey, testValue)
        testNode = BtreeNode(None, True)
        testNode.insert(testPartition)

        assert testNode.children == [None, None, None]
        assert testNode.parent == None
        assert testNode.keyValuePairs[0] == testPartition
        assert testNode._BtreeNode__order == 3

    def test_setPartitionsInOrder(self):
        testKey = "Min-slice"
        testValue = 123
        testPartition = BtreeNodePartition(testKey, testValue)
        testNode = BtreeNode(testPartition, True)

        # At first the testPartition is the first parition in the testNode
        assert testNode.keyValuePairs[0] == testPartition
        
        firstKey = "Almond"
        firstValue = 222
        firstPartition = BtreeNodePartition(firstKey, firstValue)
        testNode._BtreeNode__setPartitionsInOrder(firstPartition)

        # Afterwards the firstPartition should be at the first of the list
        assert testNode.keyValuePairs[0] == firstPartition
        # testPartition should be at the back of the list
        assert testNode.keyValuePairs[1] == testPartition

    def test_isOverflowing(self):
        """
        Test discerns that the node is full when 
        there are more than 3 key value pairs
        """
        testBtree = BtreeNode()
        testBtree.keyValuePairs = [(1,1),(1,1),(1,1)]
        assert testBtree.isOverflowing() == True

    def test_insert_isEmpty(self):
        """
        Test insert when node is currently empty
        """
        testKey = "Min-slice"
        testValue = 123
        testPartition = BtreeNodePartition(testKey, testValue)
        testNode = BtreeNode(None, True)
        testNode.insert(testPartition)
        assert testNode.keyValuePairs[0].getKey() == testKey

    def test_insert_isHalfull(self):
        """
        Inserts seperator correct when current node is half full
        Reordering the seperators if need be
        """
        # Creating test values
        testKey = "Min-slice"
        testValue = 123
        testPartition = BtreeNodePartition(testKey, testValue)
        testPartition2 = BtreeNodePartition("Nina", 454)
        testNode = BtreeNode(None, True)

        # Insert both partitions into the node
        testNode.insert(testPartition)
        testNode.insert(testPartition2)

        assert testNode.keyValuePairs == [testPartition, testPartition2]

    def test_insert_isOverflowing(self):
        """
        Test insert when node is currently empty
        """

        # Creating what should be the left child
        leftKey = "Almond"
        leftValue = 222
        leftPartition = BtreeNodePartition(leftKey, leftValue)
        startNode = BtreeNode(leftPartition, True) # starts off as the root node

        # Creating what should be the middle note
        medianKey = "Bethany"
        medianValue = 111
        medianPartition = BtreeNodePartition(medianKey, medianValue)

        # Creating what should be the right child
        rightKey = "Chloe"
        rightValue = 333
        rightPartition = BtreeNodePartition(rightKey, rightValue)

        startNode.insert(medianPartition)
        startNode.insert(rightPartition)

        # median Node should become the new root 
        #assert startNode.parent.isRoot == True
        
        # startNode should now have median as it's parent
        #assert startNode.parent.getKey() == medianKey


    def test_splitNode(self):
        """
        Tests that the node is split properly when full
        """

    def test_isEmpty(self):
        """
        Test discerns that the node is a leaf
        1.
        """
        testBtree = BtreeNode()
        testBtree.keyValuePairs = [None, None]
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
        populated with the given partition
        """



