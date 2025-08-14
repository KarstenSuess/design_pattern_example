import unittest
from textwrap import dedent
from lxml import etree as LET

from design_pattern.models.callas_soap import ExtExecuteRequestBuilder


class CallasSOAPBuilder(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_request(self):
        req_xml = (
            ExtExecuteRequestBuilder()
            .with_user(None)  # leeres userID-Feld
            .add_args(
                "--noprogress",
                "--nosummary",
                "--nohits",
                "--outputfolder=/mnt/ingest/output",
                "/mnt/ingest/ausbildungsstellenmarkt-mit-zkt-035-0-202401-xlsx_Deckblatt.pdf",
            )
            .build_xml()
        )

        expected_xml = dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:ns="http://callassoftware.com/cws.xsd">
              <SOAP-ENV:Body>
                <ns:extExecute>
                  <args>
                    <userID></userID>
                    <args>--noprogress</args>
                    <args>--nosummary</args>
                    <args>--nohits</args>
                    <args>--outputfolder=/mnt/ingest/output</args>
                    <args>/mnt/ingest/ausbildungsstellenmarkt-mit-zkt-035-0-202401-xlsx_Deckblatt.pdf</args>
                  </args>
                </ns:extExecute>
              </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>
        """).encode("utf-8")

        got = LET.fromstring(req_xml.encode("utf-8"))
        exp = LET.fromstring(expected_xml)

        self.assertEqual(
            LET.tostring(got, method="c14n"),
            LET.tostring(exp, method="c14n"),
        )



if __name__ == '__main__':
    unittest.main()
