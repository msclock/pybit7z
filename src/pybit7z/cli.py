from __future__ import annotations

import argparse
import fnmatch
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

from . import (
    Bit7zLibrary,
    BitAbstractArchiveHandler,
    BitArchiveEditor,
    BitArchiveReader,
    BitArchiveWriter,
    BitCompressionLevel,
    BitCompressionMethod,
    BitInFormat,
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
    _core,
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

# Maps writable format objects (or their ids) to their display names (for info output).
# Some of the bit7z format objects may not be Python types suitable for use as
# dict keys in isinstance checks or as hashable keys; map by a stable key when
# possible (prefer the .value() if provided).
FORMAT_NAMES: dict[Any, str] = {}
for name, fmt in WRITABLE_FORMATS.items():
    key = fmt.value() if hasattr(fmt, "value") else fmt
    FORMAT_NAMES[key] = name

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


def _total_callback(total_ref: list[int]) -> Any:
    """Return a callback that updates total_ref[0] with the total size."""

    def cb(total_size: int) -> None:
        total_ref[0] = total_size

    return cb


def build_parser() -> argparse.ArgumentParser:
    """Build and return the ArgumentParser for the CLI."""
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
            "formats",
        ],
        help="Operation to perform",
    )
    parser.add_argument(
        "paths",
        nargs="*",
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
        "--store-open-files",
        action="store_true",
        help="Compress files that are open by other processes (7z -ssw)",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        action="append",
        default=None,
        metavar="PATTERN",
        help="Exclude files matching the wildcard pattern during compression "
        "(can be repeated)",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read input data from stdin for compression (7z -si)",
    )
    parser.add_argument(
        "--stdin-name",
        default="stdin",
        help="Name to use for the stdin input item (default: stdin)",
    )
    parser.add_argument(
        "--delete-after",
        action="store_true",
        help="Delete source files after successful compression (7z -sdel)",
    )
    parser.add_argument(
        "--format-property",
        action="append",
        default=None,
        metavar="KEY=VALUE",
        help="Set a raw 7z format property (e.g. '0=4' for 4 threads). "
        "Can be repeated.",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Assume Yes on all queries (suppress overwrite prompts)",
    )
    parser.add_argument(
        "--show-files",
        action="store_true",
        help="Log each file as it is processed",
    )
    parser.add_argument(
        "--progress",
        action="store_true",
        help="Show progress percentage during operations",
    )
    parser.add_argument(
        "--ratio",
        action="store_true",
        help="Show compression ratio during progress",
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
        default=None,
        help="Delete item(s) by in-archive path (can be repeated)",
    )
    update_group.add_argument(
        "--delete-index",
        type=int,
        action="append",
        default=None,
        help="Delete item(s) by index (can be repeated)",
    )
    update_group.add_argument(
        "--rename",
        action="append",
        default=None,
        metavar="OLD=NEW",
        help="Rename item from OLD path to NEW path (can be repeated)",
    )
    update_group.add_argument(
        "--rename-index",
        action="append",
        default=None,
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
    """Entry point for the CLI application.

    Parses arguments and dispatches to the appropriate handler.
    """
    parser = build_parser()
    args = parser.parse_args()

    # 'formats' does not need an archive or input paths.
    if args.action == "formats":
        show_formats()
        return

    # Compression requires output; stdin mode allows no input paths.
    if args.action == "compress":
        if not args.output:
            parser.error("Output file path is required for compression")
        if not args.paths and not args.stdin:
            parser.error("Input paths are required (or use --stdin)")

    if (
        args.action in ("decompress", "extract")
        and not args.output
        and not args.to_stdout
    ):
        parser.error("Output file/directory path is required")

    if args.action in ("list", "test", "info", "update") and not args.paths:
        parser.error("Archive path is required")

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


class _ProgressHelper:
    """Helper that encapsulates progress/ratio/file display state and callbacks.

    This avoids deep nested callbacks by keeping mutable state in instance
    attributes and exposing methods suitable for passing as callbacks to the
    underlying bit7z handler.
    """

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.total_ref: list[int] = [0]
        self.last_pct: list[int] = [0]
        # Use lowercase 'tuple' in the annotation to help pylint's type inference
        # and avoid a false-positive "Attempting to unpack a non-sequence" error.
        self.last_ratio: list[Optional[tuple[int, int]]] = [None]
        self.line_active: list[bool] = [False]
        self.last_text: list[str] = [""]

    def build_text(self) -> str:
        """Build the current status text from progress/ratio state."""
        parts = []
        if self.args.progress:
            parts.append(f"Progress: {self.last_pct[0]:3d}%")
        if self.args.ratio:
            ratio = self.last_ratio[0]
            if ratio is not None:
                in_size, out_size = ratio
                if in_size > 0:
                    rpct = int(100.0 * out_size / in_size)
                    parts.append(
                        f"Ratio: {rpct}% ({_human_size(out_size)} / {_human_size(in_size)})"
                    )
        return "  ".join(parts)

    def render(self) -> None:
        """Render the current status text to stderr (updates single line)."""
        text = self.build_text()
        if not text:
            return
        if text == self.last_text[0] and self.line_active[0]:
            return
        sys.stderr.write("\r  " + text)
        sys.stderr.flush()
        self.last_text[0] = text
        self.line_active[0] = True

    def progress_cb(self, processed_size: int) -> bool:
        """Progress callback expected by the handler; returns True to continue."""
        total = self.total_ref[0] if self.total_ref else 0
        if total > 0:
            self.last_pct[0] = min(100, int(100.0 * processed_size / total))
            self.render()
        return True

    def ratio_cb(self, in_size: int, out_size: int) -> None:
        """Ratio callback to store sizes and re-render."""
        self.last_ratio[0] = (in_size, out_size)
        self.render()

    def file_cb(self, path: str) -> None:
        """File callback to log each processed file on its own line."""
        if self.line_active[0]:
            sys.stderr.write("\r" + " " * 80 + "\r")
            self.line_active[0] = False
            self.last_text[0] = ""
        sys.stderr.write(f"  + {path}\n")
        sys.stderr.flush()
        self.render()

    def attach(self, handler: BitAbstractArchiveHandler) -> None:
        """Attach callbacks to the provided handler based on CLI flags."""
        if self.args.progress or self.args.ratio:
            handler.set_total_callback(_total_callback(self.total_ref))
            handler.set_progress_callback(self.progress_cb)
            if self.args.ratio:
                handler.set_ratio_callback(self.ratio_cb)
        if self.args.show_files:
            handler.set_file_callback(self.file_cb)


def _apply_progress(
    handler: BitAbstractArchiveHandler,
    args: argparse.Namespace,
) -> None:
    """Configure progress/ratio/file callbacks on the provided handler.

    This implementation uses _ProgressHelper to keep callback state at the
    instance level and avoid deeply nested inner functions that trigger
    "too many nested blocks" lint warnings.
    """
    helper = _ProgressHelper(args)
    helper.attach(handler)


def show_formats() -> None:
    """List all supported archive formats with their extensions and features."""

    writable: list[tuple[str, BitInOutFormat]] = []
    readable: list[tuple[str, BitInFormat]] = []
    for name in dir(_core):
        if not name.startswith("Format"):
            continue
        obj = getattr(_core, name)
        # Avoid isinstance checks against non-type objects which can raise
        # TypeError during import; use duck-typing instead.
        if hasattr(obj, "has_feature") and hasattr(obj, "extension"):
            writable.append((name, obj))
        elif hasattr(obj, "value"):
            readable.append((name, obj))

    sys.stdout.write("Writable formats:\n")
    header = f"  {'Name':<12} {'Extension':<10} {'Features'}\n"
    sys.stdout.write(header)
    sys.stdout.write("  " + "-" * 50 + "\n")
    for name, fmt in sorted(writable, key=lambda x: x[0]):
        features = _format_features_str(fmt)
        # Some format objects expose an extension() method.
        ext = fmt.extension() if hasattr(fmt, "extension") else "-"
        sys.stdout.write(f"  {name:<12} {ext:<10} {features}\n")

    sys.stdout.write("\nRead-only formats:\n")
    sys.stdout.write(header)
    sys.stdout.write("  " + "-" * 50 + "\n")
    for name, fmt in sorted(readable, key=lambda x: x[0]):  # type: ignore[assignment]
        # For read-only formats print their id/value when available.
        val = fmt.value() if hasattr(fmt, "value") else str(fmt)
        sys.stdout.write(f"  {name:<12} {'-':<10} id={val}\n")


def _format_features_str(fmt: BitInOutFormat) -> str:
    """Return a comma-separated string describing format features."""
    feats = []
    if fmt.has_feature(FormatFeatures.MultipleFiles):
        feats.append("multi-file")
    if fmt.has_feature(FormatFeatures.SolidArchive):
        feats.append("solid")
    if fmt.has_feature(FormatFeatures.CompressionLevel):
        feats.append("levels")
    if fmt.has_feature(FormatFeatures.Encryption):
        feats.append("encrypt")
    if fmt.has_feature(FormatFeatures.HeaderEncryption):
        feats.append("hdr-enc")
    if fmt.has_feature(FormatFeatures.MultipleMethods):
        feats.append("methods")
    return ",".join(feats) if feats else "-"


def _add_files_from_directory(
    writer: BitArchiveWriter,
    base_path: Path,
    exclude_patterns: list[str],
    source_files: list[Path],
) -> None:
    """Walk a directory, adding files to writer while applying exclude patterns."""
    for root, dirs, files in os.walk(base_path):
        if exclude_patterns:
            dirs[:] = [
                d
                for d in dirs
                if not any(fnmatch.fnmatch(d, pat) for pat in exclude_patterns)
            ]
        for fname in files:
            if exclude_patterns and any(
                fnmatch.fnmatch(fname, pat) for pat in exclude_patterns
            ):
                continue
            fpath = Path(root) / fname
            writer.add_file(str(fpath))
            source_files.append(fpath)


def _collect_files_under_directory(base_path: Path, source_files: list[Path]) -> None:
    """Collect all files under base_path into source_files (for deletion)."""
    for root, _dirs, files in os.walk(base_path):
        for fname in files:
            source_files.append(Path(root) / fname)


def compress(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    """Create an archive from the provided paths or stdin using the writer API."""

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
    if args.store_open_files:
        writer.set_store_open_files(True)

    # Symbolic link handling: 'donotfollow' stores links as-is,
    # 'follow' (default) stores the target file content.
    writer.set_store_symbolic_links(args.symlinks == "donotfollow")

    # Raw 7z format properties (e.g. '0=4' -> 4 threads, 'x=9' -> ultra level).
    for prop in args.format_property or []:
        if "=" not in prop:
            msg = f"Invalid --format-property (expected KEY=VALUE): {prop}"
            raise ValueError(msg)
        key, value = prop.split("=", 1)
        # bit7z's BitPropVariant only supports bool/uint64; parse numeric values.
        if value.lower() in ("true", "false"):
            variant = BitPropVariant(value.lower() == "true")
        else:
            variant = BitPropVariant(int(value))
        writer.set_format_property(key, variant)

    # Collect source files (with exclusion filtering) and track for --delete-after.
    source_files: list[Path] = []
    exclude_patterns = args.exclude or []

    def _excluded(name: str) -> bool:
        return any(fnmatch.fnmatch(name, pat) for pat in exclude_patterns)

    # IMPORTANT: callbacks (progress/ratio/file) must be set BEFORE adding
    # any input items, otherwise bit7z captures an inconsistent internal
    # state and the operation can deadlock.
    _apply_progress(writer, args)

    if args.stdin:
        data = sys.stdin.buffer.read()
        writer.add_file(data, args.stdin_name)
    else:
        for p in args.paths:
            path = Path(p)
            if not path.exists():
                sys.stderr.write(f"Warning: path does not exist, skipping: {p}\n")
                continue
            if path.is_dir():
                if exclude_patterns:
                    _add_files_from_directory(writer, path, exclude_patterns, source_files)
                else:
                    writer.add_directory(str(path))
                    _collect_files_under_directory(path, source_files)
            else:
                if exclude_patterns and _excluded(path.name):
                    continue
                writer.add_file(str(path))
                source_files.append(path)

    out = args.output
    if out == "-":
        # Compress to stdout as bytes.
        buf = writer.compress_to()
        sys.stdout.buffer.write(buf)
    else:
        writer.compress_to(out)
        if args.progress or args.ratio:
            sys.stderr.write("\n")
        sys.stdout.write(f"Successfully created archive: {out}\n")

    # Delete source files after successful compression (7z -sdel).
    if args.delete_after and source_files:
        for f in source_files:
            try:
                f.unlink()
            except OSError as exc:
                sys.stderr.write(f"Warning: could not delete {f}: {exc}\n")


def extract(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    """Extract files from an archive to the given destination or stdout."""
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
                if fnmatch.fnmatch(item.name(), args.match) != (
                    policy == FilterPolicy.Exclude
                ):
                    data = reader.extract_to(item.index())
                    break
            else:
                msg = f"No item matches pattern: {args.match}"
                raise RuntimeError(msg)
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
            msg = f"No item matches regex: {args.match_regex}"
            raise RuntimeError(msg)
        reader.extract_to(out_dir, indices)
    else:
        reader.extract_to(out_dir)

    if args.progress or args.ratio:
        sys.stderr.write("\n")
    sys.stdout.write(f"Successfully extracted to: {out_dir}\n")


def list_archive(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    """Print a listing of archive contents and basic archive metadata."""
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
    header = f"{ 'Idx':>4}  {'Size':>10}  {'Packed':>10}  {'Flags':>6}  Name"
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
    """Run integrity test(s) on the archive items specified."""
    fmt = _resolve_read_format(args)
    password = args.password or ""
    reader = BitArchiveReader(lib, args.paths[0], fmt, password)

    _apply_progress(reader, args)

    if args.indices:
        reader.test(args.indices)
    else:
        reader.test()

    if args.progress or args.ratio:
        sys.stderr.write("\n")
    sys.stdout.write("Archive integrity test passed.\n")


def info_archive(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    """Print detailed archive information (format, sizes, flags, properties)."""
    fmt = _resolve_read_format(args)
    password = args.password or ""
    reader = BitArchiveReader(lib, args.paths[0], fmt, password)

    detected = reader.detected_format()
    key = detected.value() if hasattr(detected, "value") else detected
    fmt_name = FORMAT_NAMES.get(key, f"id={detected.value()}" if hasattr(detected, "value") else str(detected))
    uncompressed = reader.size()
    compressed = reader.pack_size()
    ratio = f"{100.0 * compressed / uncompressed:.1f}%" if uncompressed else "N/A"
    sys.stdout.write(
        f"Archive: {args.paths[0]}\n"
        f"  Format:          {fmt_name}\n"
        f"  Items count:     {reader.items_count()}\n"
        f"  Files count:     {reader.files_count()}\n"
        f"  Folders count:   {reader.folders_count()}\n"
        f"  Uncompressed:    {_human_size(uncompressed)}\n"
        f"  Compressed:      {_human_size(compressed)}\n"
        f"  Ratio:           {ratio}\n"
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
    """Convert a BitPropVariant to a human-readable string."""
    if variant.is_string():
        return variant.get_string()
    if variant.is_uint64():
        return str(variant.get_uint64())
    if variant.is_bool():
        return str(variant.get_bool())
    return f"<{variant.type().name}>"


def update_archive(lib: Bit7zLibrary, args: argparse.Namespace) -> None:
    """Apply updates (delete/rename) to an existing archive.

    The function validates arguments, performs requested update operations,
    and applies changes using BitArchiveEditor.
    """
    if args.format == "auto":
        parser = build_parser()
        parser.error(
            "Update requires an explicit writable format (use -f 7z, zip, ...)"
        )

    fmt = WRITABLE_FORMATS[args.format]
    password = args.password or ""
    editor = BitArchiveEditor(lib, args.paths[0], fmt, password)

    editor.set_update_mode(UpdateMode.Update)

    delete_policy = (
        DeletePolicy.RecurseDirs if args.recurse_dirs else DeletePolicy.ItemOnly
    )

    changed = False

    for path in args.delete or []:
        editor.delete_item(path, delete_policy)
        changed = True
    for idx in args.delete_index or []:
        editor.delete_item(idx, delete_policy)
        changed = True

    for spec in args.rename or []:
        if "=" not in spec:
            msg = f"Invalid --rename spec (expected OLD=NEW): {spec}"
            raise ValueError(msg)
        old, new = spec.split("=", 1)
        editor.rename_item(old, new)
        changed = True
    for spec in args.rename_index or []:
        if ":" not in spec:
            msg = f"Invalid --rename-index spec (expected INDEX:NEW): {spec}"
            raise ValueError(msg)
        idx_str, new = spec.split(":", 1)
        editor.rename_item(int(idx_str), new)
        changed = True

    if not changed:
        sys.stderr.write("No update operations specified (use --delete/--rename/...)\n")
        sys.exit(2)

    _apply_progress(editor, args)
    editor.apply_changes()

    if args.progress or args.ratio:
        sys.stderr.write("\n")
    sys.stdout.write("Successfully updated archive.\n")


if __name__ == "__main__":
    main()
