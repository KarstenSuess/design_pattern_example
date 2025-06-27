from dataclasses import asdict, dataclass
from types import NoneType
from typing import Dict, List

from design_pattern.utils import Cast


@dataclass
class ILWrapperFileUploadResponse:
    filePath: str
    durationInMs: int

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, dto: dict) -> 'ILWrapperFileUploadResponse':
        return Cast(dto, cls)

@dataclass
class ILWrapperFileIdentifyResponse:
    result: str
    durationInMs: int

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, dto: dict) -> 'ILWrapperFileIdentifyResponse':
        return Cast(dto, cls)

@dataclass
class ILWrapperToolEntry:
    toolName: str = None
    toolAttributes: Dict[str, str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class ILWrapperParser:
    @staticmethod
    def parse(content : str) -> dict:
        lines = content.splitlines()
        retCode = lines[0].split(' ')[0]
        lines = lines[1:]
        result = { 'ILRetCode': retCode, "Tools": [] }
        ILTools : List[ILWrapperToolEntry] = []
        currentTool: ILWrapperToolEntry = None

        for line in lines:

            if line == "":
                continue

            fields = line.split('\t')

            if len(fields) == 1:
                if currentTool:
                    ILTools.append(currentTool)
                    currentTool = None

                if currentTool is None:
                    currentTool = ILWrapperToolEntry()

                if currentTool:
                    currentTool.toolName = fields[0].rstrip()

            if len(fields) == 3:
                if currentTool:
                    if currentTool.toolAttributes is None:
                        currentTool.toolAttributes = {}
                    currentTool.toolAttributes[fields[1].rstrip()] = fields[2].rstrip()

        result['Tools'] = ILTools
        return result






