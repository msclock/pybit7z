"""
Copyright (c) 2024 l.feng. All rights reserved.

pybit7z: A wrapper based on bit7z.
"""

from __future__ import annotations

import os

from importlib_metadata import distribution

from ._version import version as __version__

__all__ = ["__version__"]

os.environ["__PYBIT7Z_LIB7ZIP_PATH__"] = str(
    distribution(__package__).locate_file(__package__)
)
