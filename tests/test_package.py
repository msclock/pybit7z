from __future__ import annotations

from importlib_metadata import version

import pybit7z as m


def test_version():
    assert version("pybit7z") == m.__version__
