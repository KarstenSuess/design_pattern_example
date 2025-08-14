from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from .payloads import ExtExecuteArgsPayload, ExtExecuteResultPayload
from .envelope import SoapEnvelope

__all__ = ["ExtExecuteRequestBuilder"]

@dataclass
class ExtExecuteRequestBuilder:
    _user_id: str | None = None
    _args: List[str] = field(default_factory=list)

    def with_user(self, user_id: str | None) -> "ExtExecuteRequestBuilder":
        self._user_id = user_id
        return self

    def add_arg(self, arg: str) -> "ExtExecuteRequestBuilder":
        self._args.append(arg)
        return self

    def add_args(self, *args: str) -> "ExtExecuteRequestBuilder":
        self._args.extend(args)
        return self

    def build_payload(self) -> ExtExecuteArgsPayload:
        if not self._args:
            raise ValueError("args darf nicht leer sein.")
        return ExtExecuteArgsPayload(user_id=self._user_id, args=list(self._args))

    def build_envelope(self) -> SoapEnvelope[ExtExecuteResultPayload]:
        return SoapEnvelope(header_xml=None, payload=self.build_payload())

    def build_xml(self, pretty: bool = True) -> str:
        env = self.build_envelope()
        return env.to_xml(pretty=pretty)
