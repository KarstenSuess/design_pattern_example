import asyncio

from design_pattern.identify import IngestListTaskState
from design_pattern.identify.ingestlist import IngestListIdentifierConfig, IngestListJobType
from design_pattern.identify.ingestlist.models import IngestListTaskResponse
from design_pattern.models.abstract_identifier import AbstractIdentifier
from design_pattern.utils import RemoteSessionAsync

class IngestListIdentifierAsync(AbstractIdentifier):
  def __init__(self, cfg: IngestListIdentifierConfig):
    self.__base_url = cfg.base_url
    self.__proxies = cfg.proxies
    self.__username = cfg.username
    self.__password = cfg.password

    self.token: str | None = None

    # Polling Konfiguration
    self.poll_interval: float = 2.0  # Sekunden zwischen Status-Checks
    self.max_poll_time: float = 300.0  # Max 5 Minuten warten

  async def __aenter__(self):
    await self.__login()
    return self

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    pass

  async def initialize(self):
    await self.__login()
    return self

  async def __login(self):
    async with RemoteSessionAsync(base_url=self.__base_url) as s:
      payload = {
        'email': self.__username,
        'password': self.__password
      }

      header = {
        'Content-Type': 'application/json',
      }

      resp = await s.post(
        "/api/login",
        proxies=self.__proxies,
        headers=header,
        json=payload
      )

      if resp.status_code == 200 and resp.content:
        self.token = resp.json()['token']
      else:
        raise Exception(f'{resp.status_code}: {resp.content}')

  def __header(self) -> dict[str, str]:
    return {
      'Accept': 'application/json',
      'Authorization': 'Bearer ' + self.token,
    }

  async def __identify(self, file_path: str, job_type: IngestListJobType = IngestListJobType.LOCAL):
    async with RemoteSessionAsync(base_url=self.__base_url) as s:
      match job_type:
        case IngestListJobType.LOCAL:
          with open(file_path, 'rb') as f:
            data = f.read()

            files = {
              'file': (file_path, data, "multipart/form-data")
            }

            payload = {
              'type': 'Identify'
            }

            resp = await s.post(
              '/api/create',
              proxies=self.__proxies,
              headers=self.__header(),
              files=files,
              data=payload
            )

            if 200 <= resp.status_code < 400 and resp.content:
              self.__response = resp.json()
            else:
              raise Exception(f'{resp.status_code}: {resp.content}')

        case IngestListJobType.REMOTE:
          payload = {
            'filename': file_path,
            'type': 'Identify'
          }

          resp = await s.post(
            '/api/create',
            proxies=self.__proxies,
            headers=self.__header(),
            json=payload
          )

          if 200 <= resp.status_code < 400 and resp.content:
            self.__response = resp.json()
          else:
            raise Exception(f'{resp.status_code}: {resp.content}')

  async def __validate(self, file_path: str, job_type: IngestListJobType = IngestListJobType.LOCAL):
    async with RemoteSessionAsync(base_url=self.__base_url) as s:
      match job_type:
        case IngestListJobType.LOCAL:
          with open(file_path, 'rb') as f:
            data = f.read()

            files = {
              'file': (file_path, data, "multipart/form-data")
            }

            payload = {
              'type': 'Validate'
            }

            resp = await s.post(
              '/api/create',
              proxies=self.__proxies,
              headers=self.__header(),
              files=files,
              data=payload
            )

            if 200 <= resp.status_code < 400 and resp.content:
              self.__response = resp.json()
            else:
              raise Exception(f'{resp.status_code}: {resp.content}')

        case IngestListJobType.REMOTE:
          payload = {
            'filename': file_path,
            'type': 'Validate'
          }

          resp = await s.post(
            '/api/create',
            proxies=self.__proxies,
            headers=self.__header(),
            json=payload
          )

          if 200 <= resp.status_code < 400 and resp.content:
            self.__response = resp.json()
          else:
            raise Exception(f'{resp.status_code}: {resp.content}')

  async def __check_task_status(self, job_id: str):
    async with RemoteSessionAsync(base_url=self.__base_url) as s:
      resp = await s.get(
        f'api/job/{job_id}',
        proxies=self.__proxies,
        headers=self.__header()
      )

      if 200 <= resp.status_code < 400 and resp.content:
        self.__response = resp.json()
      else:
        raise Exception(f'{resp.status_code}: {resp.content}')

  async def __wait_for_completion(self, job_id: str) -> IngestListTaskResponse:
    """
    Wartet bis der Task abgeschlossen ist (Status = Completed oder Failed)
    """
    start_time = asyncio.get_event_loop().time()

    while True:
      await self.__check_task_status(job_id)

      try:
        response = IngestListTaskResponse.from_dict(self.__response)
        status = getattr(response, 'status', None)

        if status == IngestListTaskState.Completed:
          return response
        elif status == IngestListTaskState.Failed:
          raise Exception(f'Task {job_id} failed: {response}')

        # Timeout Check
        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed > self.max_poll_time:
          raise TimeoutError(f'Task {job_id} did not complete within {self.max_poll_time}s')

        # Warte vor nächstem Check
        await asyncio.sleep(self.poll_interval)

      except Exception as e:
        raise Exception(f'Error checking task status: {e}')

  async def identify(
      self,
      file_path: str,
      job_type: IngestListJobType = IngestListJobType.LOCAL,
      wait_for_completion: bool = True
  ) -> IngestListTaskResponse | None:
    """
    Startet einen Identify-Task

    Args:
        file_path: Pfad zur Datei
        job_type: LOCAL oder REMOTE
        wait_for_completion: Wenn True, wartet bis Task fertig ist
    """
    if self.__base_url and file_path:
      if self.token is None:
        await self.__login()

      await self.__identify(file_path, job_type)

      try:
        initial_response = IngestListTaskResponse.from_dict(self.__response)

        if not wait_for_completion:
          return initial_response

        # Hole Job-ID (anpassen je nach deinem Model)
        job_id = getattr(initial_response, 'job_id', None) or getattr(initial_response, 'id', None)

        if not job_id:
          raise Exception('No job_id in response')

        # Warte auf Completion
        return await self.__wait_for_completion(job_id)

      except Exception as e:
        raise Exception(f'Error in identify: {e}')
    return None

  async def validate(
      self,
      file_path: str,
      job_type: IngestListJobType = IngestListJobType.LOCAL,
      wait_for_completion: bool = True
  ) -> IngestListTaskResponse | None:
    if self.__base_url and file_path:
      if self.token is None:
        await self.__login()

      await self.__validate(file_path, job_type)

      try:
        initial_response = IngestListTaskResponse.from_dict(self.__response)

        if not wait_for_completion:
          return initial_response

        job_id = getattr(initial_response, 'job_id', None) or getattr(initial_response, 'id', None)

        if not job_id:
          raise Exception('No job_id in response')

        return await self.__wait_for_completion(job_id)

      except Exception:
        return None
    return None

  async def check_task_status(self, job_id: str) -> IngestListTaskResponse | None:
    if self.__base_url and job_id:
      if self.token is None:
        await self.__login()

      await self.__check_task_status(job_id)
      try:
        return IngestListTaskResponse.from_dict(self.__response)
      except Exception:
        return None
    return None
