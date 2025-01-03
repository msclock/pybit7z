"""
Copyright (c) 2024 l.feng. All rights reserved.

pybit7z: A wrapper based on bit7z.
"""

from __future__ import annotations

import pathlib
from contextlib import contextmanager
from typing import Any, Generator

from importlib_metadata import distribution

from pybit7z._core import (
    Bit7zLibrary,
    BitAbstractArchiveCreator,
    BitAbstractArchiveHandler,
    BitAbstractArchiveOpener,
    BitArchiveEditor,
    BitArchiveItem,
    BitArchiveItemInfo,
    BitArchiveItemOffset,
    BitArchiveReader,
    BitArchiveWriter,
    BitCompressionLevel,
    BitCompressionMethod,
    BitException,
    BitFileCompressor,
    BitFileExtractor,
    BitGenericItem,
    BitInFormat,
    BitInOutFormat,
    BitInputArchive,
    BitMemCompressor,
    BitMemExtractor,
    BitOutputArchive,
    BitProperty,
    BitPropVariant,
    BitPropVariantType,
    BitStringCompressor,
    BitStringExtractor,
    DeletePolicy,
    FilterPolicy,
    FormatAPM,
    FormatArj,
    FormatAuto,
    FormatBZip2,
    FormatCab,
    FormatChm,
    FormatCoff,
    FormatCompound,
    FormatCpio,
    FormatCramFS,
    FormatDeb,
    FormatDmg,
    FormatElf,
    FormatExt,
    FormatFat,
    FormatFeatures,
    FormatFlv,
    FormatGpt,
    FormatGZip,
    FormatHfs,
    FormatHxs,
    FormatIHex,
    FormatIso,
    FormatLzh,
    FormatLzma,
    FormatLzma86,
    FormatMacho,
    FormatMbr,
    FormatMslz,
    FormatMub,
    FormatNsis,
    FormatNtfs,
    FormatPe,
    FormatPpmd,
    FormatQcow,
    FormatRar,
    FormatRar5,
    FormatRpm,
    FormatSevenZip,
    FormatSplit,
    FormatSquashFS,
    FormatSwf,
    FormatSwfc,
    FormatTar,
    FormatTE,
    FormatUdf,
    FormatUEFIc,
    FormatUEFIs,
    FormatVdi,
    FormatVhd,
    FormatVhdx,
    FormatVmdk,
    FormatWim,
    FormatXar,
    FormatXz,
    FormatZ,
    FormatZip,
    OverwriteMode,
    UpdateMode,
    platform_lib7zip_name,
)

from ._version import version as __version__

__all__ = [
    "Bit7zLibrary",
    "BitAbstractArchiveCreator",
    "BitAbstractArchiveHandler",
    "BitAbstractArchiveOpener",
    "BitArchiveEditor",
    "BitArchiveItem",
    "BitArchiveItemInfo",
    "BitArchiveItemOffset",
    "BitArchiveReader",
    "BitArchiveWriter",
    "BitCompressionLevel",
    "BitCompressionMethod",
    "BitException",
    "BitFileCompressor",
    "BitFileExtractor",
    "BitGenericItem",
    "BitInFormat",
    "BitInOutFormat",
    "BitInputArchive",
    "BitMemCompressor",
    "BitMemExtractor",
    "BitOutputArchive",
    "BitPropVariant",
    "BitPropVariantType",
    "BitProperty",
    "BitStringCompressor",
    "BitStringExtractor",
    "DeletePolicy",
    "FilterPolicy",
    "FormatAPM",
    "FormatArj",
    "FormatAuto",
    "FormatBZip2",
    "FormatCab",
    "FormatChm",
    "FormatCoff",
    "FormatCompound",
    "FormatCpio",
    "FormatCramFS",
    "FormatDeb",
    "FormatDmg",
    "FormatElf",
    "FormatExt",
    "FormatFat",
    "FormatFeatures",
    "FormatFlv",
    "FormatGZip",
    "FormatGpt",
    "FormatHfs",
    "FormatHxs",
    "FormatIHex",
    "FormatIso",
    "FormatLzh",
    "FormatLzma",
    "FormatLzma86",
    "FormatMacho",
    "FormatMbr",
    "FormatMslz",
    "FormatMub",
    "FormatNsis",
    "FormatNtfs",
    "FormatPe",
    "FormatPpmd",
    "FormatQcow",
    "FormatRar",
    "FormatRar5",
    "FormatRpm",
    "FormatSevenZip",
    "FormatSplit",
    "FormatSquashFS",
    "FormatSwf",
    "FormatSwfc",
    "FormatTE",
    "FormatTar",
    "FormatUEFIc",
    "FormatUEFIs",
    "FormatUdf",
    "FormatVdi",
    "FormatVhd",
    "FormatVhdx",
    "FormatVmdk",
    "FormatWim",
    "FormatXar",
    "FormatXz",
    "FormatZ",
    "FormatZip",
    "OverwriteMode",
    "UpdateMode",
    "__version__",
    "default_lib7zip",
    "lib7zip_context",
]


def default_lib7zip() -> str:
    """
    Get the default lib7zip library path under the package directory.

    Returns:
        The default lib7zip library path.
    """
    return str(
        distribution(__package__).locate_file(__package__) / platform_lib7zip_name()
    )


@contextmanager
def lib7zip_context(
    path: str = "", larg_page_mode: bool = True
) -> Generator[Bit7zLibrary, Any, None]:
    """
    A context manager to create a Bit7zLibrary instance.

    Args:
        path: The path to the lib7zip library. If not provided, the library will be searched in the package directory.
        larg_page_mode: Whether to enable large page mode.

    Yields:
        A Bit7zLibrary instance.

    Raises:
        FileNotFoundError: If the lib7zip library is not found.
    """
    lib_path = path if len(path) != 0 else default_lib7zip()

    if pathlib.Path(lib_path).exists():
        lib7zip = Bit7zLibrary(lib_path)
        if larg_page_mode:
            lib7zip.set_large_page_mode()
        yield lib7zip
    else:
        raise FileNotFoundError("lib7zip not found at " + lib_path)
