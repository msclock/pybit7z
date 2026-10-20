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
    BitCodecInfo,
    BitCompressionLevel,
    BitCompressionMethod,
    BitFormatInfo,
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
    default_plugin_dir,
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
            "info",
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
        default="auto",
        help="Archive format (auto-detect for read operations). "
        f"Built-in writable: {', '.join(WRITABLE_FORMATS)}. "
        "External formats loaded from plugins are also supported "
        "(run 'info' to list all available formats).",
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
        default=None,
        help="Compression method (e.g. Lzma, Deflate, brotli, zstd). Default is format's default.",
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
    parser.add_argument(
        "--plugin-dir",
        action="append",
        default=None,
        metavar="DIR",
        help="Additional directory containing external codec/format plugins to load. "
        "Can be repeated. For each directory the Codecs/ and Formats/ subfolders "
        "are scanned. Bundled plugins are always loaded automatically.",
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


def _load_codecs(lib: Bit7zLibrary, extra_dirs: Optional[list[str]] = None) -> None:
    """Load bundled external codecs and format handlers plus any user-specified directories.

    All directories are passed to :meth:`Bit7zLibrary.load_plugins` in a single
    call. For each directory the library scans the ``Codecs/`` subfolder first,
    then the ``Formats/`` subfolder, accumulating the results.
    """
    plugin_paths: list[str] = []

    plugin_dir = Path(default_plugin_dir())
    if plugin_dir.is_dir():
        plugin_paths.append(str(plugin_dir))

    if extra_dirs:
        for d in extra_dirs:
            if Path(d).is_dir():
                plugin_paths.append(d)

    if plugin_paths:
        lib.load_plugins(plugin_paths)


def main(argv: Optional[list[str]] = None) -> None:
    """Entry point for the CLI application.

    Parses arguments and dispatches to the appropriate handler.

    Args:
        argv: Optional list of command-line arguments. If None, ``sys.argv[1:]``
            is used (the normal process-argument behaviour). Passing an explicit
            list allows the function to be driven from tests without spawning a
            subprocess.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    # 'info' without an archive path shows library info.
    if args.action == "info" and not args.paths:
        with lib7zip_context() as lib:
            _load_codecs(lib, args.plugin_dir)
            show_library_info(lib)
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
            _load_codecs(lib, args.plugin_dir)
            _validate_format(parser, lib, args)

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


def _validate_format(
    parser: argparse.ArgumentParser, lib: Bit7zLibrary, args: argparse.Namespace
) -> None:
    """Validate that ``args.format`` is a known (built-in or loaded external) format.

    External formats are discovered at runtime after loading plugin DLLs, so
    this check cannot be performed by argparse's static ``choices`` and must
    happen here. Invalid values produce an argparse-style error.
    """
    if args.format == "auto":
        return
    valid = _available_format_names(lib)
    if args.format not in valid:
        parser.error(
            f"argument -f/--format: invalid choice: '{args.format}' "
            f"(choose from {', '.join(valid)})"
        )


def _available_format_names(lib: Bit7zLibrary) -> list[str]:
    """Return all available format names: built-in writable + externally loaded.

    External formats are discovered at runtime from the loaded 7-zip format
    DLLs (see :func:`Bit7zLibrary.get_formats`). Only formats that support
    update (``update=True``) are included, as they are the writable ones.
    """
    names: set[str] = set(WRITABLE_FORMATS.keys())
    names.update(READABLE_FORMATS.keys())
    for f in lib.get_formats():
        if f.update:
            names.add(f.name.lower())
    return sorted(names)


def _resolve_writable_format(lib: Bit7zLibrary, name: str) -> BitInOutFormat:
    """Resolve a format name to a ``BitInOutFormat``.

    Built-in formats are looked up in :data:`WRITABLE_FORMATS`; otherwise the
    external format registry of the loaded 7-zip library is consulted.
    """
    fmt = WRITABLE_FORMATS.get(name)
    if fmt is not None:
        return fmt
    external: Optional[BitInOutFormat] = lib.get_external_in_out_format(name)
    if external is not None:
        return external
    available = _available_format_names(lib)
    msg = f"Unsupported format '{name}'. Available formats: {', '.join(available)}"
    raise ValueError(msg)


def _resolve_format_from_extension(lib: Bit7zLibrary, ext: str) -> Optional[str]:
    """Resolve a file extension to a format name.

    Built-in extensions are looked up in :data:`EXTENSION_MAP`; otherwise the
    formats loaded from external format DLLs are scanned for a matching
    extension. Each format's ``extension`` field may contain multiple
    space-separated extensions (e.g. ``"br brotli tbr"``).
    """
    if ext in EXTENSION_MAP:
        return EXTENSION_MAP[ext]
    ext_clean = ext.lstrip(".").lower()
    for f in lib.get_formats():
        if not f.update:
            continue
        for token in f.extension.lower().split():
            if token == ext_clean:
                return f.name.lower()
        for token in f.add_extension.lower().split():
            if token == ext_clean and token != "*":
                return f.name.lower()
    return None


def _is_external_format(name: str) -> bool:
    """Return True if the format name is not a built-in writable format.

    External formats are loaded dynamically from format DLLs, so any name not
    present in :data:`WRITABLE_FORMATS` is treated as external.
    """
    return name not in WRITABLE_FORMATS


def _resolve_read_format(lib: Bit7zLibrary, args: argparse.Namespace) -> Any:
    """Resolve the read format for an archive path.

    ``auto`` first attempts extension-based detection (needed for formats
    without a magic-number signature such as brotli/lz4), then falls back to
    ``FormatAuto`` for signature-based detection.
    """
    if args.format not in READABLE_FORMATS:
        if args.format in WRITABLE_FORMATS:
            return WRITABLE_FORMATS[args.format]
        external = lib.get_external_in_out_format(args.format)
        if external is not None:
            return external
        in_fmt = lib.get_external_in_format(args.format)
        if in_fmt is not None:
            return in_fmt
        return FormatAuto

    # 'auto' mode: try extension-based detection first, then signature-based.
    if args.paths:
        ext = Path(args.paths[0]).suffix.lower()
        fmt_name = _resolve_format_from_extension(lib, ext)
        if fmt_name is not None:
            if fmt_name in WRITABLE_FORMATS:
                return WRITABLE_FORMATS[fmt_name]
            external = lib.get_external_in_out_format(fmt_name)
            if external is not None:
                return external
            in_fmt = lib.get_external_in_format(fmt_name)
            if in_fmt is not None:
                return in_fmt
    return FormatAuto


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


def _bit7z_defined_extensions() -> set[str]:
    """Collect names of all formats predefined by bit7z."""
    result: set[str] = set()
    for name in dir(_core):
        if not name.startswith("Format"):
            continue
        if name in ("FormatFeatures", "FormatAuto"):
            continue
        obj = getattr(_core, name)
        if isinstance(obj, type):
            continue
        fmt_name = name[6:].lower()
        if fmt_name == "sevenzip":
            fmt_name = "7z"
        result.add(fmt_name)
    return result


def show_library_info(lib: Bit7zLibrary) -> None:
    """Print supported formats, codecs, and hashers (similar to ``7z i``)."""
    formats: list[BitFormatInfo] = lib.get_formats()
    codecs: list[BitCodecInfo] = lib.get_codecs()
    codec_paths: list[str] = lib.get_codec_paths()
    bit7z_names = _bit7z_defined_extensions()

    sys.stdout.write("Libs:\n")
    if codec_paths:
        for i, p in enumerate(codec_paths):
            sys.stdout.write(f"  {i:>2} : {p}\n")
    else:
        sys.stdout.write("  (no external codecs loaded)\n")

    sys.stdout.write("\nFormats:\n")
    sys.stdout.write(
        f"  {'#':>3} {'bit7z':>5} {'Name':<16} {'Ext':<10} {'Update':>6} {'Signature'}\n"
    )
    sys.stdout.write("  " + "-" * 68 + "\n")
    for i, f in enumerate(formats):
        sig = f.signature.hex() if f.signature else ""
        update = "Y" if f.update else "-"
        defined = "Y" if f.name.lower() in bit7z_names else "-"
        sys.stdout.write(
            f"  {i:>3} {defined:>5} {f.name:<16} {f.extension:<10} {update:>6} {sig}\n"
        )

    sys.stdout.write("\nCodecs:\n")
    sys.stdout.write(
        f"  {'#':>3} {'Ext':>3} {'ID':<18} {'Name':<16} {'Enc':>3} {'Dec':>3} {'Desc'}\n"
    )
    sys.stdout.write("  " + "-" * 72 + "\n")
    for i, c in enumerate(codecs):
        enc = "Y" if c.encoder else "-"
        dec = "Y" if c.decoder else "-"
        ext = "Y" if c.is_external else "-"
        sys.stdout.write(
            f"  {i:>3} {ext:>3} {c.id:<#018x} {c.name:<16} {enc:>3} {dec:>3} {c.description}\n"
        )


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
            resolved = _resolve_format_from_extension(lib, ext)
            fmt_name = resolved if resolved else "7z"
        else:
            fmt_name = "7z"

    fmt = _resolve_writable_format(lib, fmt_name)
    is_external = _is_external_format(fmt_name)

    writer = BitArchiveWriter(lib, fmt)

    if args.password:
        if args.crypt_headers and fmt.has_feature(FormatFeatures.HeaderEncryption):
            writer.set_password(args.password, EncryptionScope.DataAndHeaders)
        else:
            writer.set_password(args.password)

    writer.set_compression_level(getattr(BitCompressionLevel, args.level))
    writer.set_overwrite_mode(getattr(OverwriteMode, args.overwrite))

    if args.method:
        if is_external:
            # Standalone external formats (e.g. brotli, zstd) use a fixed
            # compression algorithm; --method only applies to container
            # formats such as 7z/zip.
            sys.stderr.write(f"Warning: ignoring --method for {fmt_name} format\n")
        else:
            external_codecs = {
                c.name for c in lib.get_codecs() if c.is_external and c.encoder
            }
            method_lower = args.method.lower()
            external_lower = {name.lower(): name for name in external_codecs}
            if method_lower in external_lower:
                # External codecs (brotli, zstd, lz4, ...) are used via the Copy
                # method plus a format property that selects the codec by name.
                writer.set_compression_method(BitCompressionMethod.Copy)
                writer.set_format_property(
                    "0", BitPropVariant(external_lower[method_lower])
                )
            elif hasattr(BitCompressionMethod, args.method):
                writer.set_compression_method(
                    getattr(BitCompressionMethod, args.method)
                )
            else:
                available = METHOD_NAMES + sorted(external_codecs)
                msg = (
                    f"Unknown compression method '{args.method}'. "
                    f"Available methods: {', '.join(available)}"
                )
                raise ValueError(msg)
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
                    _add_files_from_directory(
                        writer,
                        path,
                        exclude_patterns,
                        source_files,
                    )
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
    fmt = _resolve_read_format(lib, args)
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
    fmt = _resolve_read_format(lib, args)
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
    """Run integrity test(s) on the archive items specified."""
    fmt = _resolve_read_format(lib, args)
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
    fmt = _resolve_read_format(lib, args)
    password = args.password or ""
    reader = BitArchiveReader(lib, args.paths[0], fmt, password)

    detected = reader.detected_format()
    fmt_name = FORMAT_NAMES.get(detected)
    if fmt_name is None:
        # External formats are not in FORMAT_NAMES; look them up by value.
        detected_value = detected.value()
        for f in lib.get_formats():
            fmt_obj = lib.get_external_in_out_format(f.name)
            if fmt_obj is not None and fmt_obj.value() == detected_value:
                fmt_name = f.name
                break
        if fmt_name is None:
            fmt_name = f"id={detected_value}"
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

    fmt = _resolve_writable_format(lib, args.format)
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
