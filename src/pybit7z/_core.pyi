"""

Python bindings for bit7z library
-----------------------
.. currentmodule:: _core

"""

from __future__ import annotations

import datetime
import typing

__all__ = [
    "CRC",
    "ATime",
    "AltStreamsSize",
    "Attrib",
    "BZip2",
    "BigEndian",
    "Bit64",
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
    "Block",
    "Bool",
    "CTime",
    "Characters",
    "Checksum",
    "ClusterSize",
    "CodePage",
    "Comment",
    "Commented",
    "Copy",
    "CopyLink",
    "Cpu",
    "CreatorApp",
    "Deflate",
    "Deflate64",
    "DeletePolicy",
    "DictionarySize",
    "EmbeddedStubSize",
    "Empty",
    "Encrypted",
    "Error",
    "ErrorFlags",
    "ErrorType",
    "Exclude",
    "Extension",
    "Fast",
    "Fastest",
    "FileSystem",
    "FileTime",
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
    "FreeSpace",
    "Group",
    "HandlerItemIndex",
    "HardLink",
    "HeadersSize",
    "HostOS",
    "INode",
    "Id",
    "Include",
    "Int8",
    "Int16",
    "Int32",
    "Int64",
    "IsAltStream",
    "IsAnti",
    "IsAux",
    "IsDeleted",
    "IsDir",
    "IsNotArcType",
    "IsTree",
    "IsVolume",
    "ItemOnly",
    "Links",
    "LocalName",
    "Lzma",
    "Lzma2",
    "MTime",
    "MainSubfile",
    "Max",
    "Method",
    "Name",
    "NoProperty",
    "None_",
    "Normal",
    "NtReparse",
    "NtSecure",
    "NumAltStreams",
    "NumBlocks",
    "NumErrors",
    "NumStreams",
    "NumSubDirs",
    "NumSubFiles",
    "NumVolumes",
    "Offset",
    "OutName",
    "Overwrite",
    "OverwriteMode",
    "PackSize",
    "Path",
    "PhySize",
    "PhySizeCantBeDetected",
    "Position",
    "PosixAttrib",
    "Ppmd",
    "Prefix",
    "Provider",
    "ReadOnly",
    "RecurseDirs",
    "SectorSize",
    "Sha1",
    "Sha256",
    "ShortComment",
    "ShortName",
    "Size",
    "Skip",
    "Solid",
    "SplitAfter",
    "SplitBefore",
    "StreamId",
    "String",
    "SubType",
    "SymLink",
    "TailSize",
    "TimeType",
    "TotalPhySize",
    "TotalSize",
    "Type",
    "UInt8",
    "UInt16",
    "UInt32",
    "UInt64",
    "Ultra",
    "UnpackSize",
    "UnpackVer",
    "UpdateMode",
    "User",
    "Va",
    "VirtualSize",
    "Volume",
    "VolumeIndex",
    "VolumeName",
    "Warning",
    "WarningFlags",
    "ZerosTailIsAllowed",
    "set_large_page_mode",
    "set_lib7zip_path",
    "version",
]

class BitAbstractArchiveCreator(BitAbstractArchiveHandler):
    def compression_format(self) -> BitInOutFormat: ...
    def compression_method(self) -> BitCompressionMethod: ...
    def crypt_headers(self) -> bool: ...
    def dictionary_size(self) -> int: ...
    def set_compression_level(self, arg0: BitCompressionLevel) -> None: ...
    def set_compression_method(self, arg0: BitCompressionMethod) -> None: ...
    def set_dictionary_size(self, arg0: int) -> None: ...
    @typing.overload
    def set_password(self, password: str) -> None: ...
    @typing.overload
    def set_password(self, password: str, crypt_headers: bool) -> None: ...
    def set_solid_mode(self, arg0: bool) -> None: ...
    def set_store_symbolic_links(self, arg0: bool) -> None: ...
    def set_threads_count(self, arg0: int) -> None: ...
    def set_update_mode(self, arg0: UpdateMode) -> None: ...
    def set_volume_size(self, arg0: int) -> None: ...
    def set_word_size(self, arg0: int) -> None: ...
    def solid_mode(self) -> bool: ...
    def store_symbolic_links(self) -> bool: ...
    def threads_count(self) -> int: ...
    def update_mode(self) -> UpdateMode: ...
    def volume_size(self) -> int: ...
    def word_size(self) -> int: ...

class BitAbstractArchiveHandler:
    def clear_password(self) -> None: ...
    def file_callback(self) -> typing.Callable[[str], None]: ...
    def format(self) -> BitInFormat: ...
    def is_password_defined(self) -> bool: ...
    def overwrite_mode(self) -> OverwriteMode: ...
    def password(self) -> str: ...
    def password_callback(self) -> typing.Callable[[], str]: ...
    def progress_callback(self) -> typing.Callable[[int], bool]: ...
    def ratio_callback(self) -> typing.Callable[[int, int], None]: ...
    def retainDirectories(self) -> bool: ...
    def set_file_callback(self, arg0: typing.Callable[[str], None]) -> None: ...
    def set_overwrite_mode(self, mode: OverwriteMode) -> None: ...
    def set_password(self, password: str) -> None: ...
    def set_password_callback(self, callback: typing.Callable[[], str]) -> None: ...
    def set_progress_callback(self, arg0: typing.Callable[[int], bool]) -> None: ...
    def set_ratio_callback(self, arg0: typing.Callable[[int, int], None]) -> None: ...
    def set_retain_directories(self, arg0: bool) -> None: ...
    def set_total_callback(self, arg0: typing.Callable[[int], None]) -> None: ...
    def total_callback(self) -> typing.Callable[[int], None]: ...

class BitAbstractArchiveOpener(BitAbstractArchiveHandler):
    def extraction_format(self) -> BitInFormat: ...

class BitArchiveEditor(BitArchiveWriter):
    def __init__(
        self, in_archive: str, format: BitInOutFormat, password: str = ""
    ) -> None: ...
    def apply_changes(self) -> None: ...
    @typing.overload
    def delete_item(self, index: int, policy: DeletePolicy) -> None: ...
    @typing.overload
    def delete_item(self, item_path: str, policy: DeletePolicy) -> None: ...
    @typing.overload
    def rename_item(self, index: int, new_path: str) -> None: ...
    @typing.overload
    def rename_item(self, old_path: str, new_path: str) -> None: ...
    def set_update_mode(self, update_mode: UpdateMode) -> None: ...
    @typing.overload
    def update_item(self, index: int, in_file: str) -> None: ...
    @typing.overload
    def update_item(self, index: int, in_buffer: bytes) -> None: ...
    @typing.overload
    def update_item(self, item_path: str, in_file: str) -> None: ...
    @typing.overload
    def update_item(self, item_path: str, in_buffer: bytes) -> None: ...

class BitArchiveItem(BitGenericItem):
    def attributes(self) -> int: ...
    def crc(self) -> int: ...
    def creation_time(self) -> datetime.datetime: ...
    def extension(self) -> str: ...
    def index(self) -> int: ...
    def is_encrypted(self) -> bool: ...
    def last_access_time(self) -> datetime.datetime: ...
    def last_write_time(self) -> datetime.datetime: ...
    def native_path(self) -> str: ...
    def pack_size(self) -> int: ...

