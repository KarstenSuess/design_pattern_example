from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from lxml import etree as LET
import xml.etree.ElementTree as ET
from ._utils import _qn, _text, _parse_console_out, _parse_hhmmss_like

__all__ = ["ExtExecuteArgsPayload", "ExtExecuteResultPayload"]

NSMAP = {
    "SOAP-ENV": "http://schemas.xmlsoap.org/soap/envelope/",
    "SOAP-ENC": "http://schemas.xmlsoap.org/soap/encoding/",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "ns": "http://callassoftware.com/cws.xsd",
}

@dataclass
class ExtExecuteArgsPayload:
    user_id: str | None = None
    args: List[str] = field(default_factory=list)

    def to_element(self) -> ET.Element:
        root = ET.Element(_qn("ns", "extExecute"))
        args_el = ET.SubElement(root, "args")

        uid = ET.SubElement(args_el, "userID")
        # wichtig: leerer String, nicht None -> verhindert <userID/>
        uid.text = "" if self.user_id in (None, "") else str(self.user_id)

        for a in self.args:
            arg_el = ET.SubElement(args_el, "args")
            arg_el.text = a

        return root


    @staticmethod
    def expected_tag() -> str:
        return _qn("ns", "extExecute")

@dataclass
class ExtExecuteResultPayload:
    console_out: Optional[str] = None
    return_code: Optional[int] = None

    @classmethod
    def from_xml_element(cls, el: LET._Element) -> "ExtExecuteResultPayload":
        # el entspricht <ns:extExecuteResult>
        # consoleOut und returnCode können unqualifiziert oder im ns-NS stehen.
        # Wir versuchen erst ns:-qualifiziert, dann unqualifiziert.
        console_el = el.find("ns:consoleOut", namespaces=NSMAP) or el.find("consoleOut")
        rc_el = el.find("ns:returnCode", namespaces=NSMAP) or el.find("returnCode")

        console_text = console_el.text if console_el is not None else None
        if console_text is not None:
            # &#xA; ist bereits als '\n' decodiert; optional trimmen
            console_text = console_text.strip("\n")

        rc: Optional[int] = None
        if rc_el is not None and rc_el.text is not None:
            try:
                rc = int(rc_el.text.strip())
            except ValueError:
                rc = None

        return cls(console_out=console_text, return_code=rc)
