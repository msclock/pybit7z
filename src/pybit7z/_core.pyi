"""
Pybind11 _core plugin
-----------------------
.. currentmodule:: _core

"""

from __future__ import annotations

import datetime
import typing

__all__: list[str] = [
    "CRC",
    "ATime",
    "AbortOperation",
    "AltStreamsSize",
    "Attrib",
    "BZip2",
    "BigEndian",
    "Bit7zLibrary",
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
    "DataAndHeaders",
    "DataOnly",
    "Deflate",
    "Deflate64",
    "DeletePolicy",
    "DictionarySize",
    "EmbeddedStubSize",
    "Empty",
    "Encrypted",
    "EncryptionScope",
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
    "FilterResult",
    "FolderPathPolicy",
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
    "KeepName",
    "KeepPath",
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
    "Normal",
    "Nothing",
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
    "ProcessItem",
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
    "SkipItem",
    "Solid",
    "SplitAfter",
    "SplitBefore",
    "StreamId",
    "String",
    "Strip",
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
    "platform_lib7zip_name",
    "version",
]

class Bit7zLibrary:
    """
    The Bit7zLibrary class allows accessing the basic functionalities provided by the 7z DLLs.
    """
    def __init__(self, lib_path: str = "") -> None: ...
    def use_large_pages(self) -> None:
        """
        Enable large page mode for 7zip library. This can improve performance on some systems.
        """

class BitException(Exception):
    pass

class BitCompressionLevel:
    """
    Compression level for 7zip library

    Members:

      Nothing

      Fastest

      Fast

      Normal

      Max

      Ultra
    """

    Fast: typing.ClassVar[BitCompressionLevel]
    Fastest: typing.ClassVar[BitCompressionLevel]
    Max: typing.ClassVar[BitCompressionLevel]
    Normal: typing.ClassVar[BitCompressionLevel]
    Nothing: typing.ClassVar[BitCompressionLevel]
    Ultra: typing.ClassVar[BitCompressionLevel]
    __members__: typing.ClassVar[dict[str, BitCompressionLevel]]
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
    Compression method by bit7z when creating archives.

    Members:

      Copy

      Deflate

      Deflate64

      BZip2

      Lzma

      Lzma2

      Ppmd
    """

    BZip2: typing.ClassVar[BitCompressionMethod]
    Copy: typing.ClassVar[BitCompressionMethod]
    Deflate: typing.ClassVar[BitCompressionMethod]
    Deflate64: typing.ClassVar[BitCompressionMethod]
    Lzma: typing.ClassVar[BitCompressionMethod]
    Lzma2: typing.ClassVar[BitCompressionMethod]
    Ppmd: typing.ClassVar[BitCompressionMethod]
    __members__: typing.ClassVar[dict[str, BitCompressionMethod]]
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
    Features of a format supported by bit7z

    Members:

      MultipleFiles : Archive supports multiple files.

      SolidArchive : Archive supports solid mode.

      CompressionLevel : Archive supports compression level.

      Encryption : Archive supports encryption.

      HeaderEncryption : Archive supports encrypted headers.

      MultipleMethods : Archive supports multiple compression methods.
    """

    CompressionLevel: typing.ClassVar[FormatFeatures]
    Encryption: typing.ClassVar[FormatFeatures]
    HeaderEncryption: typing.ClassVar[FormatFeatures]
    MultipleFiles: typing.ClassVar[FormatFeatures]
    MultipleMethods: typing.ClassVar[FormatFeatures]
    SolidArchive: typing.ClassVar[FormatFeatures]
    __members__: typing.ClassVar[dict[str, FormatFeatures]]
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

class DeletePolicy:
    """
    Delete policy for archive items.

    Members:

      ItemOnly

      RecurseDirs
    """

    ItemOnly: typing.ClassVar[DeletePolicy]
    RecurseDirs: typing.ClassVar[DeletePolicy]
    __members__: typing.ClassVar[dict[str, DeletePolicy]]
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

class BitInFormat:
    """
    The BitInFormat class specifies an extractable archive format.
    """
    def __eq__(self, arg0: typing.Any) -> bool: ...
    def __hash__(self) -> int: ...
    def __ne__(self, arg0: typing.Any) -> bool: ...
    def value(self) -> int:
        """
        the value of the format in the 7z SDK.
        """

class BitInOutFormat(BitInFormat):
    """
    The BitInOutFormat class specifies a format available for creating new archives and extract old ones.
    """
    def default_method(self) -> BitCompressionMethod:
        """
        the default method used for compressing the archive format.
        """
    def extension(self) -> str:
        """
        the default file extension of the archive format.
        """
    def features(self) -> FormatFeatures:
        """
        the bitset of the features supported by the format.
        """
    def has_feature(self, arg0: FormatFeatures) -> bool:
        """
        Checks if the format has a specific feature (see FormatFeatures enum)
        Args:
            feature (FormatFeatures): the feature to check
        Returns:
            bool: a boolean value indicating whether the format has the given feature.
        """

