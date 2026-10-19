from __future__ import annotations

import tempfile
from importlib.metadata import distribution
from pathlib import Path

import pytest

import pybit7z

_CODEC_NAMES = (
    "brotli",
    "flzma2",
    "lizard",
    "lz4",
    "lz5",
    "zstd",
    "bsc",
    "ZPAQ",
)

# Codecs that ship as standalone codec DLLs in the Codecs/ folder.
_CODEC_ONLY_NAMES = ("flzma2", "bsc", "zpaq")

# Codecs whose codec entry points are bundled inside the format DLL in Formats/.
_FORMAT_BUNDLED_CODEC_NAMES = ("zstd", "brotli", "lz4", "lz5", "lizard")

EXPECTED_CODEC_FILES = {f"{name.lower()}" for name in _CODEC_ONLY_NAMES}


def _codecs_dir() -> Path:
    package_dir = Path(str(distribution("pybit7z").locate_file("pybit7z")))
    return package_dir / "Codecs"


def _formats_dir() -> Path:
    package_dir = Path(str(distribution("pybit7z").locate_file("pybit7z")))
    return package_dir / "Formats"


@pytest.fixture
def codecs_dir() -> Path:
    return _codecs_dir()


@pytest.fixture
def sample_text_file(tmp_path: Path) -> Path:
    f = tmp_path / "hello.txt"
    f.write_text("Hello, external codecs and formats ! " * 200)
    return f


@pytest.fixture
def sample_binary_file(tmp_path: Path) -> Path:
    f = tmp_path / "binary.bin"
    f.write_bytes(bytes(range(256)) * 100)
    return f


@pytest.fixture
def formats_dir() -> Path:
    return _formats_dir()


@pytest.fixture
def lib_with_codecs(codecs_dir: Path, formats_dir: Path):
    with pybit7z.lib7zip_context() as lib:
        lib.load_plugins(str(codecs_dir), str(formats_dir))
        yield lib


def _roundtrip(
    lib,
    codec: str,
    files: list[Path],
    archive_path: Path,
    extract_dir: Path,
    level: pybit7z.BitCompressionLevel | int | None = None,
) -> None:
    _compress_with_codec(lib, codec, files, archive_path, level=level)
    assert archive_path.exists(), f"{codec}: archive was not created"
    assert archive_path.stat().st_size > 0, f"{codec}: archive is empty"
    _extract_archive(lib, archive_path, extract_dir)


def test_codecs_directory_exists(codecs_dir: Path):
    """The bundled Codecs directory must exist and contain the expected codec libraries."""
    assert codecs_dir.is_dir(), f"Codecs directory not found at {codecs_dir}"
    present = {f.name.lower().split(".")[0] for f in codecs_dir.glob("*")}
    missing = EXPECTED_CODEC_FILES - present
    assert not missing, f"Missing codec libraries: {sorted(missing)}"


def test_load_plugins_codecs_valid_path(codecs_dir: Path, formats_dir: Path):
    """Loading external codecs from the valid Codecs folder returns True."""
    with pybit7z.lib7zip_context() as lib:
        result = lib.load_plugins(str(codecs_dir), str(formats_dir))
        assert result is True


def test_load_plugins_codecs_nonexistent_path(codecs_dir: Path, formats_dir: Path):
    """Loading from non-existent folders returns False."""
    bad_codecs = codecs_dir.parent / "does_not_exist_codecs"
    bad_formats = formats_dir.parent / "does_not_exist_formats"
    with pybit7z.lib7zip_context() as lib:
        result = lib.load_plugins(str(bad_codecs), str(bad_formats))
        assert result is False


def test_load_plugins_codecs_empty_directory():
    """Loading from an empty directory returns False."""
    with tempfile.TemporaryDirectory() as empty_dir, pybit7z.lib7zip_context() as lib:
        result = lib.load_plugins(empty_dir, empty_dir)
        assert result is False


