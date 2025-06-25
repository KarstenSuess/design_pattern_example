import os
import unittest

from design_pattern.identify import ILWrapperIdentifier
from tests import TESTDATA_PATH


class Test_ILWrapperIdentifier(unittest.TestCase):
    def test_upload_file(self):
        test_file_path = os.path.join(TESTDATA_PATH, 'droid_results.csv')

        identifier: ILWrapperIdentifier = ILWrapperIdentifier(base_url="http://ilapiwrapper.apps.kubecluster.blha.mwfk.ad.lvnbb.de/")
        res: dict[str, str] = identifier.identify(test_file_path)
        print(res)


if __name__ == '__main__':
    unittest.main()