class BitProperty:
    """
    The BitProperty enum represents the archive/item properties that 7-zip can read or write.

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

    ATime: typing.ClassVar[BitProperty]
    AltStreamsSize: typing.ClassVar[BitProperty]
    Attrib: typing.ClassVar[BitProperty]
    BigEndian: typing.ClassVar[BitProperty]
    Bit64: typing.ClassVar[BitProperty]
    Block: typing.ClassVar[BitProperty]
    CRC: typing.ClassVar[BitProperty]
    CTime: typing.ClassVar[BitProperty]
    Characters: typing.ClassVar[BitProperty]
    Checksum: typing.ClassVar[BitProperty]
    ClusterSize: typing.ClassVar[BitProperty]
    CodePage: typing.ClassVar[BitProperty]
    Comment: typing.ClassVar[BitProperty]
    Commented: typing.ClassVar[BitProperty]
    CopyLink: typing.ClassVar[BitProperty]
    Cpu: typing.ClassVar[BitProperty]
    CreatorApp: typing.ClassVar[BitProperty]
    DictionarySize: typing.ClassVar[BitProperty]
    EmbeddedStubSize: typing.ClassVar[BitProperty]
    Encrypted: typing.ClassVar[BitProperty]
    Error: typing.ClassVar[BitProperty]
    ErrorFlags: typing.ClassVar[BitProperty]
    ErrorType: typing.ClassVar[BitProperty]
    Extension: typing.ClassVar[BitProperty]
    FileSystem: typing.ClassVar[BitProperty]
    FreeSpace: typing.ClassVar[BitProperty]
    Group: typing.ClassVar[BitProperty]
    HandlerItemIndex: typing.ClassVar[BitProperty]
    HardLink: typing.ClassVar[BitProperty]
    HeadersSize: typing.ClassVar[BitProperty]
    HostOS: typing.ClassVar[BitProperty]
    INode: typing.ClassVar[BitProperty]
    Id: typing.ClassVar[BitProperty]
    IsAltStream: typing.ClassVar[BitProperty]
    IsAnti: typing.ClassVar[BitProperty]
    IsAux: typing.ClassVar[BitProperty]
    IsDeleted: typing.ClassVar[BitProperty]
    IsDir: typing.ClassVar[BitProperty]
    IsNotArcType: typing.ClassVar[BitProperty]
    IsTree: typing.ClassVar[BitProperty]
    IsVolume: typing.ClassVar[BitProperty]
    Links: typing.ClassVar[BitProperty]
    LocalName: typing.ClassVar[BitProperty]
    MTime: typing.ClassVar[BitProperty]
    MainSubfile: typing.ClassVar[BitProperty]
    Method: typing.ClassVar[BitProperty]
    Name: typing.ClassVar[BitProperty]
    NoProperty: typing.ClassVar[BitProperty]
    NtReparse: typing.ClassVar[BitProperty]
    NtSecure: typing.ClassVar[BitProperty]
    NumAltStreams: typing.ClassVar[BitProperty]
    NumBlocks: typing.ClassVar[BitProperty]
    NumErrors: typing.ClassVar[BitProperty]
    NumStreams: typing.ClassVar[BitProperty]
    NumSubDirs: typing.ClassVar[BitProperty]
    NumSubFiles: typing.ClassVar[BitProperty]
    NumVolumes: typing.ClassVar[BitProperty]
    Offset: typing.ClassVar[BitProperty]
    OutName: typing.ClassVar[BitProperty]
    PackSize: typing.ClassVar[BitProperty]
    Path: typing.ClassVar[BitProperty]
    PhySize: typing.ClassVar[BitProperty]
    PhySizeCantBeDetected: typing.ClassVar[BitProperty]
    Position: typing.ClassVar[BitProperty]
    PosixAttrib: typing.ClassVar[BitProperty]
    Prefix: typing.ClassVar[BitProperty]
    Provider: typing.ClassVar[BitProperty]
    ReadOnly: typing.ClassVar[BitProperty]
    SectorSize: typing.ClassVar[BitProperty]
    Sha1: typing.ClassVar[BitProperty]
    Sha256: typing.ClassVar[BitProperty]
    ShortComment: typing.ClassVar[BitProperty]
    ShortName: typing.ClassVar[BitProperty]
    Size: typing.ClassVar[BitProperty]
    Solid: typing.ClassVar[BitProperty]
    SplitAfter: typing.ClassVar[BitProperty]
    SplitBefore: typing.ClassVar[BitProperty]
    StreamId: typing.ClassVar[BitProperty]
    SubType: typing.ClassVar[BitProperty]
    SymLink: typing.ClassVar[BitProperty]
    TailSize: typing.ClassVar[BitProperty]
    TimeType: typing.ClassVar[BitProperty]
    TotalPhySize: typing.ClassVar[BitProperty]
    TotalSize: typing.ClassVar[BitProperty]
    Type: typing.ClassVar[BitProperty]
    UnpackSize: typing.ClassVar[BitProperty]
    UnpackVer: typing.ClassVar[BitProperty]
    User: typing.ClassVar[BitProperty]
    Va: typing.ClassVar[BitProperty]
    VirtualSize: typing.ClassVar[BitProperty]
    Volume: typing.ClassVar[BitProperty]
    VolumeIndex: typing.ClassVar[BitProperty]
    VolumeName: typing.ClassVar[BitProperty]
    Warning: typing.ClassVar[BitProperty]
    WarningFlags: typing.ClassVar[BitProperty]
    ZerosTailIsAllowed: typing.ClassVar[BitProperty]
    __members__: typing.ClassVar[dict[str, BitProperty]]
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

class BitPropVariantType:
    """
    The BitPropVariantType enum represents the possible types that a BitPropVariant can store.

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

    Bool: typing.ClassVar[BitPropVariantType]
    Empty: typing.ClassVar[BitPropVariantType]
    FileTime: typing.ClassVar[BitPropVariantType]
    Int16: typing.ClassVar[BitPropVariantType]
    Int32: typing.ClassVar[BitPropVariantType]
    Int64: typing.ClassVar[BitPropVariantType]
    Int8: typing.ClassVar[BitPropVariantType]
    String: typing.ClassVar[BitPropVariantType]
    UInt16: typing.ClassVar[BitPropVariantType]
    UInt32: typing.ClassVar[BitPropVariantType]
    UInt64: typing.ClassVar[BitPropVariantType]
    UInt8: typing.ClassVar[BitPropVariantType]
    __members__: typing.ClassVar[dict[str, BitPropVariantType]]
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

class BitPropVariant:
    """
    The BitPropVariant struct is a light extension to the WinAPI PROPVARIANT struct providing useful getters.
    """
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, value: bool) -> None: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    def clear(self) -> None:
        """
        Clears the variant.
        """
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
    def type(self) -> BitPropVariantType:
        """
        Returns the type of the variant.
        """

class BitGenericItem:
    """
    The BitGenericItem interface class represents a generic item (either inside or outside an archive).
    """
    def attributes(self) -> int:
        """
        the item attributes.
        """
    def is_dir(self) -> bool:
        """
        true if and only if the item is a directory (i.e., it has the property BitProperty::IsDir)
        """
    def name(self) -> str:
        """
        the name of the item, if available or inferable from the path, or an empty string otherwise.
        """
    def path(self) -> str:
        """
        the path of the item.
        """
    def size(self) -> int:
        """
        the uncompressed size of the item.
        """

class BitArchiveItem(BitGenericItem):
    """
    The BitArchiveItem class represents a generic item inside an archive.
    """
    def attributes(self) -> int:
        """
        the item attributes.
        """
    def crc(self) -> int:
        """
        the CRC of the item.
        """
    def creation_time(self) -> datetime.datetime: ...
    def extension(self) -> str:
        """
        the extension of the item, if available or if it can be inferred from the name; otherwise it returns an empty string (e.g., when the item is a folder).
        """
    def index(self) -> int:
        """
        the index of the item in the archive.
        """
    def is_encrypted(self) -> bool:
        """
        true if and only if the item is encrypted.
        """
    def last_access_time(self) -> datetime.datetime: ...
    def last_write_time(self) -> datetime.datetime: ...
    def native_path(self) -> str:
        """
        the path of the item in the archive, if available or inferable from the name, or an empty string otherwise.
        """
    def pack_size(self) -> int:
        """
        the compressed size of the item.
        """

class BitArchiveItemOffset(BitArchiveItem):
    """
    The BitArchiveItemOffset class represents an archived item but doesn't store its properties.
    """
    def __eq__(self, other: typing.Any) -> bool: ...
    def __hash__(self) -> int: ...
    def __iadd__(self, arg0: int) -> BitArchiveItemOffset: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def item_property(self, arg0: BitProperty) -> BitPropVariant:
        """
        Gets the specified item property.

        Args:
            property_id (bit7z::BitProperty): The ID of the property to get.

        Returns:
            BitPropVariant: the value of the item property, if available, or an empty BitPropVariant.
        """

class BitArchiveItemInfo(BitArchiveItem):
    """
    The BitArchiveItemInfo class represents an archived item and that stores all its properties for later use.
    """
    def item_properties(self) -> dict[BitProperty, BitPropVariant]:
        """
        a map of all the available (i.e., non-empty) item properties and their respective values.
        """
    def item_property(self, arg0: BitProperty) -> BitPropVariant:
        """
        Gets the specified item property.

        Args:
            property_id (bit7z::BitProperty): The ID of the property to get.

        Returns:
            BitPropVariant: the value of the item property, if available, or an empty BitPropVariant.
        """

class OverwriteMode:
    """
    Enumeration representing how a handler should deal when an output file already exists.

    Members:

      Nothing : The handler will throw an exception if the output file or buffer already exists.

      Overwrite : The handler will overwrite the old file or buffer with the new one.

      Skip : The handler will skip writing to the output file or buffer.
    """

    Nothing: typing.ClassVar[OverwriteMode]
    Overwrite: typing.ClassVar[OverwriteMode]
    Skip: typing.ClassVar[OverwriteMode]
    __members__: typing.ClassVar[dict[str, OverwriteMode]]
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

