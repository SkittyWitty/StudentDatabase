import os
import sys
import inspect

# Obtain system path to btree files to import Btree Objects
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from btree import Btree
from btree import BtreeNode
from btree import Partition
import unittest

"""
    Some tests have written diagrams used for visualizations 
    for tests that will be provided upon request
    - Mindy DeWaal
"""
class BtreeNodeTest(unittest.TestCase):
    """
    Unit tests for the BtreeNodes class
    """
    def test_findIndex_returnZero(self):
        testNode = BtreeNode(True)
        testNode.partitionList = [Partition("Bethany", 1), Partition("Vlad", 2)]
        testPartition = Partition("Applejack", 123)
        index = testNode._BtreeNode__findIndex(testPartition)

        assert index == 0

    def test_findIndex_returnOne(self):
        testNode = BtreeNode(True)
        testNode.partitionList = [Partition("Adrian", 1), Partition("Marinette", 3)]
        testPartition = Partition("Luca", 123)
        index = testNode._BtreeNode__findIndex(testPartition)

        assert index == 1
    
    def test_findIndex_returnTwo(self):
        testNode = BtreeNode(True)
        testNode.partitionList = [Partition("Catnoir", 2), Partition("Ladybug", 4)]
        testPartition = Partition("Renarouge", 123)
        index = testNode._BtreeNode__findIndex(testPartition)

        assert index == 2

    def test_initialization(self):
        """
        Initialization of a BtreeNode places variables in the expected areas
        """
        testKey = "Min-slice"
        testValue = 123
        testPartition = Partition(testKey, testValue)
        testNode = BtreeNode(True)
        testNode.insert(testPartition)

        assert testNode.children == []
        assert testNode.parent == None
        assert testNode.partitionList[0] == testPartition
        assert testNode._BtreeNode__order == 3

    def test_createNewRoot(self):
        # Set-up 
        testKey = "Min-slice"
        testValue = 123
        testPartition = Partition(testKey, testValue)
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
        testBtree.partitionList = [(1,1),(1,1)]
        assert testBtree._BtreeNode__isOverflowing() == True

    def test_insert_isEmpty(self):
        """
        Test insert when node is currently empty
        """
        testKey = "Min-slice"
        testValue = 123
        testPartition = Partition(testKey, testValue)
        testNode = BtreeNode(True)
        testNode.insert(testPartition)
        assert testNode.partitionList[0].key == testKey

    def test_insert_isHalfull(self):
        """
        Inserts seperator correct when current node is half full
        Reordering the seperators if need be
        """
        # Creating test values
        testKey = "Min-slice"
        testValue = 123
        testPartition = Partition(testKey, testValue)
        testPartition2 = Partition("Nina", 454)
        testNode = BtreeNode(True)

        # Insert both partitions into the node
        testNode.insert(testPartition)
        testNode.insert(testPartition2)

        assert testNode.partitionList == [testPartition, testPartition2]

    def test_insert_incomingIsGreatest(self):
        """
        Test insert when the node is about to overflow
        """
        # Set-up
        # Creating what should be the left child
        leftKey = "Almond"
        leftValue = 222
        leftPartition = Partition(leftKey, leftValue)

        # Creating what should be the middle node
        medianKey = "Bethany"
        medianValue = 111
        medianPartition = Partition(medianKey, medianValue)

        # Creating what should be the right child
        rightKey = "Chloe"
        rightValue = 333
        rightPartition = Partition(rightKey, rightValue)

        # Call
        startNode = BtreeNode(True) # future left node starts off as the root node
        startNode.insert(leftPartition)
        startNode.insert(medianPartition)
        startNode.insert(rightPartition)

        # Assert
        # median Node should become the new root 
        assert startNode.parent.isRoot == True
        # startNode should now have median as it's parent
        assert startNode.parent.partitionList[0].key == medianKey

        # Now that parent is confirmed to be Bethany check 
        newRoot = startNode.parent
        assert newRoot.children[0].partitionList[0].key == leftKey  # To the left is Almond
        assert newRoot.children[1].partitionList[0].key == rightKey # To the right is Chloe


    def setup(self):
        leftKey = "Almond"
        leftPartition = Partition(leftKey, 111, 1)

        # Creating what should be the middle node
        medianKey = "Bethany"
        medianPartition = Partition(medianKey, 222, 2)

        # Creating what should be the right child
        rightKey = "Chloe"
        rightPartition = Partition(rightKey, 333, 3)

        # Call
        startNode = BtreeNode(True) # future left node starts off as the root node
        startNode.insert(leftPartition)
        startNode.insert(medianPartition)
        startNode.insert(rightPartition)

        return startNode.parent

    def test_traverseToString(self):
        startNode = self.setup()
        stringList = []
        startNode.traverseToString(stringList)
        assert len(stringList) == 3
        assert stringList[0].__contains__("Almond")
        assert stringList[0].__contains__("111")
        assert stringList[0].__contains__("1")

        assert stringList[2].__contains__("Chloe")
        assert stringList[2].__contains__("333")
        assert stringList[2].__contains__("3")


    def test_find(self):
        """
        Find and returns the parition with the requested key 
        or None if no parition with that key exists
        """
        # setup a basic tree structure with the nodes
        startNode = self.setup()

        # find Chloe which we know is in the tree
        result = startNode.find("Chloe")
        assert result.key == "Chloe"

        # Tomoyo is known to NOT be in the tree confirm None is returned
        result = startNode.find("Tomoyo")
        assert result == None


    def test_insert_fullTreeCopiesChildren(self):
        """
        When there is an overflow and subtrees are full ensure that
        """

    def test_insert_thirdNodeAppearance(self):
        firstRoot = BtreeNode(True)
        firstRoot.insert(Partition("Effy", 2))
        assert firstRoot.partitionList[0].key == "Effy"

        firstRoot.insert(Partition("Bernie", 1))
        assert firstRoot.partitionList[0].key == "Bernie"
        assert firstRoot.partitionList[1].key == "Effy"

        firstRoot.insert(Partition("Twili", 3))
        # a new root has been found
        newRoot = firstRoot.parent
        assert newRoot.partitionList[0].key == "Effy"
        assert newRoot.children[0].partitionList[0].key == "Bernie"
        assert newRoot.children[1].partitionList[0].key == "Twili"

        newRoot.insert(Partition("Usui", 4))
        # Usui joins Twili
        assert newRoot.children[1].partitionList[0].key == "Twili"
        assert newRoot.children[1].partitionList[1].key == "Usui"

        newRoot.insert(Partition("Zecora", 5))
        # Still expecting same root
        assert newRoot.partitionList[0].key == "Effy"
        # check out new child
        assert newRoot.children[2].partitionList[0].key == "Zecora"

        # Quick test of find with a bigger tree
        result = newRoot.find("Usui")
        assert result.key == "Usui"

        result = newRoot.find("Twili")
        assert result.key == "Twili"

    def test_insert_incomingIsMedian(self):
        """
        When there is an overflow and the incoming partition is not the median
        """
        # Set-up
        # Creating what should be the left child
        leftKey = "Eminem"
        leftValue = 222
        leftPartition = Partition(leftKey, leftValue)

        # Creating what should be the middle node
        medianKey = "Goose"
        medianValue = 111
        medianPartition = Partition(medianKey, medianValue)

        # Creating what should be the right child
        rightKey = "Maverik"
        rightValue = 333
        rightPartition = Partition(rightKey, rightValue)

        # Call
        startNode = BtreeNode(True) # future left node starts off as the root node
        startNode.insert(leftPartition)
        assert startNode.partitionList[0].key == leftKey

        startNode.insert(rightPartition) # inserting right partition first
        assert startNode.partitionList[1].key == rightKey

        startNode.insert(medianPartition)

        # Assert
        # median Node should become the new root 
        assert startNode.parent.isRoot == True
        # startNode should now have median as it's parent
        assert startNode.parent.partitionList[0].key == medianKey

        # Now that parent is confirmed to be Goose check 
        newRoot = startNode.parent
        assert newRoot.children[0].partitionList[0].key == leftKey  # To the left is Eminem
        assert newRoot.children[1].partitionList[0].key == rightKey # To the right is Maverik

    def test_insert_incomingIsLeastest(self):
        """
        Test insert when node is full and incoming parition will be the lesser value
        out of all current partitionList
        """
        # Set-up
        # Creating what should be the left child
        leftKey = "Applejack"
        leftValue = 222
        leftPartition = Partition(leftKey, leftValue)

        # Creating what should be the middle node
        medianKey = "Rarity"
        medianValue = 111
        medianPartition = Partition(medianKey, medianValue)

        # Creating what should be the right child
        rightKey = "Yuna"
        rightValue = 333
        rightPartition = Partition(rightKey, rightValue)

        # Call
        startNode = BtreeNode(True) # future left node starts off as the root node
        startNode.insert(medianPartition)
        assert startNode.partitionList[0].key == medianKey #added successfully

        startNode.insert(rightPartition) # inserting right partition first
        assert startNode.partitionList[1].key == rightKey #added successfully

        startNode.insert(leftPartition)

        # Assert
        # startNode becomes Applejack which is the left most node now
        assert startNode.isRoot == False
        assert startNode.partitionList[0].key == leftKey

        # Check that parent is Rarity
        assert startNode.parent.partitionList[0].key == medianKey  # To the left is Eminem
        
        # Check that Rarity has Applejack as left child Yuna as right child
        assert startNode.parent.children[0].partitionList[0].key == leftKey # To the right is Maverik
        assert startNode.parent.children[1].partitionList[0].key == rightKey # To the right is Maverik

    def test_isEmpty(self):
        """
        Test discerns that the node is empty
        """
        testBtree = BtreeNode()
        testBtree.partitionList = []
        assert testBtree.isEmpty() == True
