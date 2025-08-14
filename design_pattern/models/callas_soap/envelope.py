from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Type, TypeVar, Optional, Union
from lxml import etree as LET
import xml.etree.ElementTree as ET

T = TypeVar("T")

SOAP_NS = "http://schemas.xmlsoap.org/soap/envelope/"

NSMAP = {
    "SOAP-ENV": "http://schemas.xmlsoap.org/soap/envelope/",
    "SOAP-ENC": "http://schemas.xmlsoap.org/soap/encoding/",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "ns": "http://callassoftware.com/cws.xsd",
}

NS = {
    "soap": SOAP_NS,
    "ns": "http://callassoftware.com/cws.xsd",  # anpassen, falls abweichend
}

@dataclass
class SoapFault(Exception):
    code: str
    message: str
    detail_xml: Optional[str] = None

    def __str__(self) -> str:
        base = f"SOAP Fault: {self.code} - {self.message}"
        return f"{base}\n{self.detail_xml}" if self.detail_xml else base

@dataclass
class SoapEnvelope(Generic[T]):
    payload: Optional[T]
    header_xml: Optional[str] = None

    def to_xml(self, pretty: bool = False) -> str:
        env = LET.Element(f"{{{NSMAP['SOAP-ENV']}}}Envelope", nsmap=NSMAP)
        body = LET.SubElement(env, f"{{{NSMAP['SOAP-ENV']}}}Body")

        et_elem: ET.Element = self.payload.to_element()
        lxml_payload = LET.fromstring(ET.tostring(et_elem, encoding="utf-8"))

        # userID erzwingen als <userID></userID>
        for uid in lxml_payload.xpath(".//userID"):
            if uid.text is None:
                uid.text = ""  # verhindert Selbstschließung

        body.append(lxml_payload)

        xml_bytes = LET.tostring(
            env, pretty_print=pretty,
            xml_declaration=True, encoding="UTF-8"
        )
        xml = xml_bytes.decode("utf-8")

        # optional: XML-Deklaration mit doppelten Anführungszeichen normieren
        # (semantisch egal; nur falls deine Gegenstelle das exakt so erwartet)
        if xml.startswith("<?xml version='1.0'"):
            xml = xml.replace("version='1.0'", 'version="1.0"', 1)
            xml = xml.replace("encoding='UTF-8'", 'encoding="UTF-8"', 1)

        return xml

    @classmethod
    def from_xml(cls, data: Union[str, bytes], payload_cls: Type[T]) -> "SoapEnvelope[T]":
        parser = LET.XMLParser(recover=False, huge_tree=True)
        root = LET.fromstring(data if isinstance(data, (bytes, bytearray)) else data.encode("utf-8"), parser=parser)

        # Fault prüfen
        fault = root.find(".//soap:Fault", namespaces=NS)
        if fault is not None:
            code = (fault.findtext("faultcode") or "").strip()
            msg = (fault.findtext("faultstring") or "").strip()
            detail_el = fault.find("detail")
            detail_xml = LET.tostring(detail_el, encoding="unicode") if detail_el is not None else None
            raise SoapFault(code=code, message=msg, detail_xml=detail_xml)

        # Header optional
        header_el = root.find("./soap:Header", namespaces=NS)
        header_xml = LET.tostring(header_el, encoding="unicode") if header_el is not None else None

        # Body und erstes Element darin finden
        body = root.find("./soap:Body", namespaces=NS)
        if body is None:
            raise ValueError("SOAP Body fehlt")

        # erstes echte Element im Body (Response-Element)
        payload_el = next((el for el in body if isinstance(el.tag, str)), None)
        if payload_el is None:
            return cls(header_xml=header_xml, payload=None)

        # Payload bauen – erfordert eine Fabrik: from_xml_element oder ähnliches
        if hasattr(payload_cls, "from_xml_element"):
            payload = payload_cls.from_xml_element(payload_el)  # type: ignore[attr-defined]
        elif hasattr(payload_cls, "from_xml"):
            # Falls dein Payload direkte XML-Strings erwartet
            payload = payload_cls.from_xml(LET.tostring(payload_el, encoding="utf-8"))  # type: ignore[attr-defined]
        else:
            # Minimal: rohes XML in das Payload-Modell stopfen, wenn es ein init(xml=...) hat
            try:
                payload = payload_cls(xml=LET.tostring(payload_el, encoding="unicode"))  # type: ignore[call-arg]
            except Exception as e:
                raise TypeError(
                    f"{payload_cls.__name__} braucht eine Fabrikmethode wie from_xml_element(self, el) "
                    "oder ein __init__(xml=...)."
                ) from e

        return cls(header_xml=header_xml, payload=payload)
