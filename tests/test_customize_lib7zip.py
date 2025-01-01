from __future__ import annotations

import importlib
import os
import sys

import pytest


@pytest.fixture(autouse=True)
def clean_import_cache():
    for module in list(sys.modules.keys()):
        if module.startswith("pybit7z"):
            del sys.modules[module]


def test_custom_dummy():
    os.environ["PYBIT7Z_LIB7ZIP_PATH"] = "/path/to/custom/lib7zip.so"
    with pytest.raises(
        FileNotFoundError,
        match=f"lib7zip not found at {os.environ['PYBIT7Z_LIB7ZIP_PATH']}",
    ):
        import pybit7z
