from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path
from typing import Any

from . import (
    Bit7zLibrary,
    BitArchiveEditor,
    BitArchiveReader,
    BitArchiveWriter,
    BitCompressionLevel,
    BitCompressionMethod,
    BitInOutFormat,
    BitPropVariant,
    DeletePolicy,
    EncryptionScope,
    FilterPolicy,
    FormatAuto,
    FormatBZip2,
    FormatFeatures,
    FormatGZip,
    FormatSevenZip,
    FormatTar,
    FormatWim,
    FormatXz,
    FormatZip,
    OverwriteMode,
    UpdateMode,
    lib7zip_context,
)

# Maps command-line format names to bit7z format objects.
WRITABLE_FORMATS: dict[str, BitInOutFormat] = {
    "7z": FormatSevenZip,
    "zip": FormatZip,
    "tar": FormatTar,
    "gzip": FormatGZip,
    "bzip2": FormatBZip2,
    "xz": FormatXz,
    "wim": FormatWim,
}

# Maps file extensions to writable format names (for auto-detection).
EXTENSION_MAP: dict[str, str] = {
    ".7z": "7z",
    ".zip": "zip",
    ".tar": "tar",
    ".gz": "gzip",
    ".gzip": "gzip",
    ".bz2": "bzip2",
    ".bzip2": "bzip2",
    ".xz": "xz",
    ".wim": "wim",
}

# All readable formats supported by bit7z (FormatAuto handles detection).
READABLE_FORMATS = {"auto": FormatAuto}

# Maps writable format objects to their display names (for info output).
FORMAT_NAMES: dict[Any, str] = {fmt: name for name, fmt in WRITABLE_FORMATS.items()}

LEVEL_NAMES = [e.name for e in BitCompressionLevel.__members__.values()]
METHOD_NAMES = [e.name for e in BitCompressionMethod.__members__.values()]
OVERWRITE_NAMES = [e.name for e in OverwriteMode.__members__.values()]


def _human_size(num: float) -> str:
    """Convert a byte count into a human-readable string."""
    for unit in ("B", "KB", "MB", "GB", "TB", "PB"):
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}" if unit != "B" else f"{int(num)} {unit}"
        num /= 1024.0
    return f"{num:.1f} EB"


def _progress_callback(stream: Any) -> Any:
    """Build a progress callback that writes a percentage to stderr."""

    def cb(processed_size: int) -> bool:
        total = getattr(stream, "_pybit7z_total", 0)
        if total > 0:
            pct = min(100, int(100.0 * processed_size / total))
            sys.stderr.write(f"\r  Progress: {pct:3d}%")
            sys.stderr.flush()
        return True

    return cb