def test_load_plugins_codecs_path_is_file(tmp_path: Path):
    """Loading from a path that points to a file (not a directory) returns False."""
    a_file = tmp_path / "not_a_dir.txt"
    a_file.write_text("hello")
    with pybit7z.lib7zip_context() as lib:
        result = lib.load_plugins(str(a_file), str(a_file))
        assert result is False


def test_load_plugins_codecs_directory_without_dlls(tmp_path: Path):
    """Loading from a directory that has files but no codec libraries returns False."""
    (tmp_path / "readme.txt").write_text("no codecs here")
    with pybit7z.lib7zip_context() as lib:
        result = lib.load_plugins(str(tmp_path), str(tmp_path))
        assert result is False


def test_load_plugins_multiple_times(
    lib_with_codecs, codecs_dir: Path, formats_dir: Path
):
    """Calling load_plugins multiple times on the same library must not crash."""
    first = lib_with_codecs.load_plugins(str(codecs_dir), str(formats_dir))
    second = lib_with_codecs.load_plugins(str(codecs_dir), str(formats_dir))
    assert first is True
    assert second is True


def test_external_codecs_no_regression_7z(tmp_path: Path, lib_with_codecs):
    """After loading external codecs, standard 7z compression and extraction still works."""
    test_file = tmp_path / "data.txt"
    content = "External codecs regression check"
    test_file.write_text(content)
    archive_path = tmp_path / "test.7z"
    extract_dir = tmp_path / "extracted"

    compressor = pybit7z.BitFileCompressor(lib_with_codecs, pybit7z.FormatSevenZip)
    compressor.set_compression_level(pybit7z.BitCompressionLevel.Normal)
    compressor.set_compression_method(pybit7z.BitCompressionMethod.Lzma2)
    compressor.compress_files([str(test_file)], str(archive_path))

    extractor = pybit7z.BitFileExtractor(lib_with_codecs, pybit7z.FormatSevenZip)
    extractor.extract(str(archive_path), str(extract_dir))

    assert archive_path.exists()
    assert archive_path.stat().st_size > 0
    assert (extract_dir / test_file.name).read_text() == content


def test_external_codecs_zip_format_still_works(tmp_path: Path, lib_with_codecs):
    """After loading external codecs, creating/extracting a ZIP archive still works."""
    test_file = tmp_path / "zip_test.txt"
    test_file.write_text("zip with external codecs loaded")
    archive_path = tmp_path / "test.zip"
    extract_dir = tmp_path / "out"

    compressor = pybit7z.BitFileCompressor(lib_with_codecs, pybit7z.FormatZip)
    compressor.compress([str(test_file)], str(archive_path))

    extractor = pybit7z.BitFileExtractor(lib_with_codecs, pybit7z.FormatZip)
    extractor.extract(str(archive_path), str(extract_dir))

    assert (
        extract_dir / test_file.name
    ).read_text() == "zip with external codecs loaded"


def _compress_with_codec(
    lib,
    codec_name: str,
    files: list[Path],
    archive_path: Path,
    level: pybit7z.BitCompressionLevel | int | None = None,
) -> None:
    compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
    compressor.set_format_property("0", pybit7z.BitPropVariant(codec_name))
    if level is not None:
        compressor.set_compression_level(level)
    compressor.compress_files([str(f) for f in files], str(archive_path))


def _extract_archive(lib, archive_path: Path, extract_dir: Path) -> None:
    extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
    extractor.extract(str(archive_path), str(extract_dir))


@pytest.mark.parametrize("codec", _CODEC_NAMES)
def test_codec_roundtrip_single_file(
    codec: str, tmp_path: Path, lib_with_codecs, sample_text_file: Path
):
    """Each external codec must be able to compress and extract a single text file losslessly."""
    archive_path = tmp_path / f"test_{codec}.7z"
    extract_dir = tmp_path / "extracted"

    _roundtrip(lib_with_codecs, codec, [sample_text_file], archive_path, extract_dir)

    extracted = extract_dir / sample_text_file.name
    assert extracted.exists(), f"{codec}: extracted file not found"
    assert extracted.read_text() == sample_text_file.read_text(), (
        f"{codec}: extracted content does not match original"
    )


