import json
from dataclasses import dataclass
from enum import Enum

from design_pattern.models.abstract_identifier import AbstractIdentifier
from design_pattern.utils import RemoteSession


@dataclass
class ILWrapperConfig:
    proxies: str | None = None
    base_url: str | None = None
    username: str | None = None
    password: str | None = None

class ILWrapperJobtype(Enum):
    LOCAL = 1
    REMOTE = 2


class ILWrapper(AbstractIdentifier):
    def __init__(self, cfg: ILWrapperConfig):
        self.__base_url = cfg.base_url
        self.__proxies = cfg.proxies
        self.__username = cfg.username
        self.__password = cfg.password

        self.token: str | None = None
        self.__login()

    def __login(self):
        with RemoteSession(base_url=self.__base_url) as s:
            payload = {
                'username': self.__username,
                'password': self.__password
            }

            header = {
                'Content-Type': 'application/json',
            }

            resp = s.post("/api/login", proxies=self.__proxies, headers=header, data=json.dumps(payload))

            if resp.status_code == 200 and resp.content:
                self.token = json.loads(resp.text)['token']
            else:
                raise Exception(f'{resp.status_code}: {resp.content}')

    def __identify(self, file_path: str, job_type: ILWrapperJobtype = ILWrapperJobtype.LOCAL):
        with RemoteSession(base_url=self.__base_url) as s:

            header = {
                'Content-Type': 'multipart/form-data',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + self.token,
            }

            match job_type:
                # Remote means we want to upload a file and identify it.
                case ILWrapperJobtype.LOCAL:
                    with open(file_path, 'rb') as f:
                        data = f.read()

                        payload = {
                            'file': (file_path, data, "multipart/form-data"),
                            'Type': 'Identify'
                        }

                        resp = s.post('/api/create',
                                      proxies=self.__proxies,
                                      headers=header,
                                      files=payload)

                        if resp.status_code == 200 and resp.content:
                            self.__response = json.loads(resp.content)
                        else:
                            raise Exception(f'{resp.status_code}: {resp.content}')
                case ILWrapperJobtype.REMOTE:
                    # local means we want to identify a file that is already on the server.
                    payload = {
                        'filename': file_path,
                        'Type': 'Identify'
                    }

                    resp = s.post('/api/create',
                                  proxies=self.__proxies,
                                  headers=header,
                                  data=json.dumps(payload))

                    if resp.status_code == 200 and resp.content:
                        self.__response = json.loads(resp.content)
                    else:
                        raise Exception(f'{resp.status_code}: {resp.content}')

    def __validate(self, file_path: str, job_type: ILWrapperJobtype = ILWrapperJobtype.LOCAL):
        with RemoteSession(base_url=self.__base_url) as s:

            header = {
                'Content-Type': 'multipart/form-data',
                'Accept': 'application/json',
                'Authorization': 'Bearer ' + self.token,
            }

            match job_type:
                # Remote means we want to upload a file and identify it.
                case ILWrapperJobtype.LOCAL:
                    with open(file_path, 'rb') as f:
                        data = f.read()

                        payload = {
                            'file': (file_path, data, "multipart/form-data"),
                            'Type': 'Validate'
                        }

                        resp = s.post('/api/create',
                                      proxies=self.__proxies,
                                      headers=header,
                                      files=payload)

                        if resp.status_code == 200 and resp.content:
                            self.__response = json.loads(resp.content)
                        else:
                            raise Exception(f'{resp.status_code}: {resp.content}')
                case ILWrapperJobtype.REMOTE:
                    # local means we want to identify a file that is already on the server.
                    payload = {
                        'filename': file_path,
                        'Type': 'Validate'
                    }

                    resp = s.post('/api/create',
                                  proxies=self.__proxies,
                                  headers=header,
                                  data=json.dumps(payload))

                    if resp.status_code == 200 and resp.content:
                        self.__response = json.loads(resp.content)
                    else:
                        raise Exception(f'{resp.status_code}: {resp.content}')

    def identify(self, file_path: str, job_type: ILWrapperJobtype = ILWrapperJobtype.LOCAL):

        if self.__base_url and file_path:
            if self.token is None:
                self.__login()

            self.__identify(file_path, job_type)

    def validate(self, file_path: str, job_type: ILWrapperJobtype = ILWrapperJobtype.LOCAL):

        if self.__base_url and file_path:
            if self.token is None:
                self.__login()

            self.__validate(file_path, job_type)