import sys

import pytest


def pytest_sessionstart(session: pytest.Session) -> None:
    if sys.version_info < (3, 12):
        version = f"{sys.version_info.major}.{sys.version_info.minor}"
        pytest.exit(
            f"The test suite requires Python 3.12 or newer; found Python {version}.",
            returncode=1,
        )