class BitArchiveItemInfo(BitArchiveItem):
    def item_properties(self) -> dict[BitProperty, BitPropVariant]: ...
    def item_property(self, arg0: BitProperty) -> BitPropVariant: ...

class BitArchiveItemOffset(BitArchiveItem):
    def __iadd__(self, arg0: int) -> BitArchiveItemOffset: ...
    def item_property(self, arg0: BitProperty) -> BitPropVariant: ...

class BitArchiveReader(BitAbstractArchiveOpener, BitInputArchive):
    @staticmethod
    @typing.overload
    def is_header_encrypted(in_archive: str, format: BitInFormat) -> bool: ...
    @staticmethod
    @typing.overload
    def is_header_encrypted(in_archive: bytes, format: BitInFormat) -> bool: ...
    @typing.overload
    def __init__(
        self, in_archive: str, format: BitInFormat, password: str = ""
    ) -> None: ...
    @typing.overload
    def __init__(
        self, in_archive: bytes, format: BitInFormat, password: str = ""
    ) -> None: ...
    def archive_properties(self) -> dict[BitProperty, BitPropVariant]: ...
    def files_count(self) -> int: ...
    def folders_count(self) -> int: ...
    def has_encrypted_items(self) -> bool: ...
    def is_encrypted(self) -> bool: ...
    def is_multi_volume(self) -> bool: ...
    def is_solid(self) -> bool: ...
    def items(self) -> list[BitArchiveItemInfo]: ...
    def pack_size(self) -> int: ...
    def size(self) -> int: ...
    def volumes_count(self) -> int: ...

class BitArchiveWriter(BitAbstractArchiveCreator, BitOutputArchive):
    @typing.overload
    def __init__(self, format: BitInOutFormat) -> None: ...
    @typing.overload
    def __init__(
        self, in_archive: str, format: BitInOutFormat, password: str = ""
    ) -> None: ...
    @typing.overload
    def __init__(
        self, in_archive: bytes, format: BitInOutFormat, password: str = ""
    ) -> None: ...

class BitCompressionLevel:
    """
    Members:

      None_

      Fastest

      Fast

      Normal

      Max

      Ultra
    """

    Fast: typing.ClassVar[BitCompressionLevel]  # value = <BitCompressionLevel.Fast: 3>
    Fastest: typing.ClassVar[
        BitCompressionLevel
    ]  # value = <BitCompressionLevel.Fastest: 1>
    Max: typing.ClassVar[BitCompressionLevel]  # value = <BitCompressionLevel.Max: 7>
    None_: typing.ClassVar[
        BitCompressionLevel
    ]  # value = <BitCompressionLevel.None_: 0>
    Normal: typing.ClassVar[
        BitCompressionLevel
    ]  # value = <BitCompressionLevel.Normal: 5>
    Ultra: typing.ClassVar[
        BitCompressionLevel
    ]  # value = <BitCompressionLevel.Ultra: 9>
    __members__: typing.ClassVar[
        dict[str, BitCompressionLevel]
    ]  # value = {'None_': <BitCompressionLevel.None_: 0>, 'Fastest': <BitCompressionLevel.Fastest: 1>, 'Fast': <BitCompressionLevel.Fast: 3>, 'Normal': <BitCompressionLevel.Normal: 5>, 'Max': <BitCompressionLevel.Max: 7>, 'Ultra': <BitCompressionLevel.Ultra: 9>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class BitCompressionMethod:
    """
    Members:

      Copy

      Deflate

      Deflate64

      BZip2

      Lzma

      Lzma2

      Ppmd
    """

    BZip2: typing.ClassVar[
        BitCompressionMethod
    ]  # value = <BitCompressionMethod.BZip2: 3>
    Copy: typing.ClassVar[
        BitCompressionMethod
    ]  # value = <BitCompressionMethod.Copy: 0>
    Deflate: typing.ClassVar[
        BitCompressionMethod
    ]  # value = <BitCompressionMethod.Deflate: 1>
    Deflate64: typing.ClassVar[
        BitCompressionMethod
    ]  # value = <BitCompressionMethod.Deflate64: 2>
    Lzma: typing.ClassVar[
        BitCompressionMethod
    ]  # value = <BitCompressionMethod.Lzma: 4>
    Lzma2: typing.ClassVar[
        BitCompressionMethod
    ]  # value = <BitCompressionMethod.Lzma2: 5>
    Ppmd: typing.ClassVar[
        BitCompressionMethod
    ]  # value = <BitCompressionMethod.Ppmd: 6>
    __members__: typing.ClassVar[
        dict[str, BitCompressionMethod]
    ]  # value = {'Copy': <BitCompressionMethod.Copy: 0>, 'Deflate': <BitCompressionMethod.Deflate: 1>, 'Deflate64': <BitCompressionMethod.Deflate64: 2>, 'BZip2': <BitCompressionMethod.BZip2: 3>, 'Lzma': <BitCompressionMethod.Lzma: 4>, 'Lzma2': <BitCompressionMethod.Lzma2: 5>, 'Ppmd': <BitCompressionMethod.Ppmd: 6>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class BitException(Exception):
    pass

class BitFileCompressor(BitStringCompressor):
    def __init__(self, format: BitInOutFormat) -> None: ...
    @typing.overload
    def compress(self, in_files: list[str], out_archive: str) -> None: ...
    @typing.overload
    def compress(self, in_files: dict[str, str], out_archive: str) -> None: ...
    def compress_directory(self, in_dir: str, out_archive: str) -> None: ...
    def compress_directory_contents(
        self,
        in_dir: str,
        out_archive: str,
        recursive: bool = True,
        filter_pattern: str = "*",
    ) -> None: ...
    @typing.overload
    def compress_files(self, in_files: list[str], out_archive: str) -> None: ...
    @typing.overload
    def compress_files(
        self,
        in_dir: str,
        out_archive: str,
        recursive: bool = True,
        filter_pattern: str = "*",
    ) -> None: ...

class BitGenericItem:
    def attributes(self) -> int: ...
    def is_dir(self) -> bool: ...
    def name(self) -> str: ...
    def path(self) -> str: ...
    def size(self) -> int: ...

class BitInFormat:
    def value(self) -> int: ...

class BitInOutFormat(BitInFormat):
    def default_method(self) -> BitCompressionMethod: ...
    def extension(self) -> str: ...
    def features(self) -> FormatFeatures: ...
    def has_feature(self, arg0: FormatFeatures) -> bool: ...

