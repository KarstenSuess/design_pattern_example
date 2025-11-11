import asyncio
import os
import time

import pytest

from design_pattern.identify import IngestListIdentifierConfig, IngestListIdentifierAsync, IngestListTaskState, \
    IngestListJobType
from design_pattern.xmlformats import parse_il_results, IdentifyResult
from tests import TESTDATA_PATH


@pytest.fixture
def config() -> IngestListIdentifierConfig:
    return IngestListIdentifierConfig(
        base_url="http://blha-dimagapps-ilwrapper",
        username="apiuser",
        password="",
        proxies=None
    )


@pytest.mark.asyncio
async def test_blocking_behaviour(config):
    file_1 = os.path.join(TESTDATA_PATH,
                          '06842ea9-032b-4c2d-b88b-23c848812260_Aussonderung.Bewertungsverzeichnis.0502.xlsx')
    file_2 = os.path.join(TESTDATA_PATH,
                          '25.KW_.-Speiseplan-Kantine-Golm.pdf')
    file_3 = os.path.join(TESTDATA_PATH,
                          'droid_results.xml')

    async with IngestListIdentifierAsync(config) as identifier:
        results = await asyncio.gather(
            identifier.identify(file_path=file_1, job_type=IngestListJobType.LOCAL),
            identifier.identify(file_path=file_2, job_type=IngestListJobType.LOCAL),
            identifier.identify(file_path=file_3, job_type=IngestListJobType.LOCAL),
        )

        for result in results:
            print(f"Status: {result.status}")
            print(f"Result: {result}")
            assert result.status == IngestListTaskState.Completed


@pytest.mark.asyncio
async def test_nonblocking_gathering_later(config):
    file_1 = os.path.join(TESTDATA_PATH,
                          '06842ea9-032b-4c2d-b88b-23c848812260_Aussonderung.Bewertungsverzeichnis.0502.xlsx')
    file_2 = os.path.join(TESTDATA_PATH,
                          '25.KW_.-Speiseplan-Kantine-Golm.pdf')
    file_3 = os.path.join(TESTDATA_PATH,
                          'droid_results.xml')

    async with IngestListIdentifierAsync(config) as identifier:
        pending_tasks = await asyncio.gather(
            identifier.identify(file_path=file_1, job_type=IngestListJobType.LOCAL, wait_for_completion=False),
            identifier.identify(file_path=file_2, job_type=IngestListJobType.LOCAL, wait_for_completion=False),
            identifier.identify(file_path=file_3, job_type=IngestListJobType.LOCAL, wait_for_completion=False),
        )

        job_ids = [task.id for task in pending_tasks]

        while True:
            statuses = await asyncio.gather(
                *[identifier.check_task_status(job_id) for job_id in job_ids]
            )

            if all(s.status == IngestListTaskState.Completed for s in statuses):
                print("All tasks completed!")
                for status in statuses:
                    print(status)
                    assert status.status == IngestListTaskState.Completed
                break

            await asyncio.sleep(10)


@pytest.mark.asyncio
async def test_nonblocking_with_progress(config):
    async with IngestListIdentifierAsync(config) as identifier:
        file_1 = os.path.join(TESTDATA_PATH,
                              '06842ea9-032b-4c2d-b88b-23c848812260_Aussonderung.Bewertungsverzeichnis.0502.xlsx')
        file_2 = os.path.join(TESTDATA_PATH,
                              '25.KW_.-Speiseplan-Kantine-Golm.pdf')
        file_3 = os.path.join(TESTDATA_PATH,
                              'droid_results.xml')

        files = [file_1, file_2, file_3, file_1, file_2, file_3, file_1, file_2, file_3, file_1]

        tasks = [
            identifier.identify(file_path=file, job_type=IngestListJobType.LOCAL, wait_for_completion=False)
            for file in files
        ]

        pending = await asyncio.gather(*tasks)

        jobs = {p.id: p for p in pending}
        completed = {}
        failed = {}
        print(f"🚀 Started {len(jobs)} tasks")

        start_time = time.time()
        while len(completed) + len(failed) < len(jobs):
            for job_id in jobs:
                if job_id not in completed and job_id not in failed:
                    status = await identifier.check_task_status(job_id)

                if status.status == IngestListTaskState.Completed:
                    completed[job_id] = status
                    print(f"✓ [{len(completed)+len(failed)}/{len(jobs)}] Task {job_id} completed")

                elif status.status == IngestListTaskState.Failed:
                    failed[job_id] = status
                    print(f"❌ [{len(completed)+len(failed)}/{len(jobs)}] Task {job_id} failed: {status.error}")

            if len(completed) + len(failed) < len(jobs):
                await asyncio.sleep(10)

        elapsed = time.time() - start_time
        print(f"\n✅ Completed: {len(completed)}")
        print(f"❌ Failed: {len(failed)}")
        print(f"⏱️  Time: {elapsed:.1f}s")
        assert len(completed) == len(jobs)

        for job_id, result in completed.items():
            res : IdentifyResult = parse_il_results( result.output )
            print(f"ID: {job_id}")
            print(f"File: {result.filename}")
            for d in res.datei_liste.dateien:
                print(f'MD5: {d.stats.md5}')
                if d.droid.result.puid:
                    print(f'PUID: {d.droid.result.puid}')
            print(f"Duration: {result.completed_at}")
