from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.test_cleanup import cleanup_database_after_tests, initialize_test_baseline


BASELINE_KEYS: dict[str, set] = {}


@pytest.fixture(scope="session", autouse=True)
def _prepare_database():
    global BASELINE_KEYS
    BASELINE_KEYS = initialize_test_baseline()

    yield

    cleanup_database_after_tests(BASELINE_KEYS)


@pytest.fixture(autouse=True)
def _cleanup_test_data_after_each_test():
    yield
    cleanup_database_after_tests(BASELINE_KEYS)