class BitInputArchive:
    def archive_path(self) -> str: ...
    def archive_property(self, arg0: BitProperty) -> BitPropVariant: ...
    def contains(self, path: str) -> bool: ...
    def detected_format(self) -> BitInFormat: ...
    @typing.overload
    def extract_to(self, arg0: str) -> None: ...
    @typing.overload
    def extract_to(self, path: str, indices: list[int]) -> None:
        """
        Extracts the items at the specified indices to the specified path
        """
    @typing.overload
    def extract_to(self, index: int) -> bytes:
        """
        Extracts the item at the specified index to a byte array
        """
    @typing.overload
    def extract_to(self) -> dict[str, bytes]:
        """
        Extracts all items to a dictionary of byte arrays
        """
    def is_item_encrypted(self, arg0: int) -> bool: ...
    def is_item_folder(self, arg0: int) -> bool: ...
    def item_at(self, index: int) -> BitArchiveItemOffset: ...
    def item_property(self, arg0: int, arg1: BitProperty) -> BitPropVariant: ...
    def items_count(self) -> int: ...
    def test(self) -> None: ...
    def test_item(self, index: int) -> None: ...

class BitMemCompressor(BitAbstractArchiveCreator):
    def __init__(self, format: BitInOutFormat) -> None: ...
    @typing.overload
    def compress_file(
        self, input: bytes, out_file: str, input_name: str = ""
    ) -> None: ...
    @typing.overload
    def compress_file(self, input: bytes, input_name: str = "") -> bytes: ...

class BitMemExtractor(BitAbstractArchiveOpener):
    def __init__(self, format: BitInFormat) -> None: ...
    @typing.overload
    def extract(self, in_archive: list[int], out_dir: str = "") -> None: ...
    @typing.overload
    def extract(self, in_archive: bytes, index: int) -> bytes: ...
    @typing.overload
    def extract(self, in_archive: bytes) -> dict[str, bytes]: ...
    def extract_items(
        self, in_archive: list[int], indices: list[int], out_dir: str = ""
    ) -> None: ...
    @typing.overload
    def extract_matching(
        self,
        in_archive: list[int],
        pattern: str,
        out_dir: str,
        filter_policy: FilterPolicy,
    ) -> None: ...
    @typing.overload
    def extract_matching(
        self, in_archive: bytes, pattern: bytes, filter_policy: FilterPolicy
    ) -> bytes: ...
    @typing.overload
    def extract_matching_regex(
        self,
        in_archive: list[int],
        regex: str,
        out_dir: str,
        filter_policy: FilterPolicy,
    ) -> None: ...
    @typing.overload
    def extract_matching_regex(
        self, in_archive: bytes, regex: bytes, filter_policy: FilterPolicy
    ) -> bytes: ...
    def test(self, arg0: list[int]) -> None: ...

class BitOutputArchive:
    def add_directory(self, arg0: str) -> None: ...
    @typing.overload
    def add_directory_contents(self, arg0: str, arg1: str, arg2: bool) -> None: ...
    @typing.overload
    def add_directory_contents(
        self, arg0: str, arg1: str, arg2: FilterPolicy, arg3: bool
    ) -> None: ...
    @typing.overload
    def add_file(self, arg0: str, arg1: str) -> None: ...
    @typing.overload
    def add_file(self, arg0: bytes, arg1: str) -> None: ...
    @typing.overload
    def add_files(self, arg0: list[str]) -> None: ...
    @typing.overload
    def add_files(self, arg0: str, arg1: str, arg2: bool) -> None: ...
    @typing.overload
    def add_files(
        self, arg0: str, arg1: str, arg2: FilterPolicy, arg3: bool
    ) -> None: ...
    @typing.overload
    def add_items(self, arg0: list[str]) -> None: ...
    @typing.overload
    def add_items(self, arg0: dict[str, str]) -> None: ...
    @typing.overload
    def compress_to(self, arg0: str) -> None: ...
    @typing.overload
    def compress_to(self) -> bytes: ...
    def items_count(self) -> int: ...

class BitPropVariant:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, value: bool) -> None: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    def clear(self) -> None: ...
    def get_bool(self) -> bool: ...
    def get_file_time(self) -> datetime.datetime: ...
    def get_int64(self) -> int: ...
    def get_native_string(self) -> str: ...
    def get_string(self) -> str: ...
    def get_uint64(self) -> int: ...
    def is_bool(self) -> bool: ...
    def is_file_time(self) -> bool: ...
    def is_int16(self) -> bool: ...
    def is_int32(self) -> bool: ...
    def is_int64(self) -> bool: ...
    def is_int8(self) -> bool: ...
    def is_string(self) -> bool: ...
    def is_uint16(self) -> bool: ...
    def is_uint32(self) -> bool: ...
    def is_uint64(self) -> bool: ...
    def is_uint8(self) -> bool: ...
    def type(self) -> BitPropVariantType: ...

