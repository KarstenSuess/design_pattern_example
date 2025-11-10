import json
from dataclasses import dataclass
from enum import Enum

from design_pattern.models.abstract_identifier import AbstractIdentifier
from design_pattern.utils import RemoteSession


@dataclass
class IngestListIdentifierConfig:
    proxies: str | None = None
    base_url: str | None = None
    username: str | None = None
    password: str | None = None


class IngestListJobType(Enum):
    LOCAL = 1
    REMOTE = 2


class IngestListIdentifier(AbstractIdentifier):
    def __init__(self, cfg: IngestListIdentifierConfig):
        self.__base_url = cfg.base_url
        self.__proxies = cfg.proxies
        self.__username = cfg.username
        self.__password = cfg.password

        self.token: str | None = None
        self.__login()

    def __login(self):
        with RemoteSession(base_url=self.__base_url) as s:
            payload = {
                'email': self.__username,
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

    def __header(self) -> dict[str, str]:
        return {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.token,
        }

    def __identify(self, file_path: str, job_type: IngestListJobType = IngestListJobType.LOCAL):
        with RemoteSession(base_url=self.__base_url) as s:
            match job_type:
                # Remote means we want to upload a file and identify it.
                case IngestListJobType.LOCAL:

                    with open(file_path, 'rb') as f:
                        data = f.read()

                        files = {
                            'file': (file_path, data, "multipart/form-data")
                        }

                        payload = {
                            'type': 'Identify'
                        }

                        resp = s.post('/api/create',
                                      proxies=self.__proxies,
                                      headers=self.__header(),
                                      files=files,
                                      data=payload)

                        if 200 <= resp.status_code < 400 and resp.content:
                            self.__response = json.loads(resp.content)
                        else:
                            raise Exception(f'{resp.status_code}: {resp.content}')
                case IngestListJobType.REMOTE:

                    # local means we want to identify a file that is already on the server.
                    payload = {
                        'filename': file_path,
                        'type': 'Identify'
                    }

                    resp = s.post('/api/create',
                                  proxies=self.__proxies,
                                  headers=self.__header(),
                                  data=json.dumps(payload))

                    if 200 <= resp.status_code < 400 and resp.content:
                        self.__response = json.loads(resp.content)
                    else:
                        raise Exception(f'{resp.status_code}: {resp.content}')

    def __validate(self, file_path: str, job_type: IngestListJobType = IngestListJobType.LOCAL):
        with RemoteSession(base_url=self.__base_url) as s:
            match job_type:
                # Remote means we want to upload a file and identify it.
                case IngestListJobType.LOCAL:
                    with open(file_path, 'rb') as f:
                        data = f.read()

                        files = {
                            'file': (file_path, data, "multipart/form-data")
                        }

                        payload = {
                            'type': 'Validate'
                        }

                        resp = s.post('/api/create',
                                      proxies=self.__proxies,
                                      headers=self.__header(),
                                      files=files,
                                      data=payload)

                        if 200 <= resp.status_code < 400 and resp.content:
                            self.__response = json.loads(resp.content)
                        else:
                            raise Exception(f'{resp.status_code}: {resp.content}')
                case IngestListJobType.REMOTE:
                    # local means we want to identify a file that is already on the server.
                    payload = {
                        'filename': file_path,
                        'type': 'Validate'
                    }

                    resp = s.post('/api/create',
                                  proxies=self.__proxies,
                                  headers=self.__header(),
                                  data=json.dumps(payload))

                    if 200 <= resp.status_code < 400 and resp.content:
                        self.__response = json.loads(resp.content)
                    else:
                        raise Exception(f'{resp.status_code}: {resp.content}')

    def identify(self, file_path: str, job_type: IngestListJobType = IngestListJobType.LOCAL) -> dict[str]:

        if self.__base_url and file_path:
            if self.token is None:
                self.__login()

            self.__identify(file_path, job_type)
            return self.__response

    def validate(self, file_path: str, job_type: IngestListJobType = IngestListJobType.LOCAL) -> dict[str]:

        if self.__base_url and file_path:
            if self.token is None:
                self.__login()

            self.__validate(file_path, job_type)
            return self.__response
