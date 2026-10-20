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
    BitCodecInfo,
    BitCompressionLevel,
    BitCompressionMethod,
    BitException,
    BitFileCompressor,
    BitFileExtractor,
    BitFormatInfo,
    BitGenericItem,
    BitInFormat,
    BitInOutFormat,
    BitInputArchive,
    BitInputItem,
    BitMemCompressor,
    BitMemExtractor,
    BitOutputArchive,
    BitProperty,
    BitPropVariant,
    BitPropVariantType,
    BitStringCompressor,
    BitStringExtractor,
    DeletePolicy,
    EncryptionScope,
    FilterPolicy,
    FormatAPM,
    FormatArj,
    FormatAuto,
    FormatBZip2,
    FormatCab,
    FormatChm,
    FormatCOFF,
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
    FormatGPT,
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
    FormatVDI,
    FormatVhd,
    FormatVhdx,
    FormatVMDK,
    FormatWim,
    FormatXar,
    FormatXz,
    FormatZ,
    FormatZip,
    OverwriteMode,
    SymlinkPolicy,
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
    "BitCodecInfo",
    "BitCompressionLevel",
    "BitCompressionMethod",
    "BitException",
    "BitFileCompressor",
    "BitFileExtractor",
    "BitFormatInfo",
    "BitGenericItem",
    "BitInFormat",
    "BitInOutFormat",
    "BitInputArchive",
    "BitInputItem",
    "BitMemCompressor",
    "BitMemExtractor",
    "BitOutputArchive",
    "BitPropVariant",
    "BitPropVariantType",
    "BitProperty",
    "BitStringCompressor",
    "BitStringExtractor",
    "DeletePolicy",
    "EncryptionScope",
    "FilterPolicy",
    "FormatAPM",
    "FormatArj",
    "FormatAuto",
    "FormatBZip2",
    "FormatCOFF",
    "FormatCab",
    "FormatChm",
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
    "FormatGPT",
    "FormatGZip",
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
    "FormatVDI",
    "FormatVMDK",
    "FormatVhd",
    "FormatVhdx",
    "FormatWim",
    "FormatXar",
    "FormatXz",
    "FormatZ",
    "FormatZip",
    "OverwriteMode",
    "SymlinkPolicy",
    "UpdateMode",
    "__version__",
    "default_lib7zip",
    "default_plugin_dir",
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


def default_plugin_dir() -> str:
    """
    Get the default directory containing the external Codecs/ and Formats/
    plugin subdirectories under the package directory.

    Returns:
        The default plugin directory path.
    """
    return str(distribution(__package__).locate_file(__package__))


@contextmanager
def lib7zip_context(
    path: str = "",
    large_page_mode: bool = True,
) -> Generator[Bit7zLibrary, Any, None]:
    """
    A context manager to create a Bit7zLibrary instance.

    Args:
        path: The path to the lib7zip library. If not provided, the library will be searched in the package directory.
        large_page_mode: Whether to enable large page mode.

    Yields:
        A Bit7zLibrary instance.

    Raises:
        FileNotFoundError: If the lib7zip library is not found.
    """
    lib_path = path if len(path) != 0 else default_lib7zip()

    if pathlib.Path(lib_path).exists():
        lib7zip = Bit7zLibrary(lib_path)
        if large_page_mode:
            lib7zip.use_large_pages()
        yield lib7zip
    else:
        raise FileNotFoundError("lib7zip not found at " + lib_path)
