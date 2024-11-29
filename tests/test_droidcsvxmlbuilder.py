import csv
import os
import unittest

from design_pattern.xmlformats import DroidCsvXmlBuilder
from tests import TESTDATA_PATH


class TestXmlBuilder(unittest.TestCase):
    __CSV_FNAME = os.path.join(TESTDATA_PATH, 'droid_results.csv')
    __RESULT_FNAME = os.path.join(TESTDATA_PATH, 'droid_results.xml')

    def setUp(self):
        pass

    def testXmlBuilderCreation(self):
        # creat an object and the csv_fname is read by processing the constructor
        xml_builder = DroidCsvXmlBuilder(self.__CSV_FNAME, self.__RESULT_FNAME)
        xml_builder.build()
        print(xml_builder.get_data())

    def testXmlBuilderXmlFile(self):
        # creat an object and the csv_fname is read by processing the constructor
        xml_builder = DroidCsvXmlBuilder(self.__CSV_FNAME, self.__RESULT_FNAME)
        xml_builder.build()
