import os
import sys
import inspect

# Obtain system path to btree files to import Btree Objects
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from btree import Btree
from collections.abc import MutableMapping

from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

class BtreeTest(TestCase):
    def test_subclass(self):
        """
        Checks that the BTree is a subclass of a Mapping collection
        """
        assert issubclass(Btree, MutableMapping)

# region mutable mapping interface tests
    def test_get_length(self):
        testBtree = Btree({
            "Cat Noir" : ["Destruction", "Time"],
            "Ladybug" : ["Creation", "Multiplication"],
            "Rena Rouge" : ["Illusion", "Creation" ]
        })
        btreeLength = len(testBtree)
        assert btreeLength == 3

    def test_init(self):
        """
        Check that expected intialization variables 
        are set up to expected values
        """
        testBtree = Btree({
            "Cat Noir" : ["Destruction", "Time"],
            "Ladybug" : ["Creation", "Multiplication"],
            "Rena Rouge" : ["Illusion", "Creation" ]
        })
        assert testBtree._Btree__root != None
        assert testBtree.get("Cat Noir") == ("Destruction", "Time")
        assert testBtree.get("Ladybug") == ("Creation", "Multiplication")
        assert testBtree.get("Rena Rouge") == ("Illusion", "Creation")

    def test_generatePartition(self):
        """
        Able to generate a partition as expected reguardless of format
        of value in a key, value pair
        """
        testBtree = Btree()
        test1Partition = testBtree._Btree__generatePartition("Cat Noir", ["Destruction", "Time"])
        assert test1Partition.value1 == "Destruction"
        assert test1Partition.value2 == "Time"

        test2Partition = testBtree._Btree__generatePartition("Ladybug", ("Creation", "Multiplication"))
        assert test2Partition.value1 == "Creation"
        assert test2Partition.value2 == "Multiplication"

        # Raises an Exception when there are to few values within the value variable
        with self.assertRaises(Exception):
            testBtree._Btree__generatePartition("Rena Rouge", "Illusion")

    def test_toString(self):
        testBtree = Btree({
            "Cat Noir" : ["Destruction", "Time"],
            "Ladybug" : ["Creation", "Multiplication"],
            "Rena Rouge" : ["Illusion", "Creation" ]
        })
        stringList = []
        testBtree._Btree__toString(testBtree._Btree__root, stringList)
        assert len(stringList) == 3
        assert stringList[0].__contains__("Cat Noir")
        assert stringList[0].__contains__("Destruction")
        assert stringList[0].__contains__("Time")

        assert stringList[1].__contains__("Ladybug")
        assert stringList[1].__contains__("Creation")
        assert stringList[1].__contains__("Multiplication")

    def test_reverseInternalIterator(self):
        testBtree = Btree({
            "Cat Noir" : ["Destruction", "Time"],
            "Ladybug" : ["Creation", "Multiplication"],
            "Rena Rouge" : ["Illusion", "Creation" ]
        })

        testBtree.getReverse()

    def test_toArray(self):
        testBtree = Btree({
            "Cat Noir" : ["Destruction", "Time"],
            "Ladybug" : ["Creation", "Multiplication"],
            "Rena Rouge" : ["Illusion", "Creation" ]
        })

        count = 0
        for key, values in testBtree.items():
            if(count == 0):
                assert key == "Cat Noir"
                assert values[0]== "Destruction"
                assert values[1] == "Time"
            elif(count == 1):
                assert key == "Ladybug"
                assert values[0] == "Creation"
                assert values[1] == "Multiplication"
            elif(count == 2):
                assert key == "Rena Rouge"
                assert values[0] == "Illusion"
                assert values[1] == "Creation"
            count = count + 1

        # Check that we went through all test cases    
        assert count == 3

    def test_externalIterator(self):
        testBtree = Btree({
            "Cat Noir" : ["Destruction", "Time"],
            "Ladybug" : ["Creation", "Multiplication"],
            "Rena Rouge" : ["Illusion", "Creation" ]
        })

        # Iterate through BTree and expect items in order
        count = 0
        for item in testBtree:
            if(count == 0):
                assert item == "Cat Noir"
            elif(count == 1):
                assert item == "Ladybug"
            elif(count == 2):
                assert item == "Rena Rouge"
            count = count + 1

        # Check that we went through all test cases    
        assert count == 3

    def test_setItem(self):
        """
        Testing BTree's implementation of the mutableMappings 
        __setitem__
        """
        # testBtree = Btree()
        # # Creates new root node if one does not exist
        # testBtree._Btree__root.insert = MagicMock(return_value=3)
        # testBtree.__setitem__("key", "value")

        # testBtree._Btree__root.insert.assert_called_with("key", "value")
        # print("meh")

        # if not self.__root:
        #     # Currently no root node? Create one
        #     self.__root = BtreeNode(True)
        
        # partition = self.__generatePartition(key, value)
        # self.__root.insert(partition) # insertion begins at the top of the tree allow Btree Node to sort

        # if not self.__root.isRoot: # root might have changed
        #     self.__root = self.__root.parent

        # # Partition has been added keep track of the length 
        # self.__totalPartitions = self.__totalPartitions + 1
# endregion      


# region traversing tests
    # def test_insert_empty(self):
    #     """
    #     When the BTree is empty a root node is created and 
    #     populated with the given partition
    #     """
    #     testBtree = Btree()

    #     # Set up a partition to insert
    #     testKey = "Plagg"
    #     testValue = 11
    #     testPartition = Partition(testKey, testValue)
        
    #     # Call
    #     testBtree.insert(testPartition)

    #     # Assert
    #     assert testBtree._Btree__root != None
    #     assert testBtree._Btree__root.keyValuePairs[0].getKey() == testKey

    # def test_traverse_basic(self):
    #     testBtree = Btree()

    #     # Set up a partition to insert
    #     testKey = "Plagg"
    #     testValue = 11
    #     testPartition = Partition(testKey, testValue)
        
    #     # Call
    #     testBtree.insert(testPartition)
    #     myList = testBtree.traverse()
    #     assert myList == ["Plagg"]
    
    # def test_traverse_twoTierTree(self):
    #     # Set-up
    #     # Creating what should be the left child
    #     testBtree = Btree()

    #     leftKey = "Applejack"
    #     leftValue = 222
    #     leftPartition = Partition(leftKey, leftValue)

    #     # Creating what should be the middle node
    #     medianKey = "Rarity"
    #     medianValue = 111
    #     medianPartition = Partition(medianKey, medianValue)

    #     # Creating what should be the right child
    #     rightKey = "Yuna"
    #     rightValue = 333
    #     rightPartition = Partition(rightKey, rightValue)

    #     # Call
    #     testBtree.insert(leftPartition)
    #     testBtree.insert(medianPartition)
    #     testBtree.insert(rightPartition)
    #     testListOfKeys = testBtree.traverse() 
    #     assert testListOfKeys == [leftKey, medianKey, rightKey]


    # def test_traverse_thirdNodeAppearance(self):
    #     testBtree = Btree()
    #     testBtree.insert(Partition("Effy", 2))
    #     testBtree.insert(Partition("Bernie", 1))
    #     testBtree.insert(Partition("Twili", 3))
    #     testBtree.insert(Partition("Usui", 4))
    #     testBtree.insert(Partition("Zecora", 5))
    #     testBtree.insert(Partition("Catnoir", 45))

    #     testListOfKeys = testBtree.traverse()

    #     assert testListOfKeys == ["Bernie", "Catnoir", "Effy", "Twili", "Usui", "Zecora"]
# endregion







