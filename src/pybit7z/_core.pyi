"""

Pybind11 _core plugin
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
    @typing.overload
    def set_password(self, password: str) -> None:
        """
        Sets up a password for the output archives.

        When setting a password, the produced archives will be encrypted using the default cryptographic method of the output format. The option "crypt headers" remains unchanged, in contrast with what happens when calling the set_password(tstring, bool) method.

        Args:
            password: the password to be used when creating/updating archives.

        Note:
            Calling set_password when the output format doesn't support archive encryption (e.g., GZip, BZip2, etc...) does not have any effects (in other words, it doesn't throw exceptions, and it has no effects on compression operations).
            After a password has been set, it will be used for every subsequent operation. To disable the use of the password, you need to call the clearPassword method (inherited from BitAbstractArchiveHandler), which is equivalent to set_password(L"").
        """
    @typing.overload
    def set_password(self, password: str, crypt_headers: bool) -> None:
        """
        Sets up a password for the output archive.

        When setting a password, the produced archive will be encrypted using the default cryptographic method of the output format. If the format is 7z, and the option "cryptHeaders" is set to true, the headers of the archive will be encrypted, resulting in a password request every time the output file will be opened.

        Args:
            password: the password to be used when creating/updating archives.
            crypt_headers: if true, the headers of the output archives will be encrypted (valid only when using the 7z format).

        Note:
            Calling set_password when the output format doesn't support archive encryption (e.g., GZip, BZip2, etc...) does not have any effects (in other words, it doesn't throw exceptions, and it has no effects on compression operations).
            Calling set_password with "cryptHeaders" set to true does not have effects on formats different from 7z.
            After a password has been set, it will be used for every subsequent operation. To disable the use of the password, you need to call the clearPassword method (inherited from BitAbstractArchiveHandler), which is equivalent to set_password(L"").
        """
    def set_solid_mode(self, solid_mode: bool) -> None:
        """
        Sets whether the archive creator uses solid compression or not.

        Args:
            solid_mode: the solid mode desired.
        Note:
            Setting the solid compression mode to true has effect only when using the 7z format with multiple input files.
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

class BitAbstractArchiveHandler:
    """
    Abstract class representing a generic archive handler.
    """
    def clear_password(self) -> None:
        """
        Clear the current password used by the handler.

        Calling clear_password() will disable the encryption/decryption of archives.

        Note:
            This is equivalent to calling set_password(L"").
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
            Calling this method when the input archive is not encrypted does not have any effect on the extraction process.
            Calling this method when the output format doesn't support archive encryption (e.g., GZip, BZip2, etc...) does not have any effects (in other words, it doesn't throw exceptions, and it has no effects on compression operations).
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

class BitArchiveEditor(BitArchiveWriter):
    def __init__(
        self, in_archive: str, format: BitInOutFormat, password: str = ""
    ) -> None:
        """
        Constructs a BitArchiveEditor object, reading the given archive file path.
        """
    def apply_changes(self) -> None:
        """
        Applies the requested changes (i.e., rename/update/delete operations) to the input archive.
        """
    @typing.overload
    def delete_item(self, index: int, policy: DeletePolicy) -> None:
        """
        Marks as deleted the item at the given index.

        Args:
            index: the index of the item to be deleted.
            policy: the policy to be used when deleting items.

        Exceptions:
            BitException if the index is invalid.

        Note:
            By default, if the item is a folder, only its metadata is deleted, not the files within it. If instead the policy is set to DeletePolicy::RecurseDirs, then the items within the folder will also be deleted.
        """
    @typing.overload
    def delete_item(self, item_path: str, policy: DeletePolicy) -> None:
        """
        Marks as deleted the archive's item(s) with the specified path.

        Args:
            item_path: the path (in the archive) of the item to be deleted.
            policy: the policy to be used when deleting items.

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
    def update_item(self, index: int, in_buffer: bytes) -> None:
        """
        Requests to update the content of the item at the specified index with the data from the given buffer.

        Args:
            index: the index of the item to be updated.
            in_buffer: the buffer containing the new data for the item.
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
    def update_item(self, item_path: str, in_buffer: bytes) -> None:
        """
        Requests to update the content of the item at the specified path with the data from the given buffer.

        Args:
            item_path: the path of the item to be updated.
            in_buffer: the buffer containing the new data for the item.
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

