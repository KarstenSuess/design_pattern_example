import unittest

import requests

from design_pattern.models.callas_soap import ExtExecuteRequestBuilder, ExtExecuteResultReader, ExtExecuteResultPayload, \
    SoapEnvelope


class CallasSOAPRequest(unittest.TestCase):
    ENDPOINT_URL = 'http://10.175.97.121:1301'
    def setUp(self):
        pass

    def test_send_request(self):

        # neuen Builder für SOAPRequests erstellen
        builder : ExtExecuteRequestBuilder = (
            ExtExecuteRequestBuilder()
            .with_user(None)
            .add_args(
                "--noprogress",
                "--nosummary",
                "--nohits",
                "--outputfolder=/mnt/ingest/output",
                "/mnt/ingest/ausbildungsstellenmarkt-mit-zkt-035-0-202401-xlsx_Deckblatt.pdf"
            )
        )
        # request bauen
        soap_request: str = builder.build_xml(pretty=True)
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "",
        }

        resp = requests.post(self.ENDPOINT_URL, data=soap_request.encode("utf-8"), headers=headers, timeout=30)
        resp.raise_for_status()  # HTTP-Fehler werfen

        env = SoapEnvelope.from_xml(resp.content, ExtExecuteResultPayload)
        result: ExtExecuteResultPayload = env.payload  # type: ignore[assignment]
        print("Return code:", result.return_code)
        print("Console out:\n", result.console_out)

if __name__ == '__main__':
    unittest.main()