@pytest.mark.parametrize("codec", _CODEC_NAMES)
def test_codec_roundtrip_binary_file(
    codec: str, tmp_path: Path, lib_with_codecs, sample_binary_file: Path
):
    """Each external codec must handle binary data losslessly."""
    archive_path = tmp_path / f"binary_{codec}.7z"
    extract_dir = tmp_path / "extracted"

    _roundtrip(lib_with_codecs, codec, [sample_binary_file], archive_path, extract_dir)

    extracted = extract_dir / sample_binary_file.name
    assert extracted.exists(), f"{codec}: extracted binary file not found"
    assert extracted.read_bytes() == sample_binary_file.read_bytes(), (
        f"{codec}: extracted binary content does not match original"
    )


@pytest.mark.parametrize("codec", _CODEC_NAMES)
def test_codec_roundtrip_multiple_files(codec: str, tmp_path: Path, lib_with_codecs):
    """Each external codec must correctly compress and extract multiple files."""
    files = []
    for i in range(3):
        f = tmp_path / f"file_{i}.txt"
        f.write_text(f"Content of file {i}\n" * 50)
        files.append(f)

    archive_path = tmp_path / f"multi_{codec}.7z"
    extract_dir = tmp_path / "extracted"

    _roundtrip(lib_with_codecs, codec, files, archive_path, extract_dir)

    for f in files:
        extracted = extract_dir / f.name
        assert extracted.exists(), f"{codec}: {f.name} not found after extraction"
        assert extracted.read_text() == f.read_text(), (
            f"{codec}: {f.name} content mismatch"
        )


@pytest.mark.parametrize("codec", _CODEC_NAMES)
def test_codec_roundtrip_empty_file(codec: str, tmp_path: Path, lib_with_codecs):
    """Each external codec must handle empty files."""
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    archive_path = tmp_path / f"empty_{codec}.7z"
    extract_dir = tmp_path / "extracted"

    _roundtrip(lib_with_codecs, codec, [empty_file], archive_path, extract_dir)

    extracted = extract_dir / empty_file.name
    assert extracted.exists(), f"{codec}: empty file not found after extraction"
    assert extracted.read_text() == "", f"{codec}: extracted empty file is not empty"


_CODEC_LEVEL_RANGES: dict[str, tuple[int, int]] = {
    "zstd": (1, 22),
    "brotli": (0, 11),
    "lz4": (1, 12),
    "lz5": (1, 16),
    "flzma2": (1, 9),
    "lizard": (10, 49),
    "bsc": (1, 9),
    "ZPAQ": (1, 9),
}


def _codec_test_levels(codec: str) -> list[int]:
    min_l, max_l = _CODEC_LEVEL_RANGES[codec]
    if max_l - min_l <= 4:
        return list(range(min_l, max_l + 1))
    mid = (min_l + max_l) // 2
    return [min_l, min_l + 1, mid, max_l - 1, max_l]


_CODEC_LEVEL_PARAMS = [
    (codec, level) for codec in _CODEC_NAMES for level in _codec_test_levels(codec)
]


@pytest.mark.parametrize(("codec", "level"), _CODEC_LEVEL_PARAMS)
def test_codec_roundtrip_at_compression_levels(
    codec: str,
    level: int,
    tmp_path: Path,
    lib_with_codecs,
    sample_text_file: Path,
):
    """Each external codec must compress and extract correctly at its supported compression levels."""
    archive_path = tmp_path / f"{codec}_l{level}.7z"
    extract_dir = tmp_path / "extracted"

    _roundtrip(
        lib_with_codecs,
        codec,
        [sample_text_file],
        archive_path,
        extract_dir,
        level=level,
    )

    extracted = extract_dir / sample_text_file.name
    assert extracted.exists(), f"{codec} level={level}: extracted file not found"
    assert extracted.read_text() == sample_text_file.read_text(), (
        f"{codec} level={level}: extracted content does not match original"
    )


