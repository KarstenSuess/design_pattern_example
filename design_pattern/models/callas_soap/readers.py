from __future__ import annotations
from dataclasses import dataclass
import xml.etree.ElementTree as ET
from .payloads import ExtExecuteResultPayload
from .envelope import SoapEnvelope

__all__ = ["ExtExecuteResultReader"]

@dataclass
class ExtExecuteResultReader:
    _payload: ExtExecuteResultPayload

    @classmethod
    def from_xml(cls, xml: str | bytes | ET.Element) -> "ExtExecuteResultReader":
        env = SoapEnvelope.from_xml(xml, ExtExecuteResultPayload)
        return cls(_payload=env.payload)

    # Exponierte Properties (Forwarding)
    @property
    def payload(self) -> ExtExecuteResultPayload:
        return self._payload

    @property
    def success(self) -> bool:
        return self._payload.success

    @property
    def return_code(self) -> int:
        return self._payload.return_code

    @property
    def console_map(self):
        return self._payload.console_map

    @property
    def process_id(self):
        return self._payload.process_id

    @property
    def pages(self):
        return self._payload.pages

    @property
    def input_path(self):
        return self._payload.input_path

    @property
    def output_path(self):
        return self._payload.output_path

    @property
    def pdfa(self):
        return self._payload.pdfa

    @property
    def duration(self):
        return self._payload.duration
