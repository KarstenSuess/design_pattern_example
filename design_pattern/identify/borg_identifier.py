import json
from typing import Optional

from design_pattern.models.abstract_identifier import AbstractIdentifier
from design_pattern.utils.remote_session import RemoteSession


class BorgIdentifier(AbstractIdentifier):
    def __init__(self, base_url : str, proxies: Optional[str] = None):
        self.__base_url = base_url
        self.__response = None
        self.__proxies = proxies

    def __indentify(self, file_name : str):
        with RemoteSession(base_url=self.__base_url) as s:

            header = {
                'Content-Type': 'multipart/form-data',
                'Accept': 'application/json'
            }

            data = None
            with open(file_name, 'rb') as f:
                data = f.read()

                payload = {
                    'file':(file_name, data, "multipart/form-data")
                }

                resp = s.post('/api/analyze-file', proxies=self.__proxies, files=payload)
                if resp.status_code == 200 and resp.content:
                    self.__response = json.loads(resp.content)
                else:
                    raise Exception(f'{resp.status_code}: {resp.content}')

    def identify(self, file_name: str = None) -> dict[str]:
        if self.__base_url and file_name:
            self.__indentify(file_name)

        return self.__response