@pytest.mark.parametrize("codec", _CODEC_NAMES)
def test_codec_levels_produce_distinct_archives(
    codec: str,
    tmp_path: Path,
    lib_with_codecs,
    sample_text_file: Path,
):
    """Different compression levels should produce archives of different sizes (where applicable)."""
    min_l, max_l = _CODEC_LEVEL_RANGES[codec]
    if min_l == max_l:
        pytest.skip(f"{codec} has only one supported level")

    sizes = {}
    for level in (min_l, max_l):
        archive_path = tmp_path / f"{codec}_distinct_l{level}.7z"
        _compress_with_codec(
            lib_with_codecs, codec, [sample_text_file], archive_path, level=level
        )
        sizes[level] = archive_path.stat().st_size

    assert all(size > 0 for size in sizes.values())
    if len(set(sizes.values())) == 1:
        pytest.skip(f"{codec} produces same archive size at min and max levels")


# ---------------------------------------------------------------------------
# External archive format handler tests (zstd, brotli, lz4, lz5, lizard)
# ---------------------------------------------------------------------------

_EXTERNAL_FORMAT_NAMES = ("zstd", "brotli", "lz4", "lz5", "lizard")


@pytest.fixture
def lib_with_formats(codecs_dir: Path, formats_dir: Path):
    with pybit7z.lib7zip_context() as lib:
        lib.load_plugins(str(codecs_dir), str(formats_dir))
        yield lib


def test_formats_directory_exists(formats_dir: Path):
    """The bundled Formats directory must exist and contain the expected format handler DLLs."""
    assert formats_dir.is_dir(), f"Formats directory not found at {formats_dir}"
    present = {f.name.lower().split(".")[0] for f in formats_dir.glob("*")}
    expected = {f"{name}" for name in _EXTERNAL_FORMAT_NAMES}
    missing = expected - present
    assert not missing, f"Missing format handler libraries: {sorted(missing)}"


def test_load_plugins_valid_path(codecs_dir: Path, formats_dir: Path):
    """Loading external plugins from the valid Codecs/Formats folders returns True."""
    with pybit7z.lib7zip_context() as lib:
        result = lib.load_plugins(str(codecs_dir), str(formats_dir))
        assert result is True


def test_load_plugins_nonexistent_path(codecs_dir: Path, formats_dir: Path):
    """Loading from non-existent folders returns False."""
    bad_codecs = codecs_dir.parent / "does_not_exist_codecs"
    bad_formats = formats_dir.parent / "does_not_exist_formats"
    with pybit7z.lib7zip_context() as lib:
        result = lib.load_plugins(str(bad_codecs), str(bad_formats))
        assert result is False


def test_load_plugins_empty_directory():
    """Loading from empty directories returns False."""
    with tempfile.TemporaryDirectory() as empty_dir, pybit7z.lib7zip_context() as lib:
        result = lib.load_plugins(empty_dir, empty_dir)
        assert result is False


def test_external_formats_listed_in_get_formats(lib_with_formats):
    """All external formats must appear in the result of get_formats()."""
    names = {f.name for f in lib_with_formats.get_formats()}
    for name in _EXTERNAL_FORMAT_NAMES:
        assert name in names, f"External format '{name}' not found in get_formats()"


def test_get_external_in_out_format_returns_objects(lib_with_formats):
    """get_external_in_out_format must return a valid BitInOutFormat for each writable external format."""
    for name in _EXTERNAL_FORMAT_NAMES:
        fmt = lib_with_formats.get_external_in_out_format(name)
        assert fmt is not None, f"get_external_in_out_format('{name}') returned None"
        assert isinstance(fmt, pybit7z.BitInOutFormat)
        assert fmt.value() > 0, f"format '{name}' has invalid value"


def test_get_external_in_out_format_unknown_returns_none(lib_with_formats):
    """get_external_in_out_format must return None for an unknown format name."""
    assert (
        lib_with_formats.get_external_in_out_format("definitely_not_a_format") is None
    )