class BitArchiveReader(BitAbstractArchiveOpener, BitInputArchive):
    @staticmethod
    @typing.overload
    def is_header_encrypted(in_archive: str, format: BitInFormat) -> bool:
        """
        Checks if the given archive is header-encrypted or not.
        """
    @staticmethod
    @typing.overload
    def is_header_encrypted(in_archive: bytes, format: BitInFormat) -> bool:
        """
        Checks if the given memory buffer archive is header-encrypted or not.
        """
    @typing.overload
    def __init__(
        self, in_archive: str, format: BitInFormat, password: str = ""
    ) -> None:
        """
        Constructs a BitArchiveReader object, opening the input file archive.

        Args:
            in_archive: the path to the archive to be read.
            format: the format of the input archive.
            password: the password needed for opening the input archive.
        """
    @typing.overload
    def __init__(
        self, in_archive: bytes, format: BitInFormat, password: str = ""
    ) -> None:
        """
        Constructs a BitArchiveReader object, opening the input memory buffer archive.

        Args:
            in_archive: the input buffer containing the archive to be read.
            format: the format of the input archive.
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
    def __init__(self, format: BitInOutFormat) -> None:
        """
        Constructs an empty BitArchiveWriter object that can write archives of the specified format.
        """
    @typing.overload
    def __init__(
        self, in_archive: str, format: BitInOutFormat, password: str = ""
    ) -> None:
        """
        Constructs a BitArchiveWriter object, reading the given archive file path.
        """
    @typing.overload
    def __init__(
        self, in_archive: bytes, format: BitInOutFormat, password: str = ""
    ) -> None:
        """
        Constructs a BitArchiveWriter object, reading the given memory buffer archive.
        """

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

    Fast: typing.ClassVar[BitCompressionLevel]  # value = <BitCompressionLevel.Fast: 3>
    Fastest: typing.ClassVar[
        BitCompressionLevel
    ]  # value = <BitCompressionLevel.Fastest: 1>
    Max: typing.ClassVar[BitCompressionLevel]  # value = <BitCompressionLevel.Max: 7>
    Normal: typing.ClassVar[
        BitCompressionLevel
    ]  # value = <BitCompressionLevel.Normal: 5>
    Nothing: typing.ClassVar[
        BitCompressionLevel
    ]  # value = <BitCompressionLevel.Nothing: 0>
    Ultra: typing.ClassVar[
        BitCompressionLevel
    ]  # value = <BitCompressionLevel.Ultra: 9>
    __members__: typing.ClassVar[
        dict[str, BitCompressionLevel]
    ]  # value = {'Nothing': <BitCompressionLevel.Nothing: 0>, 'Fastest': <BitCompressionLevel.Fastest: 1>, 'Fast': <BitCompressionLevel.Fast: 3>, 'Normal': <BitCompressionLevel.Normal: 5>, 'Max': <BitCompressionLevel.Max: 7>, 'Ultra': <BitCompressionLevel.Ultra: 9>}
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
    def __init__(self, format: BitInOutFormat) -> None:
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
    @typing.overload
    def extract_to(self, path: str) -> None:
        """
        Extracts the archive to the chosen directory.

        Args:
            outDir: the output directory where the extracted files will be put.
        """
    @typing.overload
    def extract_to(self, out_dir: str, indices: list[int]) -> None:
        """
        Extracts the specified items to the chosen directory.

        Args:
            out_dir: the output directory where the extracted files will be put.
            indices: the array of indices of the files in the archive that must be extracted.
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
    def test(self) -> None:
        """
        Tests the archive without extracting its content.

        If the archive is not valid, a BitException is thrown!
        """
    def test_item(self, index: int) -> None:
        """
        Tests the item at the given index inside the archive without extracting it.

        If the archive is not valid, or there's no item at the given index, a BitException is thrown!
        """

class BitMemCompressor(BitAbstractArchiveCreator):
    def __init__(self, format: BitInOutFormat) -> None:
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

