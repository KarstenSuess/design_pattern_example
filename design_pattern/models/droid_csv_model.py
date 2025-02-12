from dataclasses import dataclass, asdict
from design_pattern.utils.cast import Cast


@dataclass
class DroidCsvModel:
    id: str = None
    parent_id: str = None
    uri: str = None
    file_path: str = None
    name: str = None
    method: str = None
    status: str = None
    size: str = None
    type: str = None
    ext: str = None
    last_modified: str = None
    extension_mismatch: str = None
    hash: str = None
    format_count: str = None
    puid: str = None
    mime_type: str = None
    format_name: str = None
    format_version: str = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, dto: dict) -> 'DroidCsvModel':
        return Cast(dto, cls)