def test_get_external_in_out_format_builtin_returns_none(lib_with_formats):
    """Built-in formats (e.g. 7z, zip) must not be returned by get_external_in_out_format."""
    assert lib_with_formats.get_external_in_out_format("7z") is None
    assert lib_with_formats.get_external_in_out_format("zip") is None


def test_get_external_in_format_returns_objects(lib_with_formats):
    """get_external_in_format must return a valid BitInFormat for each external format."""
    for name in _EXTERNAL_FORMAT_NAMES:
        fmt = lib_with_formats.get_external_in_format(name)
        assert fmt is not None, f"get_external_in_format('{name}') returned None"
        assert isinstance(fmt, pybit7z.BitInFormat)


def test_get_external_in_format_unknown_returns_none(lib_with_formats):
    """get_external_in_format must return None for an unknown format name."""
    assert lib_with_formats.get_external_in_format("nope") is None


def _format_roundtrip(lib, format_name: str, src: Path, tmp_path: Path) -> Path:
    fmt = lib.get_external_in_out_format(format_name)
    ext = fmt.extension()
    archive = src.with_name(src.name + "." + ext)
    extract_dir = tmp_path / f"ext_{format_name}"

    compressor = pybit7z.BitFileCompressor(lib, fmt)
    compressor.compress_files([str(src)], str(archive))
    assert archive.exists()
    assert archive.stat().st_size > 0

    extractor = pybit7z.BitFileExtractor(lib, fmt)
    extractor.extract(str(archive), str(extract_dir))

    files = [f for f in extract_dir.rglob("*") if f.is_file()]
    assert len(files) == 1, f"expected exactly one extracted file, got {len(files)}"
    return files[0]


@pytest.mark.parametrize("format_name", _EXTERNAL_FORMAT_NAMES)
def test_external_format_roundtrip_text(
    format_name: str, tmp_path: Path, lib_with_formats, sample_text_file: Path
):
    """Each external format must compress and extract a text file losslessly."""
    extracted = _format_roundtrip(
        lib_with_formats, format_name, sample_text_file, tmp_path
    )
    assert extracted.read_text() == sample_text_file.read_text()


@pytest.mark.parametrize("format_name", _EXTERNAL_FORMAT_NAMES)
def test_external_format_roundtrip_binary(
    format_name: str, tmp_path: Path, lib_with_formats, sample_binary_file: Path
):
    """Each external format must compress and extract binary data losslessly."""
    extracted = _format_roundtrip(
        lib_with_formats, format_name, sample_binary_file, tmp_path
    )
    assert extracted.read_bytes() == sample_binary_file.read_bytes()


@pytest.mark.parametrize("format_name", _EXTERNAL_FORMAT_NAMES)
def test_external_format_roundtrip_empty_file(
    format_name: str, tmp_path: Path, lib_with_formats
):
    """Each external format must handle empty files correctly."""
    empty = tmp_path / "empty.txt"
    empty.write_text("")
    extracted = _format_roundtrip(lib_with_formats, format_name, empty, tmp_path)
    assert extracted.read_text() == ""


@pytest.mark.parametrize("format_name", _EXTERNAL_FORMAT_NAMES)
def test_external_format_produces_smaller_archive(
    format_name: str, lib_with_formats, sample_text_file: Path
):
    """Compressing a repetitive text file with an external format must produce a smaller archive."""
    fmt = lib_with_formats.get_external_in_out_format(format_name)
    ext = fmt.extension()
    archive = sample_text_file.with_name(sample_text_file.name + "." + ext)

    compressor = pybit7z.BitFileCompressor(lib_with_formats, fmt)
    compressor.compress_files([str(sample_text_file)], str(archive))

    assert archive.stat().st_size < sample_text_file.stat().st_size, (
        f"{format_name}: compressed size {archive.stat().st_size} >= original "
        f"{sample_text_file.stat().st_size}"
    )