class BitAbstractArchiveHandler:
    """
    Abstract class representing a generic archive handler.
    """
    def clear_password(self) -> None:
        """
        Clear the current password used by the handler.

        Calling clear_password() will disable the encryption/decryption of archives.

        Note:
            This is equivalent to calling set_password("").
        """
    def file_callback(self) -> typing.Callable[[str], None]:
        """
        the current file callback.
        """
    def format(self) -> BitInFormat:
        """
        the format used by the handler for extracting or compressing.
        """
    def is_password_defined(self) -> bool:
        """
        a boolean value indicating whether a password is defined or not.
        """
    def overwrite_mode(self) -> OverwriteMode:
        """
        the overwrite mode.
        """
    def password(self) -> str:
        """
        the password used to open, extract, or encrypt the archive.
        """
    def password_callback(self) -> typing.Callable[[], str]:
        """
        the current password callback.
        """
    def progress_callback(self) -> typing.Callable[[int], bool]:
        """
        the current progress callback.
        """
    def ratio_callback(self) -> typing.Callable[[int, int], None]:
        """
        the current ratio callback.
        """
    def retainDirectories(self) -> bool:
        """
        a boolean value indicating whether the directory structure must be preserved while extracting or compressing the archive.
        """
    def set_file_callback(self, callback: typing.Callable[[str], None]) -> None:
        """
        Sets the function to be called when the current file being processed changes.

        Args:
            callback: the file callback to be used.
        """
    def set_overwrite_mode(self, mode: OverwriteMode) -> None:
        """
        Sets how the handler should behave when it tries to output to an existing file or buffer.
        Args:
            mode: the OverwriteMode to be used by the handler.
        """
    def set_password(self, password: str) -> None:
        """
        Sets up a password to be used by the archive handler.

        The password will be used to encrypt/decrypt archives by using the default cryptographic method of the archive format.

        Args:
            password: the password to be used.

        Note:
            Calling this set_password when the input archive is not encrypted does not have any effect on the extraction process.
            Calling this set_password when the output format doesn't support archive encryption (e.g., GZip, BZip2, etc...) does not have any effects (in other words, it doesn't throw exceptions, and it has no effects on compression operations).
            After a password has been set, it will be used for every subsequent operation. To disable the use of the password, you need to call the clear_password method, which is equivalent to calling set_password(L"").
        """
    def set_password_callback(self, callback: typing.Callable[[], str]) -> None:
        """
        Sets the function to be called when a password is needed to complete the ongoing operation.

        Args:
            callback: the password callback to be used.
        """
    def set_progress_callback(self, callback: typing.Callable[[int], bool]) -> None:
        """
        Sets the function to be called when the processed size of the ongoing operation is updated.

        Args:
            callback: the progress callback to be used.
        Note:
            The completion percentage of the current operation can be obtained by calculating int((100.0 * processed_size) / total_size).
        """
    def set_ratio_callback(self, callback: typing.Callable[[int, int], None]) -> None:
        """
        Sets the function to be called when the input processed size and current output size of the ongoing operation are known.

        Args:
            callback: the ratio callback to be used.
        Note:
            The ratio percentage of a compression operation can be obtained by calculating int((100.0 * output_size) / input_size).
        """
    def set_retain_directories(self, retain: bool) -> None:
        """
        Sets whether the operations' output will preserve the input's directory structure or not.

        Args:
            retain: the setting for preserving or not the input directory structure
        """
    def set_total_callback(self, callback: typing.Callable[[int], None]) -> None:
        """
        Sets the function to be called when the total size of an operation is available.

        Args:
            callback: the total callback to be used.
        """
    def total_callback(self) -> typing.Callable[[int], None]:
        """
        the current total callback.
        """

class BitAbstractArchiveOpener(BitAbstractArchiveHandler):
    def extraction_format(self) -> BitInFormat:
        """
        the archive format used by the archive opener.
        """

class UpdateMode:
    """
    Members:

      Nothing

      Append

      Update
    """

    Append: typing.ClassVar[UpdateMode]
    Nothing: typing.ClassVar[UpdateMode]
    Update: typing.ClassVar[UpdateMode]
    __members__: typing.ClassVar[dict[str, UpdateMode]]
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

class EncryptionScope:
    """
    Members:

      DataOnly : Only the archive's file data is encrypted.

      DataAndHeaders : Both the archive's file data and headers are encrypted (valid only for the 7z format).
    """

    DataAndHeaders: typing.ClassVar[EncryptionScope]
    DataOnly: typing.ClassVar[EncryptionScope]
    __members__: typing.ClassVar[dict[str, EncryptionScope]]
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