class BitPropVariantType:
    """
    Members:

      Empty

      Bool

      String

      UInt8

      UInt16

      UInt32

      UInt64

      Int8

      Int16

      Int32

      Int64

      FileTime
    """

    Bool: typing.ClassVar[BitPropVariantType]  # value = <BitPropVariantType.Bool: 1>
    Empty: typing.ClassVar[BitPropVariantType]  # value = <BitPropVariantType.Empty: 0>
    FileTime: typing.ClassVar[
        BitPropVariantType
    ]  # value = <BitPropVariantType.FileTime: 11>
    Int16: typing.ClassVar[BitPropVariantType]  # value = <BitPropVariantType.Int16: 8>
    Int32: typing.ClassVar[BitPropVariantType]  # value = <BitPropVariantType.Int32: 9>
    Int64: typing.ClassVar[BitPropVariantType]  # value = <BitPropVariantType.Int64: 10>
    Int8: typing.ClassVar[BitPropVariantType]  # value = <BitPropVariantType.Int8: 7>
    String: typing.ClassVar[
        BitPropVariantType
    ]  # value = <BitPropVariantType.String: 2>
    UInt16: typing.ClassVar[
        BitPropVariantType
    ]  # value = <BitPropVariantType.UInt16: 4>
    UInt32: typing.ClassVar[
        BitPropVariantType
    ]  # value = <BitPropVariantType.UInt32: 5>
    UInt64: typing.ClassVar[
        BitPropVariantType
    ]  # value = <BitPropVariantType.UInt64: 6>
    UInt8: typing.ClassVar[BitPropVariantType]  # value = <BitPropVariantType.UInt8: 3>
    __members__: typing.ClassVar[
        dict[str, BitPropVariantType]
    ]  # value = {'Empty': <BitPropVariantType.Empty: 0>, 'Bool': <BitPropVariantType.Bool: 1>, 'String': <BitPropVariantType.String: 2>, 'UInt8': <BitPropVariantType.UInt8: 3>, 'UInt16': <BitPropVariantType.UInt16: 4>, 'UInt32': <BitPropVariantType.UInt32: 5>, 'UInt64': <BitPropVariantType.UInt64: 6>, 'Int8': <BitPropVariantType.Int8: 7>, 'Int16': <BitPropVariantType.Int16: 8>, 'Int32': <BitPropVariantType.Int32: 9>, 'Int64': <BitPropVariantType.Int64: 10>, 'FileTime': <BitPropVariantType.FileTime: 11>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class BitProperty:
    """
    Members:

      NoProperty

      MainSubfile

      HandlerItemIndex

      Path

      Name

      Extension

      IsDir

      Size

      PackSize

      Attrib

      CTime

      ATime

      MTime

      Solid

      Commented

      Encrypted

      SplitBefore

      SplitAfter

      DictionarySize

      CRC

      Type

      IsAnti

      Method

      HostOS

      FileSystem

      User

      Group

      Block

      Comment

      Position

      Prefix

      NumSubDirs

      NumSubFiles

      UnpackVer

      Volume

      IsVolume

      Offset

      Links

      NumBlocks

      NumVolumes

      TimeType

      Bit64

      BigEndian

      Cpu

      PhySize

      HeadersSize

      Checksum

      Characters

      Va

      Id

      ShortName

      CreatorApp

      SectorSize

      PosixAttrib

      SymLink

      Error

      TotalSize

      FreeSpace

      ClusterSize

      VolumeName

      LocalName

      Provider

      NtSecure

      IsAltStream

      IsAux

      IsDeleted

      IsTree

      Sha1

      Sha256

      ErrorType

      NumErrors

      ErrorFlags

      WarningFlags

      Warning

      NumStreams

      NumAltStreams

      AltStreamsSize

      VirtualSize

      UnpackSize

      TotalPhySize

      VolumeIndex

      SubType

      ShortComment

      CodePage

      IsNotArcType

      PhySizeCantBeDetected

      ZerosTailIsAllowed

      TailSize

      EmbeddedStubSize

      NtReparse

      HardLink

      INode

      StreamId

      ReadOnly

      OutName

      CopyLink
    """

    ATime: typing.ClassVar[BitProperty]  # value = <BitProperty.ATime: 11>
    AltStreamsSize: typing.ClassVar[
        BitProperty
    ]  # value = <BitProperty.AltStreamsSize: 76>
    Attrib: typing.ClassVar[BitProperty]  # value = <BitProperty.Attrib: 9>
    BigEndian: typing.ClassVar[BitProperty]  # value = <BitProperty.BigEndian: 42>
    Bit64: typing.ClassVar[BitProperty]  # value = <BitProperty.Bit64: 41>
    Block: typing.ClassVar[BitProperty]  # value = <BitProperty.Block: 27>
    CRC: typing.ClassVar[BitProperty]  # value = <BitProperty.CRC: 19>
    CTime: typing.ClassVar[BitProperty]  # value = <BitProperty.CTime: 10>
    Characters: typing.ClassVar[BitProperty]  # value = <BitProperty.Characters: 47>
    Checksum: typing.ClassVar[BitProperty]  # value = <BitProperty.Checksum: 46>
    ClusterSize: typing.ClassVar[BitProperty]  # value = <BitProperty.ClusterSize: 58>
    CodePage: typing.ClassVar[BitProperty]  # value = <BitProperty.CodePage: 83>
    Comment: typing.ClassVar[BitProperty]  # value = <BitProperty.Comment: 28>
    Commented: typing.ClassVar[BitProperty]  # value = <BitProperty.Commented: 14>
    CopyLink: typing.ClassVar[BitProperty]  # value = <BitProperty.CopyLink: 95>
    Cpu: typing.ClassVar[BitProperty]  # value = <BitProperty.Cpu: 43>
    CreatorApp: typing.ClassVar[BitProperty]  # value = <BitProperty.CreatorApp: 51>
    DictionarySize: typing.ClassVar[
        BitProperty
    ]  # value = <BitProperty.DictionarySize: 18>
    EmbeddedStubSize: typing.ClassVar[
        BitProperty
    ]  # value = <BitProperty.EmbeddedStubSize: 88>
    Encrypted: typing.ClassVar[BitProperty]  # value = <BitProperty.Encrypted: 15>
    Error: typing.ClassVar[BitProperty]  # value = <BitProperty.Error: 55>
    ErrorFlags: typing.ClassVar[BitProperty]  # value = <BitProperty.ErrorFlags: 71>
    ErrorType: typing.ClassVar[BitProperty]  # value = <BitProperty.ErrorType: 69>
    Extension: typing.ClassVar[BitProperty]  # value = <BitProperty.Extension: 5>
    FileSystem: typing.ClassVar[BitProperty]  # value = <BitProperty.FileSystem: 24>
    FreeSpace: typing.ClassVar[BitProperty]  # value = <BitProperty.FreeSpace: 57>
    Group: typing.ClassVar[BitProperty]  # value = <BitProperty.Group: 26>
    HandlerItemIndex: typing.ClassVar[
        BitProperty
    ]  # value = <BitProperty.HandlerItemIndex: 2>
    HardLink: typing.ClassVar[BitProperty]  # value = <BitProperty.HardLink: 90>
    HeadersSize: typing.ClassVar[BitProperty]  # value = <BitProperty.HeadersSize: 45>
    HostOS: typing.ClassVar[BitProperty]  # value = <BitProperty.HostOS: 23>
    INode: typing.ClassVar[BitProperty]  # value = <BitProperty.INode: 91>
    Id: typing.ClassVar[BitProperty]  # value = <BitProperty.Id: 49>
    IsAltStream: typing.ClassVar[BitProperty]  # value = <BitProperty.IsAltStream: 63>
    IsAnti: typing.ClassVar[BitProperty]  # value = <BitProperty.IsAnti: 21>
    IsAux: typing.ClassVar[BitProperty]  # value = <BitProperty.IsAux: 64>
    IsDeleted: typing.ClassVar[BitProperty]  # value = <BitProperty.IsDeleted: 65>
    IsDir: typing.ClassVar[BitProperty]  # value = <BitProperty.IsDir: 6>
    IsNotArcType: typing.ClassVar[BitProperty]  # value = <BitProperty.IsNotArcType: 84>
    IsTree: typing.ClassVar[BitProperty]  # value = <BitProperty.IsTree: 66>
    IsVolume: typing.ClassVar[BitProperty]  # value = <BitProperty.IsVolume: 35>
    Links: typing.ClassVar[BitProperty]  # value = <BitProperty.Links: 37>
    LocalName: typing.ClassVar[BitProperty]  # value = <BitProperty.LocalName: 60>
    MTime: typing.ClassVar[BitProperty]  # value = <BitProperty.MTime: 12>
    MainSubfile: typing.ClassVar[BitProperty]  # value = <BitProperty.MainSubfile: 1>
    Method: typing.ClassVar[BitProperty]  # value = <BitProperty.Method: 22>
    Name: typing.ClassVar[BitProperty]  # value = <BitProperty.Name: 4>
    NoProperty: typing.ClassVar[BitProperty]  # value = <BitProperty.NoProperty: 0>
    NtReparse: typing.ClassVar[BitProperty]  # value = <BitProperty.NtReparse: 89>
    NtSecure: typing.ClassVar[BitProperty]  # value = <BitProperty.NtSecure: 62>
    NumAltStreams: typing.ClassVar[
        BitProperty
    ]  # value = <BitProperty.NumAltStreams: 75>
    NumBlocks: typing.ClassVar[BitProperty]  # value = <BitProperty.NumBlocks: 38>
    NumErrors: typing.ClassVar[BitProperty]  # value = <BitProperty.NumErrors: 70>
    NumStreams: typing.ClassVar[BitProperty]  # value = <BitProperty.NumStreams: 74>
    NumSubDirs: typing.ClassVar[BitProperty]  # value = <BitProperty.NumSubDirs: 31>
    NumSubFiles: typing.ClassVar[BitProperty]  # value = <BitProperty.NumSubFiles: 32>
    NumVolumes: typing.ClassVar[BitProperty]  # value = <BitProperty.NumVolumes: 39>
    Offset: typing.ClassVar[BitProperty]  # value = <BitProperty.Offset: 36>
    OutName: typing.ClassVar[BitProperty]  # value = <BitProperty.OutName: 94>
    PackSize: typing.ClassVar[BitProperty]  # value = <BitProperty.PackSize: 8>
    Path: typing.ClassVar[BitProperty]  # value = <BitProperty.Path: 3>
    PhySize: typing.ClassVar[BitProperty]  # value = <BitProperty.PhySize: 44>
    PhySizeCantBeDetected: typing.ClassVar[
        BitProperty
    ]  # value = <BitProperty.PhySizeCantBeDetected: 85>
    Position: typing.ClassVar[BitProperty]  # value = <BitProperty.Position: 29>
    PosixAttrib: typing.ClassVar[BitProperty]  # value = <BitProperty.PosixAttrib: 53>
    Prefix: typing.ClassVar[BitProperty]  # value = <BitProperty.Prefix: 30>
    Provider: typing.ClassVar[BitProperty]  # value = <BitProperty.Provider: 61>
    ReadOnly: typing.ClassVar[BitProperty]  # value = <BitProperty.ReadOnly: 93>
    SectorSize: typing.ClassVar[BitProperty]  # value = <BitProperty.SectorSize: 52>
    Sha1: typing.ClassVar[BitProperty]  # value = <BitProperty.Sha1: 67>
    Sha256: typing.ClassVar[BitProperty]  # value = <BitProperty.Sha256: 68>
    ShortComment: typing.ClassVar[BitProperty]  # value = <BitProperty.ShortComment: 82>
    ShortName: typing.ClassVar[BitProperty]  # value = <BitProperty.ShortName: 50>
    Size: typing.ClassVar[BitProperty]  # value = <BitProperty.Size: 7>
    Solid: typing.ClassVar[BitProperty]  # value = <BitProperty.Solid: 13>
    SplitAfter: typing.ClassVar[BitProperty]  # value = <BitProperty.SplitAfter: 17>
    SplitBefore: typing.ClassVar[BitProperty]  # value = <BitProperty.SplitBefore: 16>
    StreamId: typing.ClassVar[BitProperty]  # value = <BitProperty.StreamId: 92>
    SubType: typing.ClassVar[BitProperty]  # value = <BitProperty.SubType: 81>
    SymLink: typing.ClassVar[BitProperty]  # value = <BitProperty.SymLink: 54>
    TailSize: typing.ClassVar[BitProperty]  # value = <BitProperty.TailSize: 87>
    TimeType: typing.ClassVar[BitProperty]  # value = <BitProperty.TimeType: 40>
    TotalPhySize: typing.ClassVar[BitProperty]  # value = <BitProperty.TotalPhySize: 79>
    TotalSize: typing.ClassVar[BitProperty]  # value = <BitProperty.TotalSize: 56>
    Type: typing.ClassVar[BitProperty]  # value = <BitProperty.Type: 20>
    UnpackSize: typing.ClassVar[BitProperty]  # value = <BitProperty.UnpackSize: 78>
    UnpackVer: typing.ClassVar[BitProperty]  # value = <BitProperty.UnpackVer: 33>
    User: typing.ClassVar[BitProperty]  # value = <BitProperty.User: 25>
    Va: typing.ClassVar[BitProperty]  # value = <BitProperty.Va: 48>
    VirtualSize: typing.ClassVar[BitProperty]  # value = <BitProperty.VirtualSize: 77>
    Volume: typing.ClassVar[BitProperty]  # value = <BitProperty.Volume: 34>
    VolumeIndex: typing.ClassVar[BitProperty]  # value = <BitProperty.VolumeIndex: 80>
    VolumeName: typing.ClassVar[BitProperty]  # value = <BitProperty.VolumeName: 59>
    Warning: typing.ClassVar[BitProperty]  # value = <BitProperty.Warning: 73>
    WarningFlags: typing.ClassVar[BitProperty]  # value = <BitProperty.WarningFlags: 72>
    ZerosTailIsAllowed: typing.ClassVar[
        BitProperty
    ]  # value = <BitProperty.ZerosTailIsAllowed: 86>
    __members__: typing.ClassVar[
        dict[str, BitProperty]
    ]  # value = {'NoProperty': <BitProperty.NoProperty: 0>, 'MainSubfile': <BitProperty.MainSubfile: 1>, 'HandlerItemIndex': <BitProperty.HandlerItemIndex: 2>, 'Path': <BitProperty.Path: 3>, 'Name': <BitProperty.Name: 4>, 'Extension': <BitProperty.Extension: 5>, 'IsDir': <BitProperty.IsDir: 6>, 'Size': <BitProperty.Size: 7>, 'PackSize': <BitProperty.PackSize: 8>, 'Attrib': <BitProperty.Attrib: 9>, 'CTime': <BitProperty.CTime: 10>, 'ATime': <BitProperty.ATime: 11>, 'MTime': <BitProperty.MTime: 12>, 'Solid': <BitProperty.Solid: 13>, 'Commented': <BitProperty.Commented: 14>, 'Encrypted': <BitProperty.Encrypted: 15>, 'SplitBefore': <BitProperty.SplitBefore: 16>, 'SplitAfter': <BitProperty.SplitAfter: 17>, 'DictionarySize': <BitProperty.DictionarySize: 18>, 'CRC': <BitProperty.CRC: 19>, 'Type': <BitProperty.Type: 20>, 'IsAnti': <BitProperty.IsAnti: 21>, 'Method': <BitProperty.Method: 22>, 'HostOS': <BitProperty.HostOS: 23>, 'FileSystem': <BitProperty.FileSystem: 24>, 'User': <BitProperty.User: 25>, 'Group': <BitProperty.Group: 26>, 'Block': <BitProperty.Block: 27>, 'Comment': <BitProperty.Comment: 28>, 'Position': <BitProperty.Position: 29>, 'Prefix': <BitProperty.Prefix: 30>, 'NumSubDirs': <BitProperty.NumSubDirs: 31>, 'NumSubFiles': <BitProperty.NumSubFiles: 32>, 'UnpackVer': <BitProperty.UnpackVer: 33>, 'Volume': <BitProperty.Volume: 34>, 'IsVolume': <BitProperty.IsVolume: 35>, 'Offset': <BitProperty.Offset: 36>, 'Links': <BitProperty.Links: 37>, 'NumBlocks': <BitProperty.NumBlocks: 38>, 'NumVolumes': <BitProperty.NumVolumes: 39>, 'TimeType': <BitProperty.TimeType: 40>, 'Bit64': <BitProperty.Bit64: 41>, 'BigEndian': <BitProperty.BigEndian: 42>, 'Cpu': <BitProperty.Cpu: 43>, 'PhySize': <BitProperty.PhySize: 44>, 'HeadersSize': <BitProperty.HeadersSize: 45>, 'Checksum': <BitProperty.Checksum: 46>, 'Characters': <BitProperty.Characters: 47>, 'Va': <BitProperty.Va: 48>, 'Id': <BitProperty.Id: 49>, 'ShortName': <BitProperty.ShortName: 50>, 'CreatorApp': <BitProperty.CreatorApp: 51>, 'SectorSize': <BitProperty.SectorSize: 52>, 'PosixAttrib': <BitProperty.PosixAttrib: 53>, 'SymLink': <BitProperty.SymLink: 54>, 'Error': <BitProperty.Error: 55>, 'TotalSize': <BitProperty.TotalSize: 56>, 'FreeSpace': <BitProperty.FreeSpace: 57>, 'ClusterSize': <BitProperty.ClusterSize: 58>, 'VolumeName': <BitProperty.VolumeName: 59>, 'LocalName': <BitProperty.LocalName: 60>, 'Provider': <BitProperty.Provider: 61>, 'NtSecure': <BitProperty.NtSecure: 62>, 'IsAltStream': <BitProperty.IsAltStream: 63>, 'IsAux': <BitProperty.IsAux: 64>, 'IsDeleted': <BitProperty.IsDeleted: 65>, 'IsTree': <BitProperty.IsTree: 66>, 'Sha1': <BitProperty.Sha1: 67>, 'Sha256': <BitProperty.Sha256: 68>, 'ErrorType': <BitProperty.ErrorType: 69>, 'NumErrors': <BitProperty.NumErrors: 70>, 'ErrorFlags': <BitProperty.ErrorFlags: 71>, 'WarningFlags': <BitProperty.WarningFlags: 72>, 'Warning': <BitProperty.Warning: 73>, 'NumStreams': <BitProperty.NumStreams: 74>, 'NumAltStreams': <BitProperty.NumAltStreams: 75>, 'AltStreamsSize': <BitProperty.AltStreamsSize: 76>, 'VirtualSize': <BitProperty.VirtualSize: 77>, 'UnpackSize': <BitProperty.UnpackSize: 78>, 'TotalPhySize': <BitProperty.TotalPhySize: 79>, 'VolumeIndex': <BitProperty.VolumeIndex: 80>, 'SubType': <BitProperty.SubType: 81>, 'ShortComment': <BitProperty.ShortComment: 82>, 'CodePage': <BitProperty.CodePage: 83>, 'IsNotArcType': <BitProperty.IsNotArcType: 84>, 'PhySizeCantBeDetected': <BitProperty.PhySizeCantBeDetected: 85>, 'ZerosTailIsAllowed': <BitProperty.ZerosTailIsAllowed: 86>, 'TailSize': <BitProperty.TailSize: 87>, 'EmbeddedStubSize': <BitProperty.EmbeddedStubSize: 88>, 'NtReparse': <BitProperty.NtReparse: 89>, 'HardLink': <BitProperty.HardLink: 90>, 'INode': <BitProperty.INode: 91>, 'StreamId': <BitProperty.StreamId: 92>, 'ReadOnly': <BitProperty.ReadOnly: 93>, 'OutName': <BitProperty.OutName: 94>, 'CopyLink': <BitProperty.CopyLink: 95>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class BitStringCompressor(BitAbstractArchiveCreator):
    def __init__(self, format: BitInOutFormat) -> None: ...
    @typing.overload
    def compress_file(
        self, in_file: str, out_file: str, input_name: str = ""
    ) -> None: ...
    @typing.overload
    def compress_file(self, in_file: str, input_name: str = "") -> bytes: ...

