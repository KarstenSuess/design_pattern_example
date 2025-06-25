from dataclasses import asdict, field, dataclass
from typing import Dict

from design_pattern.utils import Cast


@dataclass
class ILWrapperFileUploadResponse:
    filePath: Dict[str, str] = field(default_factory=dict)
    duration: int = field(default_factory=int)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, dto: dict) -> 'ILWrapperFileUploadResponse':
        return Cast(dto, cls)