class BitAbstractArchiveCreator(BitAbstractArchiveHandler):
    """
    Abstract class representing a generic archive creator.
    """
    def compression_format(self) -> BitInOutFormat:
        """
        the format used for creating/updating an archive.
        """
    def compression_method(self) -> BitCompressionMethod:
        """
        the compression method used for creating/updating an archive.
        """
    def crypt_headers(self) -> bool:
        """
        whether the creator crypts also the headers of archives or not.
        """
    def dictionary_size(self) -> int:
        """
        the dictionary size used for creating/updating an archive.
        """
    def set_compression_level(self, level: BitCompressionLevel) -> None:
        """
        Sets the compression level to be used when creating/updating an archive.

        Args:
            level: the compression level desired.
        """
    def set_compression_method(self, method: BitCompressionMethod) -> None:
        """
        Sets the compression method to be used when creating/updating an archive.

        Args:
            method: the compression method desired.
        """
    def set_dictionary_size(self, dictionary_size: int) -> None:
        """
        Sets the dictionary size to be used when creating/updating an archive.

        Args:
            dictionary_size: the dictionary size desired.
        """
    def set_format_property(self, name: str, value: BitPropVariant) -> None:
        """
        Sets a property for the output archive format as described by the 7-zip documentation(e.g., https://sevenzip.osdn.jp/chm/cmdline/switches/method.htm).

        For example, passing the string L"tm" with a false value while creating a .7z archive will disable storing the last modified timestamps of the compressed files.

        Args:
            name: the name of the property to be set.
            value: the value to be used for the property.
        """
    @typing.overload
    def set_password(self, password: str) -> None:
        """
        Sets up a password for the output archives.

        When setting a password, the produced archives will be encrypted using the default cryptographic method of the output format. The option "crypt headers" remains unchanged, in contrast with what happens when calling the set_password(tstring, bool) method.

        Args:
            password: the password to be used when creating/updating archives.

        Note:
            Calling set_password when the output format doesn't support archive encryption (e.g., GZip, BZip2, etc...) does not have any effects (in other words, it doesn't throw exceptions, and it has no effects on compression operations).
            After a password has been set, it will be used for every subsequent operation. To disable the use of the password, you need to call the clearPassword method (inherited from BitAbstractArchiveHandler), which is equivalent to set_password("").
        """
    @typing.overload
    def set_password(self, password: str, scope: EncryptionScope) -> None:
        """
        Sets up a password for the output archive.

        When setting a password, the produced archive will be encrypted using the default cryptographic method of the output format. If the format is 7z, and the option "cryptHeaders" is set to true, the headers of the archive will be encrypted, resulting in a password request every time the output file will be opened.

        Args:
            password: the password to be used when creating/updating archives.
            scope: the scope of encryption; use EncryptionScope::DataAndHeaders to also encrypt the archive headers (valid only for the 7z format).

        Note:
            Calling set_password when the output format doesn't support archive encryption (e.g., GZip, BZip2, etc...) does not have any effects (in other words, it doesn't throw exceptions, and it has no effects on compression operations).
            Calling set_password with "cryptHeaders" set to true does not have effects on formats different from 7z.
            After a password has been set, it will be used for every subsequent operation. To disable the use of the password, you need to call the clearPassword method (inherited from BitAbstractArchiveHandler), which is equivalent to set_password("").
        """
    def set_solid_mode(self, solid_mode: bool) -> None:
        """
        Sets whether the archive creator uses solid compression or not.

        Args:
            solid_mode: the solid mode desired.
        Note:
            Setting the solid compression mode to true has effect only when using the 7z format with multiple input files.
        """
    def set_store_creation_time(self, store_creation_time: bool) -> None:
        """
        Sets whether the creator will store creation timestamps of items.

        Args:
            store_creation_time: if true, creation timestamps of items will be stored in the output archive.
        """
    def set_store_last_access_time(self, store_last_access_time: bool) -> None:
        """
        Sets whether the creator will store last access timestamps of items.

        Args:
            store_last_access_time: if true, last access timestamps of items will be stored in the output archive.
        """
    def set_store_last_write_time(self, store_last_write_time: bool) -> None:
        """
        Sets whether the creator will store last write timestamps of items.

        Args:
            store_last_write_time: if false, last write timestamps will be omitted from the output archive.

        By default, all archive formats store last write timestamps; pass false to suppress them.
        """
    def set_store_open_files(self, store_open_files: bool) -> None:
        """
        Sets whether the creator will attempt to compress files that are locked by other processes.
        When enabled, the creator opens files with shared read/write access on Windows, which is equivalent to 7-zip's -ssw switch. This allows compressing files that another process has open for writing.

        Warning:
            Compressing a file that is actively being written by another process may produce an incomplete or inconsistent archive entry.

        Note:
            On non-Windows platforms this setting has no effect.

        Args:
            store_open_files: if true, the creator will attempt to compress files open by other processes.
        """
    def set_store_symbolic_links(self, store_symbolic_links: bool) -> None:
        """
        Sets whether the creator will store symbolic links as links in the output archive.

        Args:
            store_symbolic_links: if true, symbolic links will be stored as links.
        """
    def set_threads_count(self, threads_count: int) -> None:
        """
        Sets the number of threads to be used when creating/updating an archive.

        Args:
            threads_count: the number of threads desired.
        """
    def set_update_mode(self, mode: UpdateMode) -> None:
        """
        Sets whether and how the creator can update existing archives or not.

        Args:
            mode: the desired update mode.

        Note:
            If set to UpdateMode::None, a subsequent compression operation may throw an exception if it targets an existing archive.
        """
    def set_volume_size(self, volume_size: int) -> None:
        """
        Sets the volumeSize (in bytes) of the output archive volumes.

        Args:
            volume_size: The dimension of a volume.

        Note:
            This setting has effects only when the destination archive is on the filesystem.
        """
    def set_word_size(self, word_size: int) -> None:
        """
        Sets the word size to be used when creating/updating an archive.

        Args:
            word_size: the word size desired.
        """
    def solid_mode(self) -> bool:
        """
        whether the archive creator uses solid compression or not.
        """
    def store_creation_time(self) -> bool:
        """
        true if the creator has been explicitly configured to store creation timestamps of items.
        """
    def store_last_access_time(self) -> bool:
        """
        true if the creator has been explicitly configured to store last access timestamps of items.
        """
    def store_last_write_time(self) -> bool:
        """
        true if the creator has been explicitly configured to store last write timestamps of items.
        """
    def store_open_files(self) -> bool:
        """
        whether the creator will attempt to compress files that are locked by other processes.
        """
    def store_symbolic_links(self) -> bool:
        """
        whether the archive creator stores symbolic links as links in the output archive.
        """
    def threads_count(self) -> int:
        """
        the number of threads used when creating/updating an archive (a 0 value means that it will use the 7-zip default value).
        """
    def update_mode(self) -> UpdateMode:
        """
        the update mode used when updating existing archives.
        """
    def volume_size(self) -> int:
        """
        the volume size (in bytes) used when creating multi-volume archives (a 0 value means that all files are going in a single archive).
        """
    def word_size(self) -> int:
        """
        the word size used for creating/updating an archive.
        """

class FilterPolicy:
    """
    Members:

      Include : Extract/compress the items that match the pattern.

      Exclude : Do not extract/compress the items that match the pattern.
    """

    Exclude: typing.ClassVar[FilterPolicy]
    Include: typing.ClassVar[FilterPolicy]
    __members__: typing.ClassVar[dict[str, FilterPolicy]]
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

class FolderPathPolicy:
    """
    Members:

      Strip : Remove the folder path from the extracted path.

      KeepName : Preserve the folder name in the extracted path.

      KeepPath : Preserve the full folder path in the extracted path.
    """

    KeepName: typing.ClassVar[FolderPathPolicy]
    KeepPath: typing.ClassVar[FolderPathPolicy]
    Strip: typing.ClassVar[FolderPathPolicy]
    __members__: typing.ClassVar[dict[str, FolderPathPolicy]]
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

class FilterResult:
    """
    Members:

      ProcessItem : Continue processing the item.

      SkipItem : Skip the item (do not process it).

      AbortOperation : Abort the whole operation.
    """

    AbortOperation: typing.ClassVar[FilterResult]
    ProcessItem: typing.ClassVar[FilterResult]
    SkipItem: typing.ClassVar[FilterResult]
    __members__: typing.ClassVar[dict[str, FilterResult]]
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

