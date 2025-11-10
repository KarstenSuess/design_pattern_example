import os
import unittest

from design_pattern.identify import IngestListIdentifier, IngestListIdentifierConfig
from tests import TESTDATA_PATH


class Test_ILWrapperIdentifier(unittest.TestCase):
    def test_upload_file(self):
        test_file_path = os.path.join(TESTDATA_PATH, '06842ea9-032b-4c2d-b88b-23c848812260_Aussonderung.Bewertungsverzeichnis.0502.xlsx')

        config : IngestListIdentifierConfig =  IngestListIdentifierConfig (
            base_url="http://blha-dimagapps-ilwrapper",
            username="appuser",
            password="",
            proxies=None
        )

        identifier: IngestListIdentifier = IngestListIdentifier(config)


if __name__ == '__main__':
    unittest.main()
