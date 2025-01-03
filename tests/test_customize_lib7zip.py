from __future__ import annotations

import pytest

import pybit7z


def test_custom_dummy():
    dummy = "/path/to/custom/lib7zip.so"
    with pytest.raises(
        FileNotFoundError,
        match=f"lib7zip not found at {dummy}",
    ), pybit7z.lib7zip_context(dummy):
        pass


def test_invalid_path():
    with pytest.raises(
        pybit7z.BitException,
        match="Failed to load the 7-zip library: ",
    ), pybit7z.lib7zip_context(__file__):
        pass


def test_custom_lib7zip():
    with pybit7z.lib7zip_context(pybit7z.default_lib7zip()):
        pass
