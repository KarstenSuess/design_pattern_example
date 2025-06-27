import os
import unittest

from design_pattern.identify import ILWrapperIdentifier
from design_pattern.models.ilwrapper_data_model import ILWrapperFileIdentifyResponse
from tests import TESTDATA_PATH


class Test_ILWrapperIdentifier(unittest.TestCase):
    def test_upload_file(self):
        test_file_path = os.path.join(TESTDATA_PATH, '25.KW_.-Speiseplan-Kantine-Golm.pdf')

        identifier: ILWrapperIdentifier = ILWrapperIdentifier(base_url="http://ilapiwrapper.apps.kubecluster.blha.mwfk.ad.lvnbb.de/")
        res: ILWrapperFileIdentifyResponse = identifier.identify(test_file_path)
        print(res.result)


if __name__ == '__main__':
    unittest.main()
