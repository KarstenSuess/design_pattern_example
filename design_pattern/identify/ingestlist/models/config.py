from dataclasses import dataclass


@dataclass
class IngestListIdentifierConfig:
    proxies: str | None = None
    base_url: str | None = None
    username: str | None = None
    password: str | None = None