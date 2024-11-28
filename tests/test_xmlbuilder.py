import csv
import os
import unittest

from design_pattern.xml import XmlBuilder
from tests import TESTDATA_PATH

class TestXmlBuilder(unittest.TestCase):
    def setUp(self):
        pass

    def testXmlBuilderCreation(self):
        csv_fname = os.path.join(TESTDATA_PATH, 'droid_results.csv')
        # creat an object and the csv_fname is read by processing the constructor
        xml_builder = XmlBuilder(csv_fname, 'dummy.xml')
        xml_builder.build()
        print (xml_builder.get_data())

    def testXmlBuilderXmlFile(self):
        csv_fname = os.path.join(TESTDATA_PATH, 'droid_results.csv')
        # creat an object and the csv_fname is read by processing the constructor
        xml_builder = XmlBuilder(csv_fname, 'dummy.xml')
        xml_builder.build()