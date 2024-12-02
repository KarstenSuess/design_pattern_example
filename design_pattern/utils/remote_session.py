import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import urllib.parse


class RemoteSession(requests.Session):

    def __init__(self, base_url: str):
        super().__init__()

        self._base_url = base_url
        retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[502, 503, 504]
                        )

        self.mount(self._base_url, HTTPAdapter(max_retries=retries))

    def post(self, url, data=None, json=None, **kwargs) -> Response:
        url = urllib.parse.urljoin(self._base_url, url)
        return super().post(url, data=data, json=json, **kwargs)

    def get(self, url, **kwargs):
        url = urllib.parse.urljoin(self._base_url, url)
        return super().get(url, **kwargs)
