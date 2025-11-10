import httpx
import urllib.parse
import asyncio
from httpx import Response


class RemoteSessionAsync(httpx.AsyncClient):

  def __init__(
      self,
      base_url: str,
      max_retries: int = 5,
      backoff_factor: float = 0.5,
      status_forcelist: list[int] = None
  ):
    super().__init__(
      base_url=base_url,
      timeout=httpx.Timeout(10.0)
    )
    self._max_retries = max_retries
    self._backoff_factor = backoff_factor
    self._status_forcelist = status_forcelist or [502, 503, 504]

  async def _request_with_retries(self, method: str, url: str, **kwargs) -> Response:
    url = urllib.parse.urljoin(str(self.base_url), url)

    for attempt in range(self._max_retries + 1):
      try:
        response = await self.request(method, url, **kwargs)

        if response.status_code not in self._status_forcelist:
          return response

        if attempt < self._max_retries:
          wait_time = self._backoff_factor * (2 ** attempt)
          await asyncio.sleep(wait_time)
        else:
          return response

      except (httpx.ConnectError, httpx.TimeoutException) as e:
        if attempt < self._max_retries:
          wait_time = self._backoff_factor * (2 ** attempt)
          await asyncio.sleep(wait_time)
        else:
          raise

    return response

  async def post(self, url, data=None, json=None, **kwargs) -> Response:
    return await self._request_with_retries("POST", url, data=data, json=json, **kwargs)

  async def get(self, url, **kwargs) -> Response:
    return await self._request_with_retries("GET", url, **kwargs)


# Verwendung:
async def main():
  async with RemoteSessionAsync("https://api.example.com") as session:
    response = await session.get("/endpoint")
    print(response.json())
