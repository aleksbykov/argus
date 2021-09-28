from random import choice

from argus.db.testrun import TestResourcesSetup, TestRun, TestRunInfo
from argus.db.interface import ArgusDatabase
from argus.db.config import Config

from argus.db.db_types import ColumnInfo
from uuid import uuid4

import pytest
import logging

LOGGER = logging.getLogger(__name__)


@pytest.mark.docker_required
def test_serialize_deserialize(completed_testrun: TestRunInfo, argus_database: ArgusDatabase):
    test_id = uuid4()
    test_run = TestRun(test_id=test_id, group="longevity-test", release_name="4_5rc5", assignee="k0machi",
                       run_info=completed_testrun)

    test_run.save()

    res = argus_database.fetch(table_name=f"test_runs", run_id=test_id)
    LOGGER.debug("Fetched: %s", res)
    LOGGER.info("Rebuilding object...")

    rebuilt_test_run = TestRun.from_db_row(res)

    assert rebuilt_test_run.serialize() == test_run.serialize()


@pytest.mark.docker_required
def test_recreate_from_id(completed_testrun: TestRunInfo, argus_database: ArgusDatabase):
    test_id = uuid4()
    test_run = TestRun(test_id=test_id, group="longevity-test", release_name="4_5rc5", assignee="k0machi",
                       run_info=completed_testrun)

    test_run.save()

    rebuilt_test_run = TestRun.from_id(test_id)

    assert rebuilt_test_run.serialize() == test_run.serialize()


@pytest.mark.docker_required
def test_update(completed_testrun: TestRunInfo, argus_database: ArgusDatabase):
    test_id = uuid4()
    test_run = TestRun(test_id=test_id, group="longevity-test", release_name="4_5rc5", assignee="k0machi",
                       run_info=completed_testrun)
    test_run.save()

    resource = choice(test_run.resources.leftover_resources)
    test_run.resources.detach_resource(resource)
    test_run.save()

    row = argus_database.fetch(table_name=f"test_runs", run_id=test_id)

    rebuilt_testrun = TestRun.from_db_row(row)

    assert test_run.serialize() == rebuilt_testrun.serialize()
