import os
import time
import unittest

from design_pattern.identify import IngestListIdentifier, IngestListIdentifierConfig, IngestListJobType, \
    IngestListTaskResponse, IngestListTaskState
from design_pattern.xmlformats import parse_il_results
from tests import TESTDATA_PATH


class Test_ILWrapperIdentifier(unittest.TestCase):
    def test_upload_file(self):
        test_file_path = os.path.join(TESTDATA_PATH,
                                      '06842ea9-032b-4c2d-b88b-23c848812260_Aussonderung.Bewertungsverzeichnis.0502.xlsx')

        config: IngestListIdentifierConfig = IngestListIdentifierConfig(
            base_url="http://blha-dimagapps-ilwrapper",
            username="apiuser",
            password="",
            proxies=None
        )

        identifier: IngestListIdentifier = IngestListIdentifier(config)
        IngestListTask : IngestListTaskResponse = identifier.identify(test_file_path, IngestListJobType.LOCAL)

        while IngestListTask.status != IngestListTaskState.Completed:
            time.sleep(20)
            IngestListTask = identifier.check_task_status(IngestListTask.id)

        result = parse_il_results (IngestListTask.output)
        for d in result.datei_liste.dateien:
            print(f'MD5: {d.stats.md5}')
            if d.droid.result.puid:
                print(f'PUID: {d.droid.result.puid}')

if __name__ == '__main__':
    unittest.main()
