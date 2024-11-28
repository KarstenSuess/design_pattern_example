import csv
import os
import unittest

from design_pattern.models import DroidCsvModel
from tests import TESTDATA_PATH

class TestReadCSVFile(unittest.TestCase):
    def setUp(self):
        pass

    def testReadCSVFile(self):
        csv_fname = os.path.join(TESTDATA_PATH, 'droid_results.csv')
        with open(csv_fname, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mod =  DroidCsvModel.from_dict(row)
                print(mod)