import os
import unittest

from design_pattern.identify import ILWrapperIdentifier
from design_pattern.models.ilwrapper_data_model import ILWrapperParser, ILWrapperFileIdentifyResponse
from tests import TESTDATA_PATH

class TestParseILResponse(unittest.TestCase):
    def test_parser_onfile(self):
        with open(os.path.join(TESTDATA_PATH, 'il_results.txt'), 'r') as f:
            raw = f.read()
            p : ILWrapperParser = ILWrapperParser()
            res = p.parse(raw)
            # Test the first toolname
            assert (res['Tools'][0].toolName == "Droid")
            # Test puid
            assert (res['Tools'][0].toolAttributes['pronom-puid'] == 'fmt/18')
            # Test J-Hove's toolname
            assert (res['Tools'][3].toolName == "Jhove")
            # Test puid
            assert (res['Tools'][3].toolAttributes['jhove-mime'] == 'application/pdf')

    def test_parser_onidentifier(self):
        test_file_path = os.path.join(TESTDATA_PATH, '25.KW_.-Speiseplan-Kantine-Golm.pdf')

        identifier: ILWrapperIdentifier = ILWrapperIdentifier(base_url="http://ilapiwrapper.apps.kubecluster.blha.mwfk.ad.lvnbb.de/")
        i_res: ILWrapperFileIdentifyResponse = identifier.identify(test_file_path)
        p : ILWrapperParser = ILWrapperParser()
        p_res = p.parse(i_res.result)

        # Test the first toolname
        assert (p_res['Tools'][0].toolName == "Droid")
        # Test puid
        assert (p_res['Tools'][0].toolAttributes['pronom-puid'] == 'fmt/18')
        # Test J-Hove's toolname
        assert (p_res['Tools'][3].toolName == "Jhove")
        # Test puid
        assert (p_res['Tools'][3].toolAttributes['jhove-mime'] == 'application/pdf')


if __name__ == '__main__':
    unittest.main()
