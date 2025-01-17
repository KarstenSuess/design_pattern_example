import os
import unittest

from design_pattern.identify.borg_identifier import BorgIdentifier
from tests import TESTDATA_PATH


class Test_BorgIdentifier(unittest.TestCase):
    def setUp(self):
        pass

    def testIdentifyBorg(self):
        test_file_path = os.path.join(TESTDATA_PATH, 'droid_results.csv')

        identifier: BorgIdentifier = BorgIdentifier(base_url="http://blha-dimagapps-borg")
        res: dict[str, str] = identifier.identify(test_file_path)
        print(res)
        puid = (res['summary']['puid'])


        assert (puid == "x-fmt/18")