class BitInputArchive:
    def archive_path(self) -> str:
        """
        the path to the archive (the empty string for buffer/stream archives).
        """
    def archive_property(self, arg0: BitProperty) -> BitPropVariant:
        """
        Gets the specified archive property.

        Args:
            property: the property to be retrieved.

        Returns:
            the current value of the archive property or an empty BitPropVariant if no value is specified.
        """
    def contains(self, path: str) -> bool:
        """
        Find if there is an item in the archive that has the given path.

        Args:
            path: the path of the file or folder to be checked.

        Returns:
            true if and only if the archive contains the specified file or folder.
        """
    def detected_format(self) -> BitInFormat:
        """
        the detected format of the file.
        """
    def extract_folder_to(
        self, out_dir: str, regex: str, policy: FolderPathPolicy = ...
    ) -> None:
        """
        Extracts a folder from the archive to the chosen directory.

        Args:
            out_dir: the output directory where the extracted files will be put.
            regex: the regex used for matching the paths of files inside the archive.
            policy: (optional) the filtering policy to be applied to the matching items.
        """
    @typing.overload
    def extract_matching_to(
        self, out_dir: str, item_filter: str, policy: FilterPolicy = ...
    ) -> None:
        """
        Extracts to the output directory all the items whose paths match the given wildcard pattern.

        Args:
            out_dir: the output directory where the extracted files will be put.
            item_filter: the wildcard pattern used for matching the paths of items inside the archive.
            policy: (optional) the filtering policy to be applied to the matching items.
        """
    @typing.overload
    def extract_matching_to(
        self, out_dir: str, regex: str, policy: FilterPolicy = ...
    ) -> None:
        """
        Extracts to the output directory all the items whose paths match the given regex pattern.

        Args:
            out_dir: the output directory where the extracted files will be put.
            regex: the regex used for matching the paths of files inside the archive.
            policy: (optional) the filtering policy to be applied to the matching items.
        """
    def extract_root_folder_content_to(self, out_dir: str) -> None:
        """
        Extracts the content of the archive's root folder to the chosen directory.
        Note:
            The archive's root folder is the single top-level folder shared by all the items in the archive; its name is stripped from the extracted items' paths.
            If the archive does not have a single root folder, a BitException is thrown.

        Args:
            out_dir: the output directory where the root folder's content will be put.
        """
    @typing.overload
    def extract_to(self, out_dir: str, indices: list[int] = []) -> None:
        """
        Extracts the specified items to the chosen directory.

        Args:
            out_dir: the output directory where the extracted files will be put.
            indices: (optional) the indices of the files in the archive that must be extracted.
        """
    @typing.overload
    def extract_to(
        self,
        out_dir: str,
        filter_callback: typing.Callable[[BitArchiveItem], FilterResult],
    ) -> None:
        """
        Extracts to the output directory all the items that satisfy the given filtering criteria.

        Args:
            out_dir: the output directory where the extracted files will be put.
            filter_callback: the filtering callback that specifies whether to extract an item or not.
        """
    @typing.overload
    def extract_to(
        self, out_dir: str, rename_callback: typing.Callable[[BitArchiveItem], str]
    ) -> None:
        """
        Extracts the archive to the chosen directory, specifying the names of the extracted items via a RenameCallback.
        Note:
            The callback receives the archive item being extracted and must return the path that the extracted item must have on the filesystem.
            If the path of the item must not change, simply return the item's path in the callback.
            If the item must not be extracted, return an empty string in the callback.

        Args:
            out_dir: the output directory where the extracted files will be put.
            rename_callback: the callback that returns the names for the extracted files.
        """
    @typing.overload
    def extract_to(self, index: int) -> bytes:
        """
        Extracts a file to the output buffer.

        Args:
            index: the index of the file to be extracted.
        """
    @typing.overload
    def extract_to(self) -> dict[str, bytes]:
        """
        Extracts the content of the archive to a map of memory buffers, where the keys are the paths of the files (inside the archive), and the values are their decompressed contents.
        """
    def is_item_encrypted(self, index: int) -> bool:
        """
        Whether the item at the given index is encrypted.

        Args:
            index: the index of an item in the archive.

        Returns:
            true if and only if the item at the given index is encrypted.
        """
    def is_item_folder(self, index: int) -> bool:
        """
        Whether the item at the given index is a folder.
        Args:
            index: the index of an item in the archive.

        Returns:
            true if and only if the item at the given index is a folder.
        """
    def item_at(self, index: int) -> BitArchiveItemOffset:
        """
        Retrieve the item at the given index.

        Args:
            index: the index of the item to be retrieved.

        Returns:
            the item at the given index within the archive.
        """
    def item_property(self, index: int, property: BitProperty) -> BitPropVariant:
        """
        Gets the specified item property.

        Args:
            index: the index of the item to retrieve the property from.
            property: the property to be retrieved.

        Returns:
            the current value of the item property or an empty BitPropVariant if no value is specified.
        """
    def items_count(self) -> int:
        """
        the number of items in the archive.
        """
    def test(self, indices: list[int] = []) -> None:
        """
        Tests the archive without extracting its content.

        Throws:
            BitException: if the archive is not valid.

        Args:
            indices: (optional) the indices of the items to be tested.
        """
    def test_item(self, index: int) -> None:
        """
        Tests the item at the given index inside the archive without extracting it.

        If the archive is not valid, or there's no item at the given index, a BitException is thrown!
        """
    def use_format_property(self, name: str, property: BitPropVariant) -> None:
        """
        Use the given format property to read the archive. See <https://github.com/rikyoz/bit7z/issues/248> for more information.

        Args:
            name: the name of the property.
            property: the property value.
        """

class BitOutputArchive:
    def add_directory(self, in_dir: str) -> None:
        """
        Adds the given directory path and all its content.

        Args:
            in_dir: the path of the directory to be added to the archive.
        """
    @typing.overload
    def add_directory_contents(self, in_dir: str, filter: str, recursive: bool) -> None:
        """
        Adds the contents of the given directory path.

        This function iterates through the specified directory and adds its contents based on the provided wildcard filter. Optionally, the operation can be recursive, meaning it will include subdirectories and their contents.

        Args:
            in_dir: the directory where to search for files to be added to the output archive.
            filter: the wildcard filter to be used for searching the files.
            recursive: recursively search the files in the given directory and all of its subdirectories.
        """
    @typing.overload
    def add_directory_contents(
        self,
        in_dir: str,
        filter: str = "*",
        policy: FilterPolicy = ...,
        recursive: bool = True,
    ) -> None:
        """
        Adds the contents of the given directory path.

        This function iterates through the specified directory and adds its contents based on the provided wildcard filter and policy. Optionally, the operation can be recursive, meaning it will include subdirectories and their contents.

        Args:
            in_dir: the directory where to search for files to be added to the output archive.
            filter: the wildcard filter to be used for searching the files.
            recursive: recursively search the files in the given directory and all of its subdirectories.
            policy: the filtering policy to be applied to the matched items. Default is FilterPolicy.Include.
        """
    def add_file(self, input: bytes, name: str) -> None:
        """
        Adds the given memory buffer, with an optional user-defined path to be used in the output archive.

        Args:
            input: the memory buffer to be added to the output archive.
            name: user-defined path to be used inside the output archive.
        """
    @typing.overload
    def add_files(self, in_files: list[str]) -> None:
        """
        Adds all the files in the given vector of filesystem paths.

        Args:
            in_files: the paths to be added to the archive.
        Note:
            Paths to directories are ignored.
        """
    @typing.overload
    def add_files(self, in_dir: str, filter: str, recursive: bool) -> None:
        """
        Adds all the files inside the given directory path that match the given wildcard filter.

        Args:
            in_dir: the directory where to search for files to be added to the output archive.
            filter: (optional) the filter pattern to be used to select the files to be added.
            recursive: (optional) if true, the directory will be searched recursively.
        Note:
            If a file path is given, a BitException is thrown.
        """
    @typing.overload
    def add_files(
        self,
        in_dir: str,
        filter: str = "*",
        policy: FilterPolicy = ...,
        recursive: bool = True,
    ) -> None:
        """
        Adds all the files inside the given directory path that match the given wildcard filter, with the specified filter policy.

        Args:
            in_dir: the directory where to search for files to be added to the output archive.
            filter: (optional) the wildcard filter to be used for searching the files.
            recursive: (optional) recursively search the files in the given directory and all of its subdirectories.
            policy: (optional) the filtering policy to be applied to the matched items. Default is FilterPolicy.Include.
        """
    @typing.overload
    def add_items(self, paths: list[str]) -> None:
        """
        Adds all the items that can be found by indexing the given vector of filesystem paths.

        Args:
            paths: the paths to be added to the archive.
        """
    @typing.overload
    def add_items(self, files: dict[str, str]) -> None:
        """
        Adds all the items that can be found by indexing the keys of the given map of filesystem paths; the corresponding mapped values are the user-defined paths wanted inside the output archive.

        Args:
            files: the map of file paths and their contents to be added to the archive.
        """
    @typing.overload
    def compress_to(self, out_file: str) -> None:
        """
        Compresses all the items added to this object to the specified archive file path.

        Args:
            out_file: the output archive file path.

        Note:
            If this object was created by passing an input archive file path, and this latter is the same as the out_file path parameter, the file will be updated.
        """
    @typing.overload
    def compress_to(self) -> bytes:
        """
        Compresses all the items added to this object to the specified buffer.
        """
    def items_count(self) -> int:
        """
        the number of items in the archive.
        """

