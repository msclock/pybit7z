from __future__ import annotations

import random
import string
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Fixture to provide temporary directory"""
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)
    except Exception:
        ...  # Ignore errors from cleanup


@pytest.fixture
def large_file(tmp_path):
    """Fixture to create a large test file (10MB)"""
    file_path: Path = tmp_path / "large_file.dat"
    size_mb = 10
    chunk_size = 1024 * 1024  # 1MB chunks

    with file_path.open("wb") as f:
        for _ in range(size_mb):
            data = "".join(
                random.choices(string.ascii_letters + string.digits, k=chunk_size)
            ).encode()
            f.write(data)

    return file_path
