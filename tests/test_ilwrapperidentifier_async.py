import asyncio

import unittest

from design_pattern.identify import IngestListIdentifierConfig, IngestListIdentifierAsync, IngestListTaskState

from tests import TESTDATA_PATH


class TestILWrapperIdentifierAsync(unittest.TestCase):

  def configure(self) -> IngestListIdentifierConfig:
    return IngestListIdentifierConfig(
      base_url="http://blha-dimagapps-ilwrapper",
      username="apiuser",
      password="",
      proxies=None
    )

  async def blocking_behaviour(self):
    async def main():
      cfg = IngestListIdentifierConfig(...)

      async with IngestListIdentifierAsync(cfg) as identifier:
        # Wartet bis alle Tasks COMPLETED sind
        results = await asyncio.gather(
          identifier.identify("file1.txt"),  # wartet auf Completion
          identifier.identify("file2.txt"),  # wartet auf Completion
          identifier.identify("file3.txt"),  # wartet auf Completion
        )

        for result in results:
          print(f"Status: {result.status}")
          print(f"Result: {result}")

  async def test_nonblocking_gathering_later(self):
    async with IngestListIdentifierAsync(self.configure()) as identifier:
      # Tasks nur starten (wait_for_completion=False)
      pending_tasks = await asyncio.gather(
        identifier.identify("file1.txt", wait_for_completion=False),
        identifier.identify("file2.txt", wait_for_completion=False),
        identifier.identify("file3.txt", wait_for_completion=False),
      )

      # Job-IDs sammeln
      job_ids = [task.job_id for task in pending_tasks]

      # Manuell auf Completion warten
      while True:
        statuses = await asyncio.gather(
          *[identifier.check_task_status(job_id) for job_id in job_ids]
        )

        if all(s.status == IngestListTaskState.Completed for s in statuses):
          print("All tasks completed!")
          for status in statuses:
            print(status)
          break

        await asyncio.sleep(2)

  async def test_nonblocking_with_progress(self):
    async with IngestListIdentifierAsync(self.configure()) as identifier:
      files = ["file1.txt",
               "file2.txt",
               "file3.txt"]

      # Tasks parallel starten
      tasks = [
        identifier.identify(file, wait_for_completion=False)
        for file in files
      ]
      pending = await asyncio.gather(*tasks)

      job_ids = [p.job_id for p in pending]
      completed = set()

      while len(completed) < len(job_ids):
        for job_id in job_ids:
          if job_id not in completed:
            status = await identifier.check_task_status(job_id)
            if status.status == 'Completed':
              completed.add(job_id)
              print(f"✓ Task {job_id} completed ({len(completed)}/{len(job_ids)})")

        await asyncio.sleep(2)

      print("All done!")


if __name__ == '__main__':
  unittest.main()
