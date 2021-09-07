import os
import sys
import inspect

# Obtain system path to Btree files to import
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

    def test_findIndex_returnZero(self):
        testNode = BtreeNode(True)
        testNode.keyValuePairs = [BtreeNodePartition("Bethany", 1), BtreeNodePartition("Vlad", 2)]
        testPartition = BtreeNodePartition("Applejack", 123)
        index = testNode._BtreeNode__findIndex(testPartition)

        assert index == 0

    def test_findIndex_returnOne(self):
        testNode = BtreeNode(True)
        testNode.keyValuePairs = [BtreeNodePartition("Adrian", 1), BtreeNodePartition("Marinette", 3)]
        testPartition = BtreeNodePartition("Luca", 123)
        index = testNode._BtreeNode__findIndex(testPartition)

        assert index == 1
    
    def test_findIndex_returnTwo(self):
        testNode = BtreeNode(True)
        testNode.keyValuePairs = [BtreeNodePartition("Catnoir", 2), BtreeNodePartition("Ladybug", 4)]
        testPartition = BtreeNodePartition("Renarouge", 123)
        index = testNode._BtreeNode__findIndex(testPartition)

        assert index == 2

    def test_initialization(self):
        """
        Initialization of a BtreeNode places variables in the expected areas
        """
        testKey = "Min-slice"
        testValue = 123
        testPartition = BtreeNodePartition(testKey, testValue)
        testNode = BtreeNode(True)
        testNode.insert(testPartition)

        assert testNode.children == []
        assert testNode.parent == None
        assert testNode.keyValuePairs[0] == testPartition
        assert testNode._BtreeNode__order == 3

    def test_createNewRoot(self):
        # Set-up 
        testKey = "Min-slice"
        testValue = 123
        testPartition = BtreeNodePartition(testKey, testValue)
        testNode = BtreeNode(True)
        testNode.insert(testPartition)

        # Call
        testNode._BtreeNode__createNewRoot()

        # Assert
        assert testNode.parent.isRoot == True # new parent node is the root
        assert testNode.isRoot == False # current node no longer root

    def test_isOverflowing(self):
        """
        Test discerns that the node is full when 
        there are more than 3 key value pairs
        """
        testBtree = BtreeNode()
        testBtree.keyValuePairs = [(1,1),(1,1)]
        assert testBtree._BtreeNode__isOverflowing() == True

    def test_insert_isEmpty(self):
        """
        Test insert when node is currently empty
        """
        testKey = "Min-slice"
        testValue = 123
        testPartition = BtreeNodePartition(testKey, testValue)
        testNode = BtreeNode(True)
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
        testNode = BtreeNode(True)

        # Insert both partitions into the node
        testNode.insert(testPartition)
        testNode.insert(testPartition2)

        assert testNode.keyValuePairs == [testPartition, testPartition2]

    def test_insert_incomingIsGreatest(self):
        """
        Test insert when the node is about to overflow
        """
        # Set-up
        # Creating what should be the left child
        leftKey = "Almond"
        leftValue = 222
        leftPartition = BtreeNodePartition(leftKey, leftValue)

        # Creating what should be the middle node
        medianKey = "Bethany"
        medianValue = 111
        medianPartition = BtreeNodePartition(medianKey, medianValue)

        # Creating what should be the right child
        rightKey = "Chloe"
        rightValue = 333
        rightPartition = BtreeNodePartition(rightKey, rightValue)

        # Call
        startNode = BtreeNode(True) # future left node starts off as the root node
        startNode.insert(leftPartition)
        startNode.insert(medianPartition)
        startNode.insert(rightPartition)

        # Assert
        # median Node should become the new root 
        assert startNode.parent.isRoot == True
        # startNode should now have median as it's parent
        assert startNode.parent.keyValuePairs[0].getKey() == medianKey

        # Now that parent is confirmed to be Bethany check 
        newRoot = startNode.parent
        assert newRoot.children[0].keyValuePairs[0].getKey() == leftKey  # To the left is Almond
        assert newRoot.children[1].keyValuePairs[0].getKey() == rightKey # To the right is Chloe

    def test_insert_fullTreeCopiesChildren(self):
        """
        When there is an overflow and subtrees are full ensure that
        """

    def test_insert_thirdNodeAppearance(self):
        firstRoot = BtreeNode(True)
        firstRoot.insert(BtreeNodePartition("Effy", 2))
        assert firstRoot.keyValuePairs[0].getKey() == "Effy"

        firstRoot.insert(BtreeNodePartition("Bernie", 1))
        assert firstRoot.keyValuePairs[0].getKey() == "Bernie"
        assert firstRoot.keyValuePairs[1].getKey() == "Effy"

        firstRoot.insert(BtreeNodePartition("Twili", 3))
        # a new root has been found kinged
        newRoot = firstRoot.parent
        assert newRoot.keyValuePairs[0].getKey() == "Effy"
        assert newRoot.children[0].keyValuePairs[0].getKey() == "Bernie"
        assert newRoot.children[1].keyValuePairs[0].getKey() == "Twili"

        newRoot.insert(BtreeNodePartition("Usui", 4))
        # Usui joins Twili
        assert newRoot.children[1].keyValuePairs[0].getKey() == "Twili"
        assert newRoot.children[1].keyValuePairs[1].getKey() == "Usui"

        newRoot.insert(BtreeNodePartition("Zecora", 5))
        # Still expecting same root
        assert newRoot.keyValuePairs[0].getKey() == "Effy"
        # check out new child
        assert newRoot.children[2].keyValuePairs[0].getKey() == "Zecora"


    def test_insert_incomingIsMedian(self):
        """
        When there is an overflow and the incoming partition is not the median
        """
        # Set-up
        # Creating what should be the left child
        leftKey = "Eminem"
        leftValue = 222
        leftPartition = BtreeNodePartition(leftKey, leftValue)

        # Creating what should be the middle node
        medianKey = "Goose"
        medianValue = 111
        medianPartition = BtreeNodePartition(medianKey, medianValue)

        # Creating what should be the right child
        rightKey = "Maverik"
        rightValue = 333
        rightPartition = BtreeNodePartition(rightKey, rightValue)

        # Call
        startNode = BtreeNode(True) # future left node starts off as the root node
        startNode.insert(leftPartition)
        assert startNode.keyValuePairs[0].getKey() == leftKey

        startNode.insert(rightPartition) # inserting right partition first
        assert startNode.keyValuePairs[1].getKey() == rightKey

        startNode.insert(medianPartition)

        # Assert
        # median Node should become the new root 
        assert startNode.parent.isRoot == True
        # startNode should now have median as it's parent
        assert startNode.parent.keyValuePairs[0].getKey() == medianKey

        # Now that parent is confirmed to be Goose check 
        newRoot = startNode.parent
        assert newRoot.children[0].keyValuePairs[0].getKey() == leftKey  # To the left is Eminem
        assert newRoot.children[1].keyValuePairs[0].getKey() == rightKey # To the right is Maverik

    def test_insert_incomingIsLeastest(self):
        """
        Test insert when node is full and incoming parition will be the lesser value
        out of all current keyValuePairs
        """
        # Set-up
        # Creating what should be the left child
        leftKey = "Applejack"
        leftValue = 222
        leftPartition = BtreeNodePartition(leftKey, leftValue)

        # Creating what should be the middle node
        medianKey = "Rarity"
        medianValue = 111
        medianPartition = BtreeNodePartition(medianKey, medianValue)

        # Creating what should be the right child
        rightKey = "Yuna"
        rightValue = 333
        rightPartition = BtreeNodePartition(rightKey, rightValue)

        # Call
        startNode = BtreeNode(True) # future left node starts off as the root node
        startNode.insert(medianPartition)
        assert startNode.keyValuePairs[0].getKey() == medianKey #added successfully

        startNode.insert(rightPartition) # inserting right partition first
        assert startNode.keyValuePairs[1].getKey() == rightKey #added successfully

        startNode.insert(leftPartition)

        # Assert
        # startNode becomes Applejack which is the left most node now
        assert startNode.isRoot == False
        assert startNode.keyValuePairs[0].getKey() == leftKey

        # Check that parent is Rarity
        assert startNode.parent.keyValuePairs[0].getKey() == medianKey  # To the left is Eminem
        
        # Check that Rarity has Applejack as left child Yuna as right child
        assert startNode.parent.children[0].keyValuePairs[0].getKey() == leftKey # To the right is Maverik
        assert startNode.parent.children[1].keyValuePairs[0].getKey() == rightKey # To the right is Maverik

    def test_isEmpty(self):
        """
        Test discerns that the node is empty
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
        assert testBtree._Btree__root == None


    def test_insert_empty(self):
        """
        When the BTree is empty a root node is created and 
        populated with the given partition
        """
        testBtree = Btree()

        # Set up a partition to insert
        testKey = "Plagg"
        testValue = 11
        testPartition = BtreeNodePartition(testKey, testValue)
        
        # Call
        testBtree.insert(testPartition)

        # Assert
        assert testBtree._Btree__root != None
        assert testBtree._Btree__root.keyValuePairs[0].getKey() == testKey

    def test_traverse_basic(self):
        testBtree = Btree()

        # Set up a partition to insert
        testKey = "Plagg"
        testValue = 11
        testPartition = BtreeNodePartition(testKey, testValue)
        
        # Call
        testBtree.insert(testPartition)
        myList = testBtree.traverse()
        assert myList == ["Plagg"]
    
    def test_traverse_twoTierTree(self):
        # Set-up
        # Creating what should be the left child
        testBtree = Btree()

        leftKey = "Applejack"
        leftValue = 222
        leftPartition = BtreeNodePartition(leftKey, leftValue)

        # Creating what should be the middle node
        medianKey = "Rarity"
        medianValue = 111
        medianPartition = BtreeNodePartition(medianKey, medianValue)

        # Creating what should be the right child
        rightKey = "Yuna"
        rightValue = 333
        rightPartition = BtreeNodePartition(rightKey, rightValue)

        # Call
        testBtree.insert(leftPartition)
        testBtree.insert(medianPartition)
        testBtree.insert(rightPartition)
        testListOfKeys = testBtree.traverse() 
        assert testListOfKeys == [leftKey, medianKey, rightKey]


    def test_traverse_thirdNodeAppearance(self):
        testBtree = Btree()
        testBtree.insert(BtreeNodePartition("Effy", 2))
        testBtree.insert(BtreeNodePartition("Bernie", 1))
        testBtree.insert(BtreeNodePartition("Twili", 3))
        testBtree.insert(BtreeNodePartition("Usui", 4))
        testBtree.insert(BtreeNodePartition("Zecora", 5))
        testBtree.insert(BtreeNodePartition("Catnoir", 45))

        testListOfKeys = testBtree.traverse()

        assert testListOfKeys == ["Bernie", "Catnoir", "Effy", "Twili", "Usui", "Zecora"]






