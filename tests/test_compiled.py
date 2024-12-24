from __future__ import annotations

from pybit7z import _core


def test_core_version():
    assert _core.version() != ""