class BitArchiveReader(BitAbstractArchiveOpener, BitInputArchive):
    @staticmethod
    @typing.overload
    def is_header_encrypted(
        library: Bit7zLibrary, in_archive: str, format: BitInFormat = ...
    ) -> bool:
        """
        Checks if the given archive is header-encrypted or not.

        Args:
            library: the library used for decompression.
            in_archive: the path to the archive to be checked.
            format: the format of the input archive. Default is FormatAuto.
        """
    @staticmethod
    @typing.overload
    def is_header_encrypted(
        library: Bit7zLibrary, in_archive: bytes, format: BitInFormat = ...
    ) -> bool:
        """
        Checks if the given memory buffer archive is header-encrypted or not.

        Args:
            library: the library used for decompression.
            in_archive: the input buffer containing the archive to be checked.
            format: the format of the input archive. Default is FormatAuto.
        """
    @typing.overload
    def __init__(
        self,
        library: Bit7zLibrary,
        in_archive: str,
        format: BitInFormat = ...,
        password: str = "",
    ) -> None:
        """
        Constructs a BitArchiveReader object, opening the input file archive.

        Args:
            library: the library used for decompression.
            in_archive: the path to the archive to be read.
            format: the format of the input archive. Default is FormatAuto.
            password: the password needed for opening the input archive.
        """
    @typing.overload
    def __init__(
        self,
        library: Bit7zLibrary,
        in_archive: bytes,
        format: BitInFormat = ...,
        password: str = "",
    ) -> None:
        """
        Constructs a BitArchiveReader object, opening the input memory buffer archive.

        Args:
            library: the library used for decompression.
            in_archive: the input buffer containing the archive to be read.
            format: the format of the input archive. Default is FormatAuto.
            password: the password needed for opening the input archive.
        """
    def archive_properties(self) -> dict[BitProperty, BitPropVariant]:
        """
        a map of all the available (i.e., non-empty) archive properties and their respective values.
        """
    def files_count(self) -> int:
        """
        the number of files in the archive.
        """
    def folders_count(self) -> int:
        """
        the number of folders in the archive.
        """
    def has_encrypted_items(self) -> bool:
        """
        true if and only if the archive has at least one encrypted item.
        """
    def is_encrypted(self) -> bool:
        """
        true if and only if the archive has only encrypted items.
        """
    def is_multi_volume(self) -> bool:
        """
        true if and only if the archive is composed by multiple volumes.
        """
    def is_solid(self) -> bool:
        """
        true if and only if the archive was created using solid compression.
        """
    def items(self) -> list[BitArchiveItemInfo]:
        """
        the list of all the archive items as BitArchiveItem objects.
        """
    def pack_size(self) -> int:
        """
        the total compressed size of the archive content.
        """
    def size(self) -> int:
        """
        the total uncompressed size of the archive content.
        """
    def volumes_count(self) -> int:
        """
        the number of volumes in the archive.
        """

class BitArchiveWriter(BitAbstractArchiveCreator, BitOutputArchive):
    @typing.overload
    def __init__(self, library: Bit7zLibrary, format: BitInOutFormat) -> None:
        """
        Constructs an empty BitArchiveWriter object that can write archives of the specified format.
        """
    @typing.overload
    def __init__(
        self,
        library: Bit7zLibrary,
        in_archive: str,
        format: BitInOutFormat,
        password: str = "",
    ) -> None:
        """
        Constructs a BitArchiveWriter object, reading the given archive file path.
        """
    @typing.overload
    def __init__(
        self,
        library: Bit7zLibrary,
        in_archive: bytes,
        format: BitInOutFormat,
        password: str = "",
    ) -> None:
        """
        Constructs a BitArchiveWriter object, reading the given memory buffer archive.
        """

class BitStringExtractor(BitAbstractArchiveOpener):
    def __init__(self, library: Bit7zLibrary, format: BitInFormat) -> None:
        """
        Constructs a BitStringExtractor object, opening the input archive.
        """
    @typing.overload
    def extract(self, in_archive: str, out_dir: str) -> None:
        """
        Extracts the given archive to the chosen directory.
        """
    @typing.overload
    def extract(self, in_archive: str, index: int) -> bytes:
        """
        Extracts the specified item from the given archive to a memory buffer.
        """
    @typing.overload
    def extract(self, in_archive: str) -> dict[str, bytes]:
        """
        Extracts all the items from the given archive to a dictionary of memory buffers.
        """
    def extract_items(
        self, in_archive: str, indices: list[int], out_dir: str = ""
    ) -> None:
        """
        Extracts the specified items from the given archive to the chosen directory.

        Args:
            in_archive: the input archive to extract from.
            indices: the indices of the files in the archive that should be extracted.
            out_dir: the output directory where the extracted files will be placed.
        """
    @typing.overload
    def extract_matching(
        self,
        in_archive: str,
        pattern: str,
        out_dir: str = "",
        policy: FilterPolicy = ...,
    ) -> None:
        """
        Extracts the files in the archive that match the given wildcard pattern to the chosen directory.
        Args:
            in_archive: the input archive to be extracted.
            pattern: the wildcard pattern to be used for matching the files.
            out_dir: the directory where to extract the matching files.
            policy: the filtering policy to be applied to the matched items. Default is FilterPolicy.Include.
        """
    @typing.overload
    def extract_matching(
        self, in_archive: str, pattern: str, policy: FilterPolicy = ...
    ) -> bytes:
        """
        Extracts to the output buffer the first file in the archive matching the given wildcard pattern.

        Args:
            in_archive: the input archive to extract from.
            pattern: the wildcard pattern to be used for matching the files.
            policy: the filtering policy to be applied to the matched items. Default is FilterPolicy.Include.
        """
    @typing.overload
    def extract_matching_regex(
        self, in_archive: str, regex: str, out_dir: str, policy: FilterPolicy = ...
    ) -> None:
        """
        Extracts the files in the archive that match the given regex pattern to the chosen directory.

        Args:
            in_archive: the input archive to extract from.
            regex: the regex pattern to be used for matching the files.
            out_dir: the output directory where the extracted files will be placed.
            policy: the filtering policy to be applied to the matched items. Default is FilterPolicy.Include.
        """
    @typing.overload
    def extract_matching_regex(
        self, in_archive: str, regex: str, policy: FilterPolicy = ...
    ) -> bytes:
        """
        Extracts to the output buffer the first file in the archive matching the given regex pattern.

        Args:
            in_archive: the input archive to extract from.
            regex: the regex pattern to be used for matching the files.
            policy: the filtering policy to be applied to the matched items. Default is FilterPolicy.Include.
        """

class BitMemExtractor(BitAbstractArchiveOpener):
    def __init__(self, library: Bit7zLibrary, format: BitInFormat) -> None:
        """
        Constructs a BitMemExtractor object, opening the input archive.
        """
    @typing.overload
    def extract(self, in_archive: bytes, out_dir: str) -> None:
        """
        Extracts the given archive to the chosen directory.

        Args:
            in_archive: the input archive to be extracted.
            out_dir: the directory where to extract the files.
        """
    @typing.overload
    def extract(self, in_archive: bytes, index: int) -> bytes:
        """
        Extracts the specified item from the given archive to a memory buffer.
        """
    @typing.overload
    def extract(self, in_archive: bytes) -> dict[str, bytes]:
        """
        Extracts all the items from the given archive to a dictionary of memory buffers.
        """
    def extract_items(
        self, in_archive: bytes, indices: list[int], out_dir: str = ""
    ) -> None:
        """
        Extracts the specified items from the given archive to the chosen directory.

        Args:
            in_archive: the input archive to extract from.
            indices: the indices of the files in the archive that should be extracted.
            out_dir: the output directory where the extracted files will be placed.
        """
    @typing.overload
    def extract_matching(
        self,
        in_archive: bytes,
        pattern: str,
        out_dir: str = "",
        policy: FilterPolicy = ...,
    ) -> None:
        """
        Extracts the files in the archive that match the given wildcard pattern to the chosen directory.

        Args:
            in_archive: the input archive to be extracted.
            pattern: the wildcard pattern to be used for matching the files.
            out_dir: the directory where to extract the matching files.
            policy: the filtering policy to be applied to the matched items. Default is FilterPolicy.Include.
        """
    @typing.overload
    def extract_matching(
        self, in_archive: bytes, pattern: str, policy: FilterPolicy = ...
    ) -> bytes:
        """
        Extracts to the output buffer the first file in the archive matching the given wildcard pattern.
        Args:
            in_archive: the input archive to extract from.
            pattern: the wildcard pattern to be used for matching the files.
            policy: the filtering policy to be applied to the matched items. Default is FilterPolicy.Include.
        """
    @typing.overload
    def extract_matching_regex(
        self,
        in_archive: bytes,
        regex: str,
        out_dir: str = "",
        policy: FilterPolicy = ...,
    ) -> None:
        """
        Extracts the files in the archive that match the given regex pattern to the chosen directory.

        Args:
            in_archive: the input archive to extract from.
            regex: the regex pattern to be used for matching the files.
            out_dir: the output directory where the extracted files will be placed.
            policy: the filtering policy to be applied to the matched items. Default is FilterPolicy.Include.
        """
    @typing.overload
    def extract_matching_regex(
        self, in_archive: bytes, regex: str, policy: FilterPolicy = ...
    ) -> bytes:
        """
        Extracts to the output buffer the first file in the archive matching the given regex pattern.
        """
    def test(self, in_archive: bytes) -> None:
        """
        Tests the given archive without extracting its content.

        If the archive is not valid, a BitException is thrown!

        Args:
            in_archive: the input archive to be tested.
        """

