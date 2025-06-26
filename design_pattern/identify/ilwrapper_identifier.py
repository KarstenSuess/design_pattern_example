import json
from typing import Optional

from design_pattern.models.abstract_identifier import AbstractIdentifier
from design_pattern.models.ilwrapper_data_model import ILWrapperFileUploadResponse, ILWrapperFileIdentifyResponse
from design_pattern.utils.remote_session import RemoteSession


class ILWrapperIdentifier(AbstractIdentifier):

    def __init__(self, base_url: str, proxies: Optional[str] = None):
        self.__base_url = base_url
        self.__filePath : str = None
        self.__proxies = proxies
        self.__response : ILWrapperFileIdentifyResponse = None

    def __upload_file(self, file_name: str):
        with (RemoteSession(base_url=self.__base_url) as s):

            header = {
                'Content-Type': 'multipart/form-data',
                'Accept': 'application/json'
            }

            data = None
            with open(file_name, 'rb') as f:
                data = f.read()

                payload = {
                    'file': (file_name, data, "multipart/form-data")
                }

                resp = s.post('/api/upload', proxies=self.__proxies, files=payload)
                if resp.status_code == 200:
                    if resp.content:
                        rd: ILWrapperFileUploadResponse = ILWrapperFileUploadResponse.from_dict(
                            json.loads(resp.content))
                        self.__filePath = rd.filePath

                else:
                    raise Exception(f'{resp.status_code}: {resp.content}')

    def __identify(self):
        with (RemoteSession(base_url=self.__base_url) as s):

            header = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            data = None

            payload = {
                'filePath': r"%s" % self.__filePath
            }

            resp = s.post('/api/identify', proxies=self.__proxies, headers=header, data=json.dumps(payload))
            if resp.content:
                self.__response = ILWrapperFileIdentifyResponse.from_dict(
                    json.loads(resp.content))

            if resp.status_code != 200:
                raise Exception(f'{resp.status_code}: {data['message']}')

    def identify(self, file_name: str = None) -> ILWrapperFileIdentifyResponse:
        if self.__base_url and file_name:
            self.__upload_file(file_name)

        if self.__filePath:
            self.__identify()
            return self.__response

        return ILWrapperFileIdentifyResponse