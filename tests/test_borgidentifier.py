import os
import unittest

from design_pattern.identify.borg_identifier import BorgIdentifier
from design_pattern.models import DroidCsvModel
from tests import TESTDATA_PATH

class Test_BorgIdentifier(unittest.TestCase):
    def setUp(self):
        pass

    def testIdentifyBorg(self):
        test_file_path = os.path.join(TESTDATA_PATH, 'droid_results.csv')

        identifier : BorgIdentifier = BorgIdentifier(base_url="http://blha-container-registry:8090")
        res : dict[str, str] = identifier.identify(test_file_path)

        puid = (res['summary']['puid']['values'][0]['value'])

        assert (puid == "x-fmt/18")