class BitStringCompressor(BitAbstractArchiveCreator):
    def __init__(self, library: Bit7zLibrary, format: BitInOutFormat) -> None:
        """
        Constructs a BitStringCompressor object, creating a new archive.
        """
    @typing.overload
    def compress_file(self, in_file: str, out_file: str, input_name: str = "") -> None:
        """
        Compresses the given file to the chosen archive.

        Args:
            in_file: the input file to be compressed.
            out_file: the path (relative or absolute) to the output archive file.
            input_name: the name of the input file in the archive (optional).
        """
    @typing.overload
    def compress_file(self, in_file: str, input_name: str = "") -> bytes:
        """
        Compresses the given file to a memory buffer.

        Args:
            in_file: the input file to be compressed.
            input_name: the name of the input file in the archive (optional).
        """

class BitFileCompressor(BitStringCompressor):
    def __init__(self, library: Bit7zLibrary, format: BitInOutFormat) -> None:
        """
        Constructs a BitFileCompressor object, creating a new archive.
        """
    @typing.overload
    def compress(self, in_files: list[str], out_archive: str) -> None:
        """
        Compresses the given files or directories.

        The items in the first argument must be the relative or absolute paths to files or directories existing on the filesystem.

        Args:
            in_files: the input files to be compressed.
            out_archive: the path (relative or absolute) to the output archive file.
        """
    @typing.overload
    def compress(self, in_files: dict[str, str], out_archive: str) -> None:
        """
        Compresses the given files or directories using the specified aliases.

        The items in the first argument must be the relative or absolute paths to files or directories existing on the filesystem. Each pair in the map must follow the following format: {"path to file in the filesystem", "alias path in the archive"}.


        Args:
            in_files: a map of paths and corresponding aliases.
            out_archive: the path (relative or absolute) to the output archive file.
        """
    def compress_directory(self, in_dir: str, out_archive: str) -> None:
        """
        Compresses an entire directory.

        Args:
            in_dir: the path (relative or absolute) to the input directory.
            out_archive: the path (relative or absolute) to the output archive file.
        Note:
            This method is equivalent to compress_files with filter set to "".
        """
    def compress_directory_contents(
        self,
        in_dir: str,
        out_archive: str,
        recursive: bool = True,
        filter_pattern: str = "*",
    ) -> None:
        """
        Compresses the contents of a directory.

        Args:
            in_dir: the path (relative or absolute) to the input directory.
            out_archive: the path (relative or absolute) to the output archive file.
            recursive: (optional) if true, it searches files inside the sub-folders of in_dir.
            filter_pattern: the wildcard pattern to filter the files to be compressed (optional).
        Note:
            Unlike compress_files, this method includes also the metadata of the sub-folders.
        """
    @typing.overload
    def compress_files(self, in_files: list[str], out_archive: str) -> None:
        """
        Compresses a group of files.

        Args:
            in_files: the input files to be compressed.
            out_archive: the path (relative or absolute) to the output archive file.
        Note:
            Any path to a directory or to a not-existing file will be ignored!
        """
    @typing.overload
    def compress_files(
        self,
        in_dir: str,
        out_archive: str,
        recursive: bool = True,
        filter_pattern: str = "*",
    ) -> None:
        """
        Compresses all the files in the given directory.

        Args:
            in_dir: the path (relative or absolute) to the input directory.
            out_archive: the path (relative or absolute) to the output archive file.
            recursive: (optional) if true, it searches files inside the sub-folders of in_dir.
            filter_pattern: the wildcard pattern to filter the files to be compressed (optional).
        """

class BitMemCompressor(BitAbstractArchiveCreator):
    def __init__(self, library: Bit7zLibrary, format: BitInOutFormat) -> None:
        """
        Constructs a BitMemCompressor object, creating a new archive.
        """
    @typing.overload
    def compress_file(self, input: bytes, out_file: str, input_name: str = "") -> None:
        """
        Compresses the given memory buffer to the chosen archive.

        Args:
            input: the input memory buffer to be compressed.
            out_file: the path (relative or absolute) to the output archive file.
            input_name: (optional) the name to give to the compressed file inside the output archive.
        """
    @typing.overload
    def compress_file(self, input: bytes, input_name: str = "") -> bytes:
        """
        Compresses the given memory buffer to a memory buffer.

        Args:
            input: the input memory buffer to be compressed.
            input_name: (optional) the name to give to the compressed file inside the output archive.
        """

class BitArchiveEditor(BitArchiveWriter):
    def __init__(
        self,
        library: Bit7zLibrary,
        in_archive: str,
        format: BitInOutFormat,
        password: str = "",
    ) -> None:
        """
        Constructs a BitArchiveEditor object, reading the given archive file path.
        """
    def apply_changes(self) -> None:
        """
        Applies the requested changes (i.e., rename/update/delete operations) to the input archive.
        """
    @typing.overload
    def delete_item(self, index: int, policy: DeletePolicy = ...) -> None:
        """
        Marks as deleted the item at the given index.

        Args:
            index: the index of the item to be deleted.
            policy: the policy to be used when deleting items. Default to DeletePolicy.ItemOnly.

        Exceptions:
            BitException if the index is invalid.

        Note:
            By default, if the item is a folder, only its metadata is deleted, not the files within it. If instead the policy is set to DeletePolicy::RecurseDirs, then the items within the folder will also be deleted.
        """
    @typing.overload
    def delete_item(self, item_path: str, policy: DeletePolicy = ...) -> None:
        """
        Marks as deleted the archive's item(s) with the specified path.

        Args:
            item_path: the path (in the archive) of the item to be deleted.
            policy: the policy to be used when deleting items. Default to DeletePolicy.ItemOnly.

        Exceptions:
            BitException if the specified path is empty or invalid, or if no matching item could be found.

        Note:
            By default, if the marked item is a folder, only its metadata will be deleted, not the files within it. To delete the folder contents as well, set the policy to DeletePolicy::RecurseDirs.
            The specified path must not begin with a path separator.
            A path with a trailing separator will _only_ be considered if the policy is DeletePolicy::RecurseDirs, and will only match folders; with DeletePolicy::ItemOnly, no item will match a path with a trailing separator.
            Generally, archives may contain multiple items with the same paths. If this is the case, all matching items will be marked as deleted according to the specified policy.
        """
    @typing.overload
    def rename_item(self, index: int, new_path: str) -> None:
        """
        Requests to change the path of the item at the specified index with the given one.

        Args:
            index: the index of the item to be renamed.
            new_path: the new path of the item.
        """
    @typing.overload
    def rename_item(self, old_path: str, new_path: str) -> None:
        """
        Requests to change the path of the item from oldPath to the newPath.

        Args:
            old_path: the current path of the item to be renamed.
            new_path: the new path of the item.
        """
    def set_update_mode(self, update_mode: UpdateMode) -> None:
        """
        Sets how the editor performs the update of the items in the archive.

        Args:
            mode: the desired update mode (either UpdateMode::Append or UpdateMode::Overwrite).

        Note:
            BitArchiveEditor doesn't support UpdateMode::Nothing.
        """
    @typing.overload
    def update_item(self, index: int, in_file: str) -> None:
        """
        Requests to update the content of the item at the specified index with the data from the given file.

        Args:
            index: the index of the item to be updated.
            in_file: the path of the file to be used for the update.
        """
    @typing.overload
    def update_item(self, index: int, input_buffer: bytes) -> None:
        """
        Requests to update the content of the item at the specified index with the data from the given buffer.

        Args:
            index: the index of the item to be updated.
            input_buffer: the buffer containing the new data for the item.
        """
    @typing.overload
    def update_item(self, item_path: str, in_file: str) -> None:
        """
        Requests to update the content of the item at the specified path with the data from the given file.

        Args:
            item_path: the path of the item to be updated.
            in_file: the path of the file to be used for the update.
        """
    @typing.overload
    def update_item(self, item_path: str, input_buffer: bytes) -> None:
        """
        Requests to update the content of the item at the specified path with the data from the given buffer.

        Args:
            item_path: the path of the item to be updated.
            input_buffer: the buffer containing the new data for the item.
        """

def platform_lib7zip_name() -> str:
    """
    lib7zip library name for current platform.
    """

def version() -> str:
    """
    The _core plugin version.
    """

ATime: BitProperty
AbortOperation: FilterResult
AltStreamsSize: BitProperty
Attrib: BitProperty
BZip2: BitCompressionMethod
BigEndian: BitProperty
Bit64: BitProperty
Block: BitProperty
Bool: BitPropVariantType
CRC: BitProperty
CTime: BitProperty
Characters: BitProperty
Checksum: BitProperty
ClusterSize: BitProperty
CodePage: BitProperty
Comment: BitProperty
Commented: BitProperty
Copy: BitCompressionMethod
CopyLink: BitProperty
Cpu: BitProperty
CreatorApp: BitProperty
DataAndHeaders: EncryptionScope
DataOnly: EncryptionScope
Deflate: BitCompressionMethod
Deflate64: BitCompressionMethod
DictionarySize: BitProperty
EmbeddedStubSize: BitProperty
Empty: BitPropVariantType
Encrypted: BitProperty
Error: BitProperty
ErrorFlags: BitProperty
ErrorType: BitProperty
Exclude: FilterPolicy
Extension: BitProperty
Fast: BitCompressionLevel
Fastest: BitCompressionLevel
FileSystem: BitProperty
FileTime: BitPropVariantType
FormatAPM: BitInFormat
FormatArj: BitInFormat
FormatAuto: BitInFormat
FormatBZip2: BitInOutFormat
FormatCab: BitInFormat
FormatChm: BitInFormat
FormatCoff: BitInFormat
FormatCompound: BitInFormat
FormatCpio: BitInFormat
FormatCramFS: BitInFormat
FormatDeb: BitInFormat
FormatDmg: BitInFormat
FormatElf: BitInFormat
FormatExt: BitInFormat
FormatFat: BitInFormat
FormatFlv: BitInFormat
FormatGZip: BitInOutFormat
FormatGpt: BitInFormat
FormatHfs: BitInFormat
FormatHxs: BitInFormat
FormatIHex: BitInFormat
FormatIso: BitInFormat
FormatLzh: BitInFormat
FormatLzma: BitInFormat
FormatLzma86: BitInFormat
FormatMacho: BitInFormat
FormatMbr: BitInFormat
FormatMslz: BitInFormat
FormatMub: BitInFormat
FormatNsis: BitInFormat
FormatNtfs: BitInFormat
FormatPe: BitInFormat
FormatPpmd: BitInFormat
FormatQcow: BitInFormat
FormatRar: BitInFormat
FormatRar5: BitInFormat
FormatRpm: BitInFormat
FormatSevenZip: BitInOutFormat
FormatSplit: BitInFormat
FormatSquashFS: BitInFormat
FormatSwf: BitInFormat
FormatSwfc: BitInFormat
FormatTE: BitInFormat
FormatTar: BitInOutFormat
FormatUEFIc: BitInFormat
FormatUEFIs: BitInFormat
FormatUdf: BitInFormat
FormatVdi: BitInFormat
FormatVhd: BitInFormat
FormatVhdx: BitInFormat
FormatVmdk: BitInFormat
FormatWim: BitInOutFormat
FormatXar: BitInFormat
FormatXz: BitInOutFormat
FormatZ: BitInFormat
FormatZip: BitInOutFormat
FreeSpace: BitProperty
Group: BitProperty
HandlerItemIndex: BitProperty
HardLink: BitProperty
HeadersSize: BitProperty
HostOS: BitProperty
INode: BitProperty
Id: BitProperty
Include: FilterPolicy
Int16: BitPropVariantType
Int32: BitPropVariantType
Int64: BitPropVariantType
Int8: BitPropVariantType
IsAltStream: BitProperty
IsAnti: BitProperty
IsAux: BitProperty
IsDeleted: BitProperty
IsDir: BitProperty
IsNotArcType: BitProperty
IsTree: BitProperty
IsVolume: BitProperty
ItemOnly: DeletePolicy
KeepName: FolderPathPolicy
KeepPath: FolderPathPolicy
Links: BitProperty
LocalName: BitProperty
Lzma: BitCompressionMethod
Lzma2: BitCompressionMethod
MTime: BitProperty
MainSubfile: BitProperty
Max: BitCompressionLevel
Method: BitProperty
Name: BitProperty
NoProperty: BitProperty
Normal: BitCompressionLevel
Nothing: OverwriteMode
NtReparse: BitProperty
NtSecure: BitProperty
NumAltStreams: BitProperty
NumBlocks: BitProperty
NumErrors: BitProperty
NumStreams: BitProperty
NumSubDirs: BitProperty
NumSubFiles: BitProperty
NumVolumes: BitProperty
Offset: BitProperty
OutName: BitProperty
Overwrite: OverwriteMode
PackSize: BitProperty
Path: BitProperty
PhySize: BitProperty
PhySizeCantBeDetected: BitProperty
Position: BitProperty
PosixAttrib: BitProperty
Ppmd: BitCompressionMethod
Prefix: BitProperty
ProcessItem: FilterResult
Provider: BitProperty
ReadOnly: BitProperty
RecurseDirs: DeletePolicy
SectorSize: BitProperty
Sha1: BitProperty
Sha256: BitProperty
ShortComment: BitProperty
ShortName: BitProperty
Size: BitProperty
Skip: OverwriteMode
SkipItem: FilterResult
Solid: BitProperty
SplitAfter: BitProperty
SplitBefore: BitProperty
StreamId: BitProperty
String: BitPropVariantType
Strip: FolderPathPolicy
SubType: BitProperty
SymLink: BitProperty
TailSize: BitProperty
TimeType: BitProperty
TotalPhySize: BitProperty
TotalSize: BitProperty
Type: BitProperty
UInt16: BitPropVariantType
UInt32: BitPropVariantType
UInt64: BitPropVariantType
UInt8: BitPropVariantType
Ultra: BitCompressionLevel
UnpackSize: BitProperty
UnpackVer: BitProperty
User: BitProperty
Va: BitProperty
VirtualSize: BitProperty
Volume: BitProperty
VolumeIndex: BitProperty
VolumeName: BitProperty
Warning: BitProperty
WarningFlags: BitProperty
ZerosTailIsAllowed: BitProperty
BitFileExtractor = BitStringExtractor
