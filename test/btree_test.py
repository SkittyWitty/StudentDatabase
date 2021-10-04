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
        stringList = testBtree._Btree__toString()
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

        reverseList = testBtree.getReverse()
        # Cat Noir is expected to be last in the list
        assert reverseList[2].__contains__("Cat Noir")
        assert reverseList[2].__contains__("Destruction")
        assert reverseList[2].__contains__("Time")

        # Rena Rouge is expected to be first in the list
        assert reverseList[0].__contains__("Rena Rouge")
        assert reverseList[0].__contains__("Illusion")
        assert reverseList[0].__contains__("Creation")


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
# endregion      