class BitStringExtractor(BitAbstractArchiveOpener):
    def __init__(self, format: BitInFormat) -> None: ...
    @typing.overload
    def extract(self, in_archive: str, out_dir: str) -> None: ...
    @typing.overload
    def extract(self, in_archive: str, index: int) -> bytes: ...
    @typing.overload
    def extract(self, in_archive: str) -> dict[str, bytes]: ...
    def extract_items(
        self, in_archive: str, indices: list[int], out_dir: str = ""
    ) -> None: ...
    @typing.overload
    def extract_matching(
        self, in_archive: str, pattern: str, out_dir: str, filter_policy: FilterPolicy
    ) -> None: ...
    @typing.overload
    def extract_matching(
        self, in_archive: str, pattern: str, filter_policy: FilterPolicy
    ) -> bytes: ...
    @typing.overload
    def extract_matching_regex(
        self, in_archive: str, regex: str, out_dir: str, filter_policy: FilterPolicy
    ) -> None: ...
    @typing.overload
    def extract_matching_regex(
        self, in_archive: str, regex: str, filter_policy: FilterPolicy
    ) -> bytes: ...
    def test(self, arg0: str) -> None: ...

class DeletePolicy:
    """
    Members:

      ItemOnly

      RecurseDirs
    """

    ItemOnly: typing.ClassVar[DeletePolicy]  # value = <DeletePolicy.ItemOnly: 0>
    RecurseDirs: typing.ClassVar[DeletePolicy]  # value = <DeletePolicy.RecurseDirs: 1>
    __members__: typing.ClassVar[
        dict[str, DeletePolicy]
    ]  # value = {'ItemOnly': <DeletePolicy.ItemOnly: 0>, 'RecurseDirs': <DeletePolicy.RecurseDirs: 1>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class FilterPolicy:
    """
    Members:

      Include

      Exclude
    """

    Exclude: typing.ClassVar[FilterPolicy]  # value = <FilterPolicy.Exclude: 1>
    Include: typing.ClassVar[FilterPolicy]  # value = <FilterPolicy.Include: 0>
    __members__: typing.ClassVar[
        dict[str, FilterPolicy]
    ]  # value = {'Include': <FilterPolicy.Include: 0>, 'Exclude': <FilterPolicy.Exclude: 1>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class FormatFeatures:
    """
    Members:

      MultipleFiles

      SolidArchive

      CompressionLevel

      Encryption

      HeaderEncryption

      MultipleMethods
    """

    CompressionLevel: typing.ClassVar[
        FormatFeatures
    ]  # value = <FormatFeatures.CompressionLevel: 4>
    Encryption: typing.ClassVar[
        FormatFeatures
    ]  # value = <FormatFeatures.Encryption: 8>
    HeaderEncryption: typing.ClassVar[
        FormatFeatures
    ]  # value = <FormatFeatures.HeaderEncryption: 16>
    MultipleFiles: typing.ClassVar[
        FormatFeatures
    ]  # value = <FormatFeatures.MultipleFiles: 1>
    MultipleMethods: typing.ClassVar[
        FormatFeatures
    ]  # value = <FormatFeatures.MultipleMethods: 32>
    SolidArchive: typing.ClassVar[
        FormatFeatures
    ]  # value = <FormatFeatures.SolidArchive: 2>
    __members__: typing.ClassVar[
        dict[str, FormatFeatures]
    ]  # value = {'MultipleFiles': <FormatFeatures.MultipleFiles: 1>, 'SolidArchive': <FormatFeatures.SolidArchive: 2>, 'CompressionLevel': <FormatFeatures.CompressionLevel: 4>, 'Encryption': <FormatFeatures.Encryption: 8>, 'HeaderEncryption': <FormatFeatures.HeaderEncryption: 16>, 'MultipleMethods': <FormatFeatures.MultipleMethods: 32>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class OverwriteMode:
    """
    Members:

      None_

      Overwrite

      Skip
    """

    None_: typing.ClassVar[OverwriteMode]  # value = <OverwriteMode.None_: 0>
    Overwrite: typing.ClassVar[OverwriteMode]  # value = <OverwriteMode.Overwrite: 1>
    Skip: typing.ClassVar[OverwriteMode]  # value = <OverwriteMode.Skip: 2>
    __members__: typing.ClassVar[
        dict[str, OverwriteMode]
    ]  # value = {'None_': <OverwriteMode.None_: 0>, 'Overwrite': <OverwriteMode.Overwrite: 1>, 'Skip': <OverwriteMode.Skip: 2>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class UpdateMode:
    """
    Members:

      None_

      Append

      Update
    """

    Append: typing.ClassVar[UpdateMode]  # value = <UpdateMode.Append: 1>
    None_: typing.ClassVar[UpdateMode]  # value = <UpdateMode.None_: 0>
    Update: typing.ClassVar[UpdateMode]  # value = <UpdateMode.Update: 2>
    __members__: typing.ClassVar[
        dict[str, UpdateMode]
    ]  # value = {'None_': <UpdateMode.None_: 0>, 'Append': <UpdateMode.Append: 1>, 'Update': <UpdateMode.Update: 2>}
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

