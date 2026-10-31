# pybit7z

<!-- SPHINX-START -->

A Python wrapper around [bit7z](https://github.com/rikyoz/bit7z) for creating and extracting 7-zip archives, with bundled external codec and format plugins.

[![Documentation](https://img.shields.io/badge/Documentation-sphinx-blue)](https://msclock.github.io/pybit7z)
[![License](https://img.shields.io/github/license/msclock/pybit7z)](https://github.com/msclock/pybit7z/blob/master/LICENSE)
[![SS Badge](https://img.shields.io/badge/Serious%20Scaffold-pybind11-blue)](https://github.com/serious-scaffold/ss-pybind11)

[![CI](https://github.com/msclock/pybit7z/actions/workflows/ci.yml/badge.svg)](https://github.com/msclock/pybit7z/actions/workflows/ci.yml)
[![CD](https://github.com/msclock/pybit7z/actions/workflows/cd.yml/badge.svg)](https://github.com/msclock/pybit7z/actions/workflows/cd.yml)
[![Renovate](https://github.com/msclock/pybit7z/actions/workflows/renovate.yml/badge.svg)](https://github.com/msclock/pybit7z/actions/workflows/renovate.yml)
[![Semantic Release](https://github.com/msclock/pybit7z/actions/workflows/semantic-release.yml/badge.svg)](https://github.com/msclock/pybit7z/actions/workflows/semantic-release.yml)
[![codecov](https://codecov.io/gh/msclock/pybit7z/branch/master/graph/badge.svg?token=123456789)](https://codecov.io/gh/msclock/pybit7z)

[![Release](https://img.shields.io/github/v/release/msclock/pybit7z)](https://github.com/msclock/pybit7z/releases)
[![PyPI](https://img.shields.io/pypi/v/pybit7z)](https://pypi.org/project/pybit7z/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybit7z)](https://pypi.org/project/pybit7z/)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![clang-format](https://img.shields.io/badge/clang--format-enabled-blue)](https://github.com/pre-commit/mirrors-clang-format)
[![cmake-format](https://img.shields.io/badge/cmake--format-enabled-blue)](https://github.com/cheshirekow/cmake-format-precommit)
[![codespell](https://img.shields.io/badge/codespell-enabled-blue)](https://github.com/codespell-project/codespell)
[![markdownlint](https://img.shields.io/badge/markdownlint-enabled-blue)](https://github.com/igorshubovych/markdownlint-cli)
[![shellcheck](https://img.shields.io/badge/shellcheck-enabled-blue)](https://github.com/shellcheck-py/shellcheck-py)

## Features

- **Compression & extraction** of 7z, zip, tar, gzip, bzip2, xz, wim archives (writing); reading support for 60+ formats (rar, iso, cab, chm, nsis, vmdk, vhdx, squashfs, and more).
- **Bundled external plugins** — zstd, brotli, lz4, lz5, lizard, flzma2, bsc, and zpaq codecs/formats are packaged with the wheel and loaded automatically.
- **In-memory operations** — compress/extract directly to/from `bytes` buffers and strings.
- **Archive metadata** — inspect items count, sizes, CRC, per-item properties, wildcard item matching (`items_matching`), common root folder (`root_folder`), and property availability (`item_has_property`).
- **Nested archive reading** — `BitNestedArchiveReader` opens an archive embedded inside another (e.g. tar inside tar.gz).
- **Lazy library loading** — `Bit7zLibraryLoader` for explicit load/try-load/unload control, plus a `loader_context()` manager that auto-unloads on exit.
- **Encryption** — password-protected archives with optional header encryption (7z).
- **Solid archives, multi-volume splitting, compression levels & methods**, custom dictionary/word sizes, multi-threading.
- **Command-line interface** — `pybit7z` CLI for compress / decompress / extract / list / test / info / update.
- **Python 3.9+** on Windows, macOS, and Linux (including musllinux).

## Installation

Install from PyPI:

```bash
pip install pybit7z
```

## Quick Start

All operations require a `Bit7zLibrary` instance. Use the `lib7zip_context()` context manager, which locates the bundled `lib7zip` automatically:

```python
import pybit7z

with pybit7z.lib7zip_context() as lib:
    ...
```

For more control over the library lifecycle — e.g. probing whether 7-zip is available without raising, loading a custom build, or deferring the load — use `loader_context()`. It yields a fresh `Bit7zLibraryLoader`; call `load()` or `try_load()` yourself, and the manager unloads automatically on exit:

```python
import pybit7z

with pybit7z.loader_context() as loader:
    # Safe probe — never raises if the library is missing
    if loader.try_load(pybit7z.default_lib7zip()):
        lib = loader.library()
        ...
    else:
        print("lib7zip unavailable, skipping")
# loader.unload() called automatically on exit (if loaded)
```

### Loading External Plugins

The bundled external codecs and format handlers (zstd, brotli, lz4, ...) are **not** loaded automatically by `lib7zip_context()`. Call `load_plugins()` with the plugin directory to register them. For each supplied path the library scans the `Codecs/` subfolder first, then the `Formats/` subfolder.

```python
import pybit7z

with pybit7z.lib7zip_context() as lib:
    # Load the plugins bundled with the package
    lib.load_plugins([pybit7z.default_plugin_dir()])

    # Multiple directories can be supplied; results are accumulated
    # lib.load_plugins([pybit7z.default_plugin_dir(), "/path/to/more/plugins"])
```

### Extract Files from an Archive

```python
import pybit7z

try:
    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
        extractor.extract("path/to/archive.7z", "out/dir/")

        # Extracting a specific file inside an archive
        extractor.extract_matching("path/to/archive.7z", "file.pdf", "out/dir/")

        # Extracting the first file of an archive to a buffer
        buffer: bytes = extractor.extract("path/to/archive.7z")

        # Extracting an encrypted archive
        extractor.set_password("password")
        extractor.extract("path/to/another/archive.7z", "out/dir/")
except pybit7z.BitException as e:
    ...  # handle the exception
```

Work on a single archive:

```python
import pybit7z

try:
    with pybit7z.lib7zip_context() as lib:
        # Opening the archive
        archive = pybit7z.BitArchiveReader(lib, "path/to/archive.gz", pybit7z.FormatGZip)

        # Testing the archive
        archive.test()

        # Extracting the archive
        archive.extract_to("out/dir/")
except pybit7z.BitException as e:
    ...  # handle the exception
```

### Compress Files into an Archive

```python
import pybit7z

try:
    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)

        files = ["path/to/file1.jpg", "path/to/file2.pdf"]

        # Creating a simple zip archive
        compressor.compress(files, "output_archive.zip")

        # Creating a zip archive with a custom directory structure
        files_map: dict[str, str] = {
            "path/to/file1.jpg": "alias/path/file1.jpg",
            "path/to/file2.pdf": "alias/path/file2.pdf",
        }
        compressor.compress(files_map, "output_archive2.zip")

        # Compressing a directory
        compressor.compress_directory("dir/path/", "dir_archive.zip")

        # Creating an encrypted zip archive of two files
        compressor.set_password("password")
        compressor.compress_files(files, "protected_archive.zip")

        # Updating an existing zip archive
        compressor.set_update_mode(pybit7z.UpdateMode.Append)
        compressor.compress_files(files, "existing_archive.zip")

        # Compressing a single file into a buffer
        compressor2 = pybit7z.BitFileCompressor(lib, pybit7z.FormatBZip2)
        buffer: bytes = compressor2.compress_file(files[0])
except pybit7z.BitException as e:
    ...  # handle the exception
```

Work on a single archive:

```python
import pybit7z

try:
    with pybit7z.lib7zip_context() as lib:
        archive = pybit7z.BitArchiveWriter(lib, pybit7z.FormatSevenZip)

        # Adding the items to be compressed (no compression is performed here)
        archive.add_file("path/to/file.txt")
        archive.add_directory("path/to/dir/")

        # Compressing the added items to the output archive
        archive.compress_to("output.7z")
except pybit7z.BitException as e:
    ...  # handle the exception
```

### Read Archive Metadata

```python
import pybit7z

try:
    with pybit7z.lib7zip_context() as lib:
        arc = pybit7z.BitArchiveReader(lib, "archive.7z", pybit7z.FormatSevenZip)

        # Printing archive metadata
        print(
            "Archive properties:",
            "\n  Items count: ", arc.items_count(),
            "\n  Folders count: ", arc.folders_count(),
            "\n  Files count: ", arc.files_count(),
            "\n  Size: ", arc.size(),
            "\n  Packed size: ", arc.pack_size(),
        )

        # Printing the metadata of the archived items
        print("Archived items")
        for item in arc:
            print(
                "    Item index: ", item.index(),
                "\n    Name: ", item.name(),
                "\n    Extension: ", item.extension(),
                "\n    Path: ", item.path(),
                "\n    IsDir: ", item.is_dir(),
                "\n    Size: ", item.size(),
                "\n    Packed size: ", item.pack_size(),
                "\n    CRC: ", item.crc(),
            )

        # Wildcard-match items by pattern
        txt_files = list(arc.items_matching("*.txt"))

        # Common root folder of all items (empty string if none)
        print("Root folder:", arc.root_folder())

        # Check whether an item exposes a given property
        if arc.item_has_property(0, pybit7z.BitProperty.Size):
            size = arc.item_at(0).item_property(pybit7z.BitProperty.Size)

        # Item native/raw name accessors
        item = arc.item_at(0)
        print("Native name:", item.native_name())
        print("Raw path:", item.raw_path())
except pybit7z.BitException as e:
    ...  # handle the exception
```

A complete API reference is available in the [documentation](https://msclock.github.io/pybit7z/api/).

## Command-Line Interface

`pybit7z` ships a command-line tool for everyday archive tasks:

```bash
# Compress
pybit7z compress file.txt -o out.7z
pybit7z compress dir/ -o out.zip -f zip -l Ultra

# Extract
pybit7z extract archive.7z -o out_dir/
pybit7z decompress archive.tar.gz -o out_dir/

# List / test
pybit7z list archive.7z
pybit7z test archive.7z

# Show supported formats and codecs
pybit7z info
```

The bundled external codecs and formats are loaded automatically. To load
additional plugins from custom directories, use the `--plugin-dir` option
(can be repeated). Each directory is scanned for `Codecs/` and `Formats/`
subfolders:

```bash
pybit7z compress file.txt -o out.zst --plugin-dir /path/to/plugins
```

Run `pybit7z --help` for the full option list (passwords, compression method, threads, volumes, filtering, stdin/stdout piping, and more).

## Supported Formats & Codecs

pybit7z bundles the full 7-zip format/codec set plus additional external plugins.
Run `pybit7z info` to see the exact list available in your build.

### Writable formats

`7z`, `zip`, `tar`, `gzip`, `bzip2`, `xz`, `wim`

### Readable formats (60+)

`7z`, `zip`, `tar`, `gzip`, `bzip2`, `xz`, `z`, `lzma`, `lzma86`, `apfs`, `arj`, `cab`, `chm`, `cpio`, `cramfs`, `dmg`, `elf`, `ext`, `fat`, `flv`, `gpt`, `hfs`, `ihex`, `iso`, `lzh`, `macho`, `mbr`, `mslz`, `mub`, `ntfs`, `pe`, `coff`, `te`, `ppmd`, `qcow`, `rar`, `rar5`, `rpm`, `squashfs`, `swf`, `swfc`, `uefic`, `vdi`, `vhd`, `vhdx`, `vmdk`, `xar`, `udf`, `wim`, `nsis`, `split`, and more.

### Bundled external codecs & formats

| Plugin | Type | Description |
| --- | --- | --- |
| **zstd** | format + codec | Zstandard compression |
| **brotli** | format + codec | Brotli compression |
| **lz4** | format + codec | LZ4 compression |
| **lz5** | format + codec | LZ5 compression |
| **lizard** | format + codec | Lizard (LZ5) compression |
| **flzma2** | codec | Fast LZMA2 |
| **bsc** | codec | BSC (libbsc) compression |
| **zpaq** | codec | ZPAQ compression |

These are packaged inside the wheel under the package's `Codecs/` and
`Formats/` subdirectories. Call `lib.load_plugins([pybit7z.default_plugin_dir()])`
to load them (the CLI does this automatically); no extra installation is required.

## Building from Source

The build uses [scikit-build-core](https://github.com/scikit-build/scikit-build-core) + CMake + [vcpkg](https://vcpkg.io) (with custom overlay ports for bit7z and the external codec plugins).

### Prerequisites

- Python 3.9+
- CMake &ge; 3.20
- Ninja
- A C++17 compiler (MSVC on Windows, GCC/Clang on Linux/macOS)
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Build

```bash
# Editable install with verbose build output
uv pip install -e . -v
```

The build downloads and compiles 7-zip, bit7z, and the bundled codec plugins via vcpkg. This may take several minutes the first time.

### Running tests

```bash
uv pip install -e ".[test]"
pytest
```

## Development

The project uses [pre-commit](https://pre-commit.com) hooks for linting and formatting:

```bash
pre-commit install
pre-commit run -a
```

## License

Apache Software License 2.0, for more details, see the [LICENSE](https://github.com/msclock/pybit7z/blob/master/LICENSE) file.
