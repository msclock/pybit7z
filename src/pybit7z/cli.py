from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import (
    Bit7zLibrary,
    BitArchiveReader,
    BitArchiveWriter,
    BitCompressionLevel,
    BitInOutFormat,
    FormatBZip2,
    FormatGZip,
    FormatSevenZip,
    FormatTar,
    FormatWim,
    FormatXz,
    FormatZip,
    OverwriteMode,
    lib7zip_context,
)

WRITABLE_FORMATS = {
    "7z": FormatSevenZip,
    "zip": FormatZip,
    "tar": FormatTar,
    "gzip": FormatGZip,
    "bzip2": FormatBZip2,
    "xz": FormatXz,
    "wim": FormatWim,
}


def main() -> None:
    """
    Main function to parse command-line arguments and perform compression/decompression operations.
    """
    parser = argparse.ArgumentParser(
        description="pybit7z command-line compression tool"
    )
    parser.add_argument(
        "action",
        choices=["compress", "decompress", "list"],
        help="Operation type (compress/decompress/list)",
    )
    parser.add_argument("paths", nargs="+", help="File/directory paths to process")
    parser.add_argument(
        "-f",
        "--format",
        choices=WRITABLE_FORMATS.keys(),
        default="7z",
        help="Supported writable formats: 7z, zip, tar, gzip, bzip2, xz, wim",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-o",
        "--output",
        help="Output file/directory path (required for compress/decompress)",
    )
    output_group.add_argument(
        "-v", "--verbose", action="store_true", help="Show detailed file information"
    )
    parser.add_argument("-p", "--password", help="Encryption password")
    parser.add_argument(
        "-l",
        "--level",
        type=str,
        choices=BitCompressionLevel.__members__.keys(),
        default=BitCompressionLevel.Nothing.value,
        help="Compression level (%(choices)s)",
    )
    parser.add_argument(
        "--overwrite",
        choices=OverwriteMode.__members__.keys(),
        default=OverwriteMode.Overwrite.value,
        help="Overwrite mode when output exists (%(choices)s)",
    )

    args = parser.parse_args()

    if args.action in ["compress", "decompress"] and not args.output:
        parser.error("Output file/directory path is required")

    try:
        with lib7zip_context() as lib:
            if args.action == "compress":
                compress(lib, args)
            elif args.action == "decompress":
                decompress(lib, args)
            else:
                list_archive(lib, args)
    except Exception as e:  # pylint: disable=W0718
        sys.stderr.write(f"Unexpected error: {e}\n")
        sys.exit(1)


def compress(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    """
    Compress files/directories into a specified archive format.
    Args:
        lib (Bit7zLibrary): The 7z library instance.
        args (argparse.Namespace): Parsed command-line arguments.
    """
    fmt = WRITABLE_FORMATS[args.format]
    assert isinstance(fmt, BitInOutFormat), (
        f"Format {args.format} is not supported for compression"
    )

    writer = BitArchiveWriter(lib, fmt)

    if args.password:
        writer.set_password(args.password)

    writer.set_compression_level(BitCompressionLevel(args.level))
    writer.set_overwrite_mode(OverwriteMode(args.overwrite))

    writer.add_items([path for path in args.paths if Path(path).exists()])

    writer.compress_to(args.output)
    sys.stdout.write(f"Successfully created archive: {args.output}")


def decompress(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    """
    Decompress an archive to a specified directory.
    Args:
        lib (Bit7zLibrary): The 7z library instance.
        args (argparse.Namespace): Parsed command-line arguments.
    """
    reader = BitArchiveReader(lib, args.paths[0])

    if args.password:
        reader.set_password(args.password)

    reader.extract_to(args.output)
    sys.stdout.write(f"Successfully extracted to: {args.output}")


def list_archive(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    """
    List the contents of an archive.
    Args:
        lib (Bit7zLibrary): The 7z library instance.
        args (argparse.Namespace): Parsed command-line arguments.
    """
    reader = BitArchiveReader(lib, args.paths[0])

    if args.password:
        reader.set_password(args.password)

    # Printing archive metadata
    sys.stdout.write(
        f"Archive properties:\n  Items count: {reader.items_count()}\n"
        f"  Folders count: {reader.folders_count()}\n"
        f"  Files count: {reader.files_count()}\n"
        f"  Size: {reader.size()}\n"
        f"  Packed size: {reader.pack_size()}"
    )

    # Printing the metadata of the archived items
    sys.stdout.write("Archived items")
    for item in reader.items():
        sys.stdout.write(
            f"    Item index: {item.index()}\n"
            f"    Name: {item.name()}\n"
            f"    Extension: {item.extension()}\n"
            f"    Path: {item.path()}\n"
            f"    IsDir: {item.is_dir()}\n"
            f"    Size: {item.size()}\n"
            f"    Packed size: {item.pack_size()}\n"
            f"    CRC: {item.crc()}"
        )


if __name__ == "__main__":
    main()