class BitMemExtractor(BitAbstractArchiveOpener):
    def __init__(self, format: BitInFormat) -> None:
        """
        Constructs a BitMemExtractor object, opening the input archive.
        """
    @typing.overload
    def extract(self, in_archive: list[int], out_dir: str = "") -> None:
        """
        Extracts the given archive to the chosen directory.
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
        self, in_archive: list[int], indices: list[int], out_dir: str = ""
    ) -> None:
        """
        Extracts the specified items from the given archive to the chosen directory.
        """
    @typing.overload
    def extract_matching(
        self,
        in_archive: list[int],
        pattern: str,
        out_dir: str,
        filter_policy: FilterPolicy,
    ) -> None:
        """
        Extracts the files in the archive that match the given wildcard pattern to the chosen directory.
        """
    @typing.overload
    def extract_matching(
        self, in_archive: bytes, pattern: bytes, filter_policy: FilterPolicy
    ) -> bytes:
        """
        Extracts to the output buffer the first file in the archive matching the given wildcard pattern.
        """
    @typing.overload
    def extract_matching_regex(
        self,
        in_archive: list[int],
        regex: str,
        out_dir: str,
        filter_policy: FilterPolicy,
    ) -> None:
        """
        Extracts the files in the archive that match the given regex pattern to the chosen directory.
        """
    @typing.overload
    def extract_matching_regex(
        self, in_archive: bytes, regex: bytes, filter_policy: FilterPolicy
    ) -> bytes:
        """
        Extracts to the output buffer the first file in the archive matching the given regex pattern.
        """
    def test(self, in_archive: list[int]) -> None:
        """
        Tests the given archive without extracting its content.

        If the archive is not valid, a BitException is thrown!

        Args:
            in_archive: the input archive to be tested.
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
        self, in_dir: str, filter: str, recursive: FilterPolicy, policy: bool
    ) -> None:
        """
        Adds the contents of the given directory path.

        This function iterates through the specified directory and adds its contents based on the provided wildcard filter and policy. Optionally, the operation can be recursive, meaning it will include subdirectories and their contents.

        Args:
            in_dir: the directory where to search for files to be added to the output archive.
            filter: the wildcard filter to be used for searching the files.
            recursive: recursively search the files in the given directory and all of its subdirectories.
            policy: the filtering policy to be applied to the matched items.
        """
    @typing.overload
    def add_file(self, in_file: str, name: str) -> None:
        """
        Adds the given file path, with an optional user-defined path to be used in the output archive.

        Args:
            in_file:  the path to the filesystem file to be added to the output archive.
            name: (optional) user-defined path to be used inside the output archive.
        Note:
            If a directory path is given, a BitException is thrown.
        """
    @typing.overload
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
        self, in_dir: str, filter: str, recursive: FilterPolicy, policy: bool
    ) -> None:
        """
        Adds all the files inside the given directory path that match the given wildcard filter, with the specified filter policy.

        Args:
            in_dir: the directory where to search for files to be added to the output archive.
            filter: (optional) the wildcard filter to be used for searching the files.
            recursive: (optional) recursively search the files in the given directory and all of its subdirectories.
            policy: (optional) the filtering policy to be applied to the matched items.
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
            If this object was created by passing an input archive file path, and this latter is the same as the outFile path parameter, the file will be updated.
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
    def __init__(self, format: BitInOutFormat) -> None:
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

class BitStringExtractor(BitAbstractArchiveOpener):
    def __init__(self, format: BitInFormat) -> None:
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
    ) -> None: ...
    @typing.overload
    def extract_matching(
        self, in_archive: str, pattern: str, out_dir: str, filter_policy: FilterPolicy
    ) -> None:
        """
        Extracts the files in the archive that match the given wildcard pattern to the chosen directory.
        """
    @typing.overload
    def extract_matching(
        self, in_archive: str, pattern: str, filter_policy: FilterPolicy
    ) -> bytes:
        """
        Extracts to the output buffer the first file in the archive matching the given wildcard pattern.
        """
    @typing.overload
    def extract_matching_regex(
        self, in_archive: str, regex: str, out_dir: str, filter_policy: FilterPolicy
    ) -> None:
        """
        Extracts the files in the archive that match the given regex pattern to the chosen directory.
        """
    @typing.overload
    def extract_matching_regex(
        self, in_archive: str, regex: str, filter_policy: FilterPolicy
    ) -> bytes:
        """
        Extracts to the output buffer the first file in the archive matching the given regex pattern.
        """
    def test(self, in_archive: str) -> None:
        """
        Tests the given archive without extracting its content.

        If the archive is not valid, a BitException is thrown!

        Args:
            in_archive: the input archive to be tested.
        """

class DeletePolicy:
    """
    Delete policy for archive items.

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

      Include : Extract/compress the items that match the pattern.

      Exclude : Do not extract/compress the items that match the pattern.
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
    Features of a format supported by bit7z

    Members:

      MultipleFiles : Archive supports multiple files.

      SolidArchive : Archive supports solid mode.

      CompressionLevel : Archive supports compression level.

      Encryption : Archive supports encryption.

      HeaderEncryption : Archive supports encrypted headers.

      MultipleMethods : Archive supports multiple compression methods.
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
    Enumeration representing how a handler should deal when an output file already exists.

    Members:

      Nothing : The handler will throw an exception if the output file or buffer already exists.

      Overwrite : The handler will overwrite the old file or buffer with the new one.

      Skip : The handler will skip writing to the output file or buffer.
    """

    Nothing: typing.ClassVar[OverwriteMode]  # value = <OverwriteMode.Nothing: 0>
    Overwrite: typing.ClassVar[OverwriteMode]  # value = <OverwriteMode.Overwrite: 1>
    Skip: typing.ClassVar[OverwriteMode]  # value = <OverwriteMode.Skip: 2>
    __members__: typing.ClassVar[
        dict[str, OverwriteMode]
    ]  # value = {'Nothing': <OverwriteMode.Nothing: 0>, 'Overwrite': <OverwriteMode.Overwrite: 1>, 'Skip': <OverwriteMode.Skip: 2>}
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

      Nothing

      Append

      Update
    """

    Append: typing.ClassVar[UpdateMode]  # value = <UpdateMode.Append: 1>
    Nothing: typing.ClassVar[UpdateMode]  # value = <UpdateMode.Nothing: 0>
    Update: typing.ClassVar[UpdateMode]  # value = <UpdateMode.Update: 2>
    __members__: typing.ClassVar[
        dict[str, UpdateMode]
    ]  # value = {'Nothing': <UpdateMode.Nothing: 0>, 'Append': <UpdateMode.Append: 1>, 'Update': <UpdateMode.Update: 2>}
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
Normal: BitCompressionLevel  # value = <BitCompressionLevel.Normal: 5>
Nothing: OverwriteMode  # value = <OverwriteMode.Nothing: 0>
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
