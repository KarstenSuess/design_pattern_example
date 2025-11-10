from dataclasses import dataclass, asdict, field
from design_pattern.utils import Cast


@dataclass
class IngestListResponse:
    id: int = field(default=0)
    filename: str = field(default='')
    status:  str = field(default='')
    type:  str = field(default='')
    started_at:  str = field(default='')
    completed_at: str = field(default='')
    output: str = field(default='')
    error: str = field(default='')
    created_at: str = field(default='')
    updated_at: str = field(default='')

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, dto: dict) -> 'IngestListCreateResponse':
        return Cast(dto, cls)