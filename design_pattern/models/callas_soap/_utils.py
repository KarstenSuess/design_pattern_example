from __future__ import annotations
import xml.etree.ElementTree as ET
from datetime import timedelta

# "Private" Modul-Helfer: nicht nach außen exportieren
NS = {
    "SOAP-ENV": "http://schemas.xmlsoap.org/soap/envelope/",
    "SOAP-ENC": "http://schemas.xmlsoap.org/soap/encoding/",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "ns": "http://callassoftware.com/cws.xsd",
}

for p, u in NS.items():
    ET.register_namespace(p, u)

def _qn(prefix: str, local: str) -> str:
    return f"{{{NS[prefix]}}}{local}"

def _text(node: ET.Element | None) -> str:
    return (node.text or "") if node is not None else ""

def _parse_console_out(console_out: str) -> dict[str, str | list[str]]:
    result: dict[str, str | list[str]] = {}
    for raw in console_out.splitlines():
        line = raw.strip()
        if not line:
            continue
        parts = [p for p in line.split("\t") if p != ""]
        if not parts:
            continue
        key, *vals = parts
        value = vals[0] if vals else ""
        if key in result:
            cur = result[key]
            result[key] = (cur + [value]) if isinstance(cur, list) else [cur, value]
        else:
            result[key] = value
    return result

def _parse_hhmmss_like(s: str) -> timedelta | None:
    if not s:
        return None
    try:
        parts = [int(p) for p in s.strip().split(":")]
    except ValueError:
        return None
    if len(parts) == 2:
        mm, ss = parts
        return timedelta(minutes=mm, seconds=ss)
    if len(parts) == 3:
        hh, mm, ss = parts
        return timedelta(hours=hh, minutes=mm, seconds=ss)
    return None