def set_large_page_mode() -> None:
    """
    Enable large page mode for 7zip library. This can improve performance on some systems.
    """

def set_lib7zip_path(lib7zip_path: str = "") -> str:
    """
    Configure the path to the 7zip library.
    """

def version() -> str:
    """
    The _core plugin version.
    """

ATime: BitProperty  # value = <BitProperty.ATime: 11>
AltStreamsSize: BitProperty  # value = <BitProperty.AltStreamsSize: 76>
Attrib: BitProperty  # value = <BitProperty.Attrib: 9>
BZip2: BitCompressionMethod  # value = <BitCompressionMethod.BZip2: 3>
BigEndian: BitProperty  # value = <BitProperty.BigEndian: 42>
Bit64: BitProperty  # value = <BitProperty.Bit64: 41>
Block: BitProperty  # value = <BitProperty.Block: 27>
Bool: BitPropVariantType  # value = <BitPropVariantType.Bool: 1>
CRC: BitProperty  # value = <BitProperty.CRC: 19>
CTime: BitProperty  # value = <BitProperty.CTime: 10>
Characters: BitProperty  # value = <BitProperty.Characters: 47>
Checksum: BitProperty  # value = <BitProperty.Checksum: 46>
ClusterSize: BitProperty  # value = <BitProperty.ClusterSize: 58>
CodePage: BitProperty  # value = <BitProperty.CodePage: 83>
Comment: BitProperty  # value = <BitProperty.Comment: 28>
Commented: BitProperty  # value = <BitProperty.Commented: 14>
Copy: BitCompressionMethod  # value = <BitCompressionMethod.Copy: 0>
CopyLink: BitProperty  # value = <BitProperty.CopyLink: 95>
Cpu: BitProperty  # value = <BitProperty.Cpu: 43>
CreatorApp: BitProperty  # value = <BitProperty.CreatorApp: 51>
Deflate: BitCompressionMethod  # value = <BitCompressionMethod.Deflate: 1>
Deflate64: BitCompressionMethod  # value = <BitCompressionMethod.Deflate64: 2>
DictionarySize: BitProperty  # value = <BitProperty.DictionarySize: 18>
EmbeddedStubSize: BitProperty  # value = <BitProperty.EmbeddedStubSize: 88>
Empty: BitPropVariantType  # value = <BitPropVariantType.Empty: 0>
Encrypted: BitProperty  # value = <BitProperty.Encrypted: 15>
Error: BitProperty  # value = <BitProperty.Error: 55>
ErrorFlags: BitProperty  # value = <BitProperty.ErrorFlags: 71>
ErrorType: BitProperty  # value = <BitProperty.ErrorType: 69>
Exclude: FilterPolicy  # value = <FilterPolicy.Exclude: 1>
Extension: BitProperty  # value = <BitProperty.Extension: 5>
Fast: BitCompressionLevel  # value = <BitCompressionLevel.Fast: 3>
Fastest: BitCompressionLevel  # value = <BitCompressionLevel.Fastest: 1>
FileSystem: BitProperty  # value = <BitProperty.FileSystem: 24>
FileTime: BitPropVariantType  # value = <BitPropVariantType.FileTime: 11>
FormatAPM: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatArj: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatAuto: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatBZip2: BitInOutFormat  # value = <pybit7z._core.BitInOutFormat object>
FormatCab: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatChm: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatCoff: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatCompound: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatCpio: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatCramFS: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatDeb: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatDmg: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatElf: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatExt: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatFat: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatFlv: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatGZip: BitInOutFormat  # value = <pybit7z._core.BitInOutFormat object>
FormatGpt: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatHfs: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatHxs: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatIHex: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatIso: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatLzh: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatLzma: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatLzma86: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatMacho: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatMbr: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatMslz: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatMub: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatNsis: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatNtfs: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatPe: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatPpmd: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatQcow: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatRar: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatRar5: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatRpm: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatSevenZip: BitInOutFormat  # value = <pybit7z._core.BitInOutFormat object>
FormatSplit: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatSquashFS: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatSwf: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatSwfc: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatTE: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatTar: BitInOutFormat  # value = <pybit7z._core.BitInOutFormat object>
FormatUEFIc: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatUEFIs: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatUdf: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatVdi: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatVhd: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatVhdx: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatVmdk: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatWim: BitInOutFormat  # value = <pybit7z._core.BitInOutFormat object>
FormatXar: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatXz: BitInOutFormat  # value = <pybit7z._core.BitInOutFormat object>
FormatZ: BitInFormat  # value = <pybit7z._core.BitInFormat object>
FormatZip: BitInOutFormat  # value = <pybit7z._core.BitInOutFormat object>
FreeSpace: BitProperty  # value = <BitProperty.FreeSpace: 57>
Group: BitProperty  # value = <BitProperty.Group: 26>
HandlerItemIndex: BitProperty  # value = <BitProperty.HandlerItemIndex: 2>
HardLink: BitProperty  # value = <BitProperty.HardLink: 90>
HeadersSize: BitProperty  # value = <BitProperty.HeadersSize: 45>
HostOS: BitProperty  # value = <BitProperty.HostOS: 23>
INode: BitProperty  # value = <BitProperty.INode: 91>
Id: BitProperty  # value = <BitProperty.Id: 49>
Include: FilterPolicy  # value = <FilterPolicy.Include: 0>
Int16: BitPropVariantType  # value = <BitPropVariantType.Int16: 8>
Int32: BitPropVariantType  # value = <BitPropVariantType.Int32: 9>
Int64: BitPropVariantType  # value = <BitPropVariantType.Int64: 10>
Int8: BitPropVariantType  # value = <BitPropVariantType.Int8: 7>
IsAltStream: BitProperty  # value = <BitProperty.IsAltStream: 63>
IsAnti: BitProperty  # value = <BitProperty.IsAnti: 21>
IsAux: BitProperty  # value = <BitProperty.IsAux: 64>
IsDeleted: BitProperty  # value = <BitProperty.IsDeleted: 65>
IsDir: BitProperty  # value = <BitProperty.IsDir: 6>
IsNotArcType: BitProperty  # value = <BitProperty.IsNotArcType: 84>
IsTree: BitProperty  # value = <BitProperty.IsTree: 66>
IsVolume: BitProperty  # value = <BitProperty.IsVolume: 35>
ItemOnly: DeletePolicy  # value = <DeletePolicy.ItemOnly: 0>
Links: BitProperty  # value = <BitProperty.Links: 37>
LocalName: BitProperty  # value = <BitProperty.LocalName: 60>
Lzma: BitCompressionMethod  # value = <BitCompressionMethod.Lzma: 4>
Lzma2: BitCompressionMethod  # value = <BitCompressionMethod.Lzma2: 5>
MTime: BitProperty  # value = <BitProperty.MTime: 12>
MainSubfile: BitProperty  # value = <BitProperty.MainSubfile: 1>
Max: BitCompressionLevel  # value = <BitCompressionLevel.Max: 7>
Method: BitProperty  # value = <BitProperty.Method: 22>
Name: BitProperty  # value = <BitProperty.Name: 4>
NoProperty: BitProperty  # value = <BitProperty.NoProperty: 0>
None_: OverwriteMode  # value = <OverwriteMode.None_: 0>
Normal: BitCompressionLevel  # value = <BitCompressionLevel.Normal: 5>
NtReparse: BitProperty  # value = <BitProperty.NtReparse: 89>
NtSecure: BitProperty  # value = <BitProperty.NtSecure: 62>
NumAltStreams: BitProperty  # value = <BitProperty.NumAltStreams: 75>
NumBlocks: BitProperty  # value = <BitProperty.NumBlocks: 38>
NumErrors: BitProperty  # value = <BitProperty.NumErrors: 70>
NumStreams: BitProperty  # value = <BitProperty.NumStreams: 74>
NumSubDirs: BitProperty  # value = <BitProperty.NumSubDirs: 31>
NumSubFiles: BitProperty  # value = <BitProperty.NumSubFiles: 32>
NumVolumes: BitProperty  # value = <BitProperty.NumVolumes: 39>
Offset: BitProperty  # value = <BitProperty.Offset: 36>
OutName: BitProperty  # value = <BitProperty.OutName: 94>
Overwrite: OverwriteMode  # value = <OverwriteMode.Overwrite: 1>
PackSize: BitProperty  # value = <BitProperty.PackSize: 8>
Path: BitProperty  # value = <BitProperty.Path: 3>
PhySize: BitProperty  # value = <BitProperty.PhySize: 44>
PhySizeCantBeDetected: BitProperty  # value = <BitProperty.PhySizeCantBeDetected: 85>
Position: BitProperty  # value = <BitProperty.Position: 29>
PosixAttrib: BitProperty  # value = <BitProperty.PosixAttrib: 53>
Ppmd: BitCompressionMethod  # value = <BitCompressionMethod.Ppmd: 6>
Prefix: BitProperty  # value = <BitProperty.Prefix: 30>
Provider: BitProperty  # value = <BitProperty.Provider: 61>
ReadOnly: BitProperty  # value = <BitProperty.ReadOnly: 93>
RecurseDirs: DeletePolicy  # value = <DeletePolicy.RecurseDirs: 1>
SectorSize: BitProperty  # value = <BitProperty.SectorSize: 52>
Sha1: BitProperty  # value = <BitProperty.Sha1: 67>
Sha256: BitProperty  # value = <BitProperty.Sha256: 68>
ShortComment: BitProperty  # value = <BitProperty.ShortComment: 82>
ShortName: BitProperty  # value = <BitProperty.ShortName: 50>
Size: BitProperty  # value = <BitProperty.Size: 7>
Skip: OverwriteMode  # value = <OverwriteMode.Skip: 2>
Solid: BitProperty  # value = <BitProperty.Solid: 13>
SplitAfter: BitProperty  # value = <BitProperty.SplitAfter: 17>
SplitBefore: BitProperty  # value = <BitProperty.SplitBefore: 16>
StreamId: BitProperty  # value = <BitProperty.StreamId: 92>
String: BitPropVariantType  # value = <BitPropVariantType.String: 2>
SubType: BitProperty  # value = <BitProperty.SubType: 81>
SymLink: BitProperty  # value = <BitProperty.SymLink: 54>
TailSize: BitProperty  # value = <BitProperty.TailSize: 87>
TimeType: BitProperty  # value = <BitProperty.TimeType: 40>
TotalPhySize: BitProperty  # value = <BitProperty.TotalPhySize: 79>
TotalSize: BitProperty  # value = <BitProperty.TotalSize: 56>
Type: BitProperty  # value = <BitProperty.Type: 20>
UInt16: BitPropVariantType  # value = <BitPropVariantType.UInt16: 4>
UInt32: BitPropVariantType  # value = <BitPropVariantType.UInt32: 5>
UInt64: BitPropVariantType  # value = <BitPropVariantType.UInt64: 6>
UInt8: BitPropVariantType  # value = <BitPropVariantType.UInt8: 3>
Ultra: BitCompressionLevel  # value = <BitCompressionLevel.Ultra: 9>
UnpackSize: BitProperty  # value = <BitProperty.UnpackSize: 78>
UnpackVer: BitProperty  # value = <BitProperty.UnpackVer: 33>
User: BitProperty  # value = <BitProperty.User: 25>
Va: BitProperty  # value = <BitProperty.Va: 48>
VirtualSize: BitProperty  # value = <BitProperty.VirtualSize: 77>
Volume: BitProperty  # value = <BitProperty.Volume: 34>
VolumeIndex: BitProperty  # value = <BitProperty.VolumeIndex: 80>
VolumeName: BitProperty  # value = <BitProperty.VolumeName: 59>
Warning: BitProperty  # value = <BitProperty.Warning: 73>
WarningFlags: BitProperty  # value = <BitProperty.WarningFlags: 72>
ZerosTailIsAllowed: BitProperty  # value = <BitProperty.ZerosTailIsAllowed: 86>
BitFileExtractor = BitStringExtractor