def _total_callback(stream: Any) -> Any:
    def cb(total_size: int) -> None:
        stream._pybit7z_total = total_size

    return cb


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pybit7z",
        description="pybit7z command-line compression tool",
    )
    parser.add_argument(
        "action",
        choices=[
            "compress",
            "decompress",
            "extract",
            "list",
            "test",
            "info",
            "update",
        ],
        help="Operation to perform",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="File/directory paths (or archive path) to process",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=list(WRITABLE_FORMATS.keys()) + list(READABLE_FORMATS.keys()),
        default="auto",
        help="Archive format (auto-detect for read operations). "
        f"Writable: {', '.join(WRITABLE_FORMATS)}.",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-o",
        "--output",
        help="Output file/directory path",
    )
    output_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show detailed file information",
    )
    parser.add_argument("-p", "--password", help="Encryption password")
    parser.add_argument(
        "--crypt-headers",
        action="store_true",
        help="Encrypt archive headers too (7z format only)",
    )
    parser.add_argument(
        "-l",
        "--level",
        type=str,
        choices=LEVEL_NAMES,
        default=BitCompressionLevel.Normal.name,
        help="Compression level (%(choices)s)",
    )
    parser.add_argument(
        "-m",
        "--method",
        type=str,
        choices=METHOD_NAMES,
        help="Compression method (%(choices)s). Default is format's default.",
    )
    parser.add_argument(
        "--overwrite",
        choices=OVERWRITE_NAMES,
        default=OverwriteMode.Overwrite.name,
        help="Overwrite mode when output exists (%(choices)s)",
    )
    parser.add_argument(
        "--solid",
        action="store_true",
        help="Use solid compression (7z only)",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=0,
        help="Number of compression threads (0 = 7-zip default)",
    )
    parser.add_argument(
        "--volume-size",
        type=int,
        default=0,
        help="Volume size in bytes for multi-volume archives (0 = single volume)",
    )
    parser.add_argument(
        "--dictionary-size",
        type=int,
        help="Dictionary size in bytes for compression",
    )
    parser.add_argument(
        "--word-size",
        type=int,
        help="Word size in bytes for compression",
    )
    parser.add_argument(
        "--no-store-times",
        action="store_true",
        help="Do not store file timestamps in the archive",
    )
    parser.add_argument(
        "--symlinks",
        choices=["follow", "donotfollow"],
        default="follow",
        help="How to handle symbolic links",
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show progress percentage during operations",
    )

    # Extract-specific options
    extract_group = parser.add_argument_group("extract options")
    extract_group.add_argument(
        "-i",
        "--indices",
        type=int,
        nargs="+",
        help="Extract only items with the given indices",
    )
    extract_group.add_argument(
        "--match",
        help="Extract only items matching the wildcard pattern",
    )
    extract_group.add_argument(
        "--match-regex",
        help="Extract only items matching the regex pattern",
    )
    extract_group.add_argument(
        "--filter-policy",
        choices=["include", "exclude"],
        default="include",
        help="Filter policy for --match/--match-regex",
    )
    extract_group.add_argument(
        "--retain-dirs",
        action="store_true",
        help="Preserve directory structure on extraction",
    )
    extract_group.add_argument(
        "--to-stdout",
        action="store_true",
        help="Extract first matched item to stdout (for piping)",
    )

    # Update/edit-specific options
    update_group = parser.add_argument_group("update options")
    update_group.add_argument(
        "--delete",
        action="append",
        default=[],
        help="Delete item(s) by in-archive path (can be repeated)",
    )
    update_group.add_argument(
        "--delete-index",
        type=int,
        action="append",
        default=[],
        help="Delete item(s) by index (can be repeated)",
    )
    update_group.add_argument(
        "--rename",
        action="append",
        default=[],
        metavar="OLD=NEW",
        help="Rename item from OLD path to NEW path (can be repeated)",
    )
    update_group.add_argument(
        "--rename-index",
        action="append",
        default=[],
        metavar="INDEX:NEW",
        help="Rename item at INDEX to NEW path (can be repeated)",
    )
    update_group.add_argument(
        "--recurse-dirs",
        action="store_true",
        help="Recursively delete folder contents (delete policy)",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.action in ("compress", "decompress", "extract") and not args.output:
        if not (args.action in ("decompress", "extract") and args.to_stdout):
            parser.error("Output file/directory path is required")

    try:
        with lib7zip_context() as lib:
            if args.action == "compress":
                compress(lib, args)
            elif args.action in ("decompress", "extract"):
                extract(lib, args)
            elif args.action == "list":
                list_archive(lib, args)
            elif args.action == "test":
                test_archive(lib, args)
            elif args.action == "info":
                info_archive(lib, args)
            elif args.action == "update":
                update_archive(lib, args)
    except Exception as e:  # pylint: disable=W0718
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


def _resolve_read_format(args: argparse.Namespace) -> Any:
    """Resolve the read format: 'auto' -> FormatAuto, else the writable format."""
    if args.format in READABLE_FORMATS:
        return READABLE_FORMATS[args.format]
    return WRITABLE_FORMATS[args.format]


def _apply_progress(handler: BitArchiveEditor, args: argparse.Namespace) -> None:
    if args.progress:
        handler.set_total_callback(_total_callback(handler))
        handler.set_progress_callback(_progress_callback(handler))


def compress(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    fmt_name = args.format
    if fmt_name == "auto":
        if args.output and args.output != "-":
            ext = Path(args.output).suffix.lower()
            fmt_name = EXTENSION_MAP.get(ext, "7z")
        else:
            fmt_name = "7z"

    fmt = WRITABLE_FORMATS[fmt_name]
    assert isinstance(fmt, BitInOutFormat), (
        f"Format {fmt_name} is not supported for compression"
    )

    writer = BitArchiveWriter(lib, fmt)

    if args.password:
        if args.crypt_headers and fmt.has_feature(FormatFeatures.HeaderEncryption):
            writer.set_password(args.password, EncryptionScope.DataAndHeaders)
        else:
            writer.set_password(args.password)

    writer.set_compression_level(getattr(BitCompressionLevel, args.level))
    writer.set_overwrite_mode(getattr(OverwriteMode, args.overwrite))

    if args.method:
        writer.set_compression_method(getattr(BitCompressionMethod, args.method))
    if args.dictionary_size is not None:
        writer.set_dictionary_size(args.dictionary_size)
    if args.word_size is not None:
        writer.set_word_size(args.word_size)
    if args.solid and fmt.has_feature(FormatFeatures.SolidArchive):
        writer.set_solid_mode(True)
    if args.threads:
        writer.set_threads_count(args.threads)
    if args.volume_size:
        writer.set_volume_size(args.volume_size)
    if args.no_store_times:
        writer.set_store_creation_time(False)
        writer.set_store_last_access_time(False)
        writer.set_store_last_write_time(False)

    # Symbolic link handling: 'donotfollow' stores links as-is,
    # 'follow' (default) stores the target file content.
    writer.set_store_symbolic_links(args.symlinks == "donotfollow")

    # Add each path: files use add_file, directories use add_directory.
    for p in args.paths:
        path = Path(p)
        if not path.exists():
            sys.stderr.write(f"Warning: path does not exist, skipping: {p}\n")
            continue
        if path.is_dir():
            writer.add_directory(str(path))
        else:
            writer.add_file(str(path))

    _apply_progress(writer, args)

    out = args.output
    if out == "-":
        # Compress to stdout as bytes.
        buf = writer.compress_to()
        sys.stdout.buffer.write(buf)
    else:
        writer.compress_to(out)
        if args.progress:
            sys.stderr.write("\n")
        sys.stdout.write(f"Successfully created archive: {out}")


def extract(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    fmt = _resolve_read_format(args)
    password = args.password or ""
    reader = BitArchiveReader(lib, args.paths[0], fmt, password)

    reader.set_overwrite_mode(getattr(OverwriteMode, args.overwrite))
    reader.set_retain_directories(args.retain_dirs)
    _apply_progress(reader, args)

    if args.to_stdout:
        # Extract first matching item (or item 0) to stdout.
        if args.indices:
            data = reader.extract_to(args.indices[0])
        elif args.match:
            policy = getattr(FilterPolicy, args.filter_policy.capitalize())
            items = reader.items()

            for item in items:
                if fnmatch.fnmatch(item.name(), args.match) != (policy == FilterPolicy.Exclude):
                    data = reader.extract_to(item.index())
                    break
            else:
                raise RuntimeError(f"No item matches pattern: {args.match}")
        else:
            data = reader.extract_to(0)
        sys.stdout.buffer.write(data)
        return

    out_dir = args.output
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    if args.indices:
        reader.extract_to(out_dir, args.indices)
    elif args.match:
        policy = getattr(FilterPolicy, args.filter_policy.capitalize())
        reader.extract_matching_to(out_dir, args.match, policy)
    elif args.match_regex:
        pattern = re.compile(args.match_regex)
        policy = getattr(FilterPolicy, args.filter_policy.capitalize())
        indices = [
            item.index()
            for item in reader.items()
            if bool(pattern.search(item.path())) != (policy == FilterPolicy.Exclude)
        ]
        if not indices:
            raise RuntimeError(f"No item matches regex: {args.match_regex}")
        reader.extract_to(out_dir, indices)
    else:
        reader.extract_to(out_dir)

    if args.progress:
        sys.stderr.write("\n")
    sys.stdout.write(f"Successfully extracted to: {out_dir}")


def list_archive(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    fmt = _resolve_read_format(args)
    password = args.password or ""
    reader = BitArchiveReader(lib, args.paths[0], fmt, password)

    sys.stdout.write(
        f"Archive: {args.paths[0]}\n"
        f"  Items:   {reader.items_count()}\n"
        f"  Files:   {reader.files_count()}\n"
        f"  Folders: {reader.folders_count()}\n"
        f"  Size:    {_human_size(reader.size())}\n"
        f"  Packed:  {_human_size(reader.pack_size())}\n"
    )

    if args.verbose:
        sys.stdout.write(f"  Solid:   {reader.is_solid()}\n")
        sys.stdout.write(f"  Encrypted: {reader.is_encrypted()}\n")
        sys.stdout.write(f"  Volumes: {reader.volumes_count()}\n")

    sys.stdout.write("\n")

    # Table header
    header = f"{'Idx':>4}  {'Size':>10}  {'Packed':>10}  {'Flags':>6}  Name"
    sys.stdout.write(header + "\n")
    sys.stdout.write("-" * len(header) + "\n")

    for item in reader.items():
        flags = []
        if item.is_dir():
            flags.append("D")
        if item.is_encrypted():
            flags.append("E")
        flag_str = "".join(flags) if flags else "-"
        sys.stdout.write(
            f"{item.index():>4}  {_human_size(item.size()):>10}  "
            f"{_human_size(item.pack_size()):>10}  {flag_str:>6}  {item.path()}\n"
        )


def test_archive(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    fmt = _resolve_read_format(args)
    password = args.password or ""
    reader = BitArchiveReader(lib, args.paths[0], fmt, password)

    _apply_progress(reader, args)

    if args.indices:
        reader.test(args.indices)
    else:
        reader.test()

    if args.progress:
        sys.stderr.write("\n")
    sys.stdout.write("Archive integrity test passed.")


def info_archive(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    fmt = _resolve_read_format(args)
    password = args.password or ""
    reader = BitArchiveReader(lib, args.paths[0], fmt, password)

    detected = reader.detected_format()
    fmt_name = FORMAT_NAMES.get(detected, f"id={detected.value()}")
    sys.stdout.write(
        f"Archive: {args.paths[0]}\n"
        f"  Format:          {fmt_name}\n"
        f"  Items count:     {reader.items_count()}\n"
        f"  Files count:     {reader.files_count()}\n"
        f"  Folders count:   {reader.folders_count()}\n"
        f"  Uncompressed:    {_human_size(reader.size())}\n"
        f"  Compressed:      {_human_size(reader.pack_size())}\n"
        f"  Encrypted:       {reader.is_encrypted()}\n"
        f"  Has encrypted:   {reader.has_encrypted_items()}\n"
        f"  Solid:           {reader.is_solid()}\n"
        f"  Multi-volume:    {reader.is_multi_volume()}\n"
        f"  Volumes:         {reader.volumes_count()}\n"
    )

    if args.verbose:
        # Show all archive properties.
        props = reader.archive_properties()
        sys.stdout.write("\nArchive properties:\n")
        for prop, variant in props.items():
            sys.stdout.write(f"  {prop.name}: {_variant_to_str(variant)}\n")


def _variant_to_str(variant: BitPropVariant) -> str:
    if variant.is_string():
        return variant.get_string()
    if variant.is_uint64():
        return str(variant.get_uint64())
    if variant.is_bool():
        return str(variant.get_bool())
    return f"<{variant.type().name}>"


def update_archive(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    if args.format == "auto":
        parser = build_parser()
        parser.error("Update requires an explicit writable format (use -f 7z, zip, ...)")

    fmt = WRITABLE_FORMATS[args.format]
    password = args.password or ""
    editor = BitArchiveEditor(lib, args.paths[0], fmt, password)

    editor.set_update_mode(UpdateMode.Update)

    delete_policy = (
        DeletePolicy.RecurseDirs if args.recurse_dirs else DeletePolicy.ItemOnly
    )

    changed = False

    for path in args.delete:
        editor.delete_item(path, delete_policy)
        changed = True
    for idx in args.delete_index:
        editor.delete_item(idx, delete_policy)
        changed = True

    for spec in args.rename:
        if "=" not in spec:
            raise ValueError(f"Invalid --rename spec (expected OLD=NEW): {spec}")
        old, new = spec.split("=", 1)
        editor.rename_item(old, new)
        changed = True
    for spec in args.rename_index:
        if ":" not in spec:
            raise ValueError(f"Invalid --rename-index spec (expected INDEX:NEW): {spec}")
        idx_str, new = spec.split(":", 1)
        editor.rename_item(int(idx_str), new)
        changed = True

    if not changed:
        sys.stderr.write("No update operations specified (use --delete/--rename/...)\n")
        sys.exit(2)

    _apply_progress(editor, args)
    editor.apply_changes()

    if args.progress:
        sys.stderr.write("\n")
    sys.stdout.write("Successfully updated archive.")


if __name__ == "__main__":
    main()
