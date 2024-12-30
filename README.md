# pybit7z

<!-- SPHINX-START -->

A wrapper based on bit7z.

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

<!-- writes more things here -->

## Installation

Package-built has uploaded to pypi and just install with the command:

```bash
pip install pybit7z
```

## Example

### Extract Files from an Archive

```python
from pybit7z import core

try:
    extractor = core.Extractor(core.FormatSevenZip)
    extractor.extract("path/to/archive.7z", "out/dir/")

    # Extracting a specific file inside an archive
    extractor.extractMatching("path/to/archive.7z", "file.pdf", "out/dir/")

    # Extracting the first file of an archive to a buffer
    buffer: bytes = extractor.extract("path/to/archive.7z")

    # Extracting an encrypted archive
    extractor.set_password("password")
    extractor.extract("path/to/another/archive.7z", "out/dir/")
except core.BitException as e:
    ... # handle the exception
```

Work on a single archive:

```python
from pybit7z import core

try:
    # Opening the archive
     archive = core.Bit7zArchiveReader("path/to/archive.gz", BitFormat::GZip)

    # Testing the archive
    archive.test()

    # Extracting the archive
    archive.extract_to("out/dir/")
except core.BitException as e:
    ... # handle the exception
```

### Compress Files into an Archive

```python
from pybit7z import core

try:
    compressor = core.BitFileCompressor(core.FormatSevenZip)

    files = ["path/to/file1.jpg", "path/to/file2.pdf"]

    # Creating a simple zip archive
    compressor.compress(files, "output_archive.zip")

    # Creating a zip archive with a custom directory structure
    files_map: dict[str, str] = {
        "path/to/file1.jpg": "alias/path/file1.jpg",
        "path/to/file2.pdf": "alias/path/file2.pdf"
    }
    compressor.compress(files_map, "output_archive2.zip")

    # Compressing a directory
    compressor.compress_directory("dir/path/", "dir_archive.zip")

    # Creating an encrypted zip archive of two files
    compressor.set_password("password")
    compressor.compress_files(files, "protected_archive.zip")

    # Updating an existing zip archive
    compressor.set_update_mode(core.UpdateMode::Append)
    compressor.compress_files(files, "existing_archive.zip")

    # Compressing a single file into a buffer
    compressor2 = core.BitFileCompressor(BitFormat::BZip2)
    buffer: bytes = compressor2.compressFile(files[0])
except core.BitException as e:
    ... # handle the exception
```

Work on a single archive:

```python
from pybit7z import core

try:
    archive = core.BitArchiveWriter(core.BitFormat::SevenZip)

    # Adding the items to be compressed (no compression is performed here)
    archive.add_file("path/to/file.txt")
    archive.add_directory("path/to/dir/")

    # Compressing the added items to the output archive
    archive.compress_to("output.7z")
except core.BitException as e:
    ... # handle the exception
```

### Read Archive Metadata

```python
from pybit7z import core

try:
    arc = core.BitArchiveReader("archive.7z", core.BitFormat::SevenZip)

    # Printing archive metadata
    print("Archive properties:",
        "\n  Items count: "   , arc.items_count()
        "\n  Folders count: " , arc.folders_count()
        "\n  Files count: "   , arc.files_count()
        "\n  Size: "          , arc.size()
        "\n  Packed size: "   , arc.pack_size())

    # Printing the metadata of the archived items
    print("Archived items")
    for item in arc:
        print("    Item index: "    , item.index(),
            "\n    Name: "          , item.name(),
            "\n    Extension: "     , item.extension(),
            "\n    Path: "          , item.path(),
            "\n    IsDir: "         , item.is_dir(),
            "\n    Size: "          , item.size(),
            "\n    Packed size: "   , item.pack_size(),
            "\n    CRC: "           , item.crc())
except core.BitException as e:
    ... # handle the exception
```

A complete API reference is available in the [documentation](https://msclock.github.io/pybit7z/api/).


## License

Apache Software License, for more details, see the [LICENSE](https://github.com/msclock/pybit7z/blob/master/LICENSE) file.
