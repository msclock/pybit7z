from __future__ import annotations

import datetime
import random
import string
import tempfile
from pathlib import Path

import pytest

from pybit7z import core


@pytest.fixture
def temp_dir():
    """Fixture to provide temporary directory"""
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)
    except Exception:
        ...  # Ignore errors from cleanup


@pytest.fixture
def large_file(temp_dir):
    """Fixture to create a large test file (10MB)"""
    file_path: Path = temp_dir / "large_file.dat"
    size_mb = 10
    chunk_size = 1024 * 1024  # 1MB chunks

    with file_path.open("wb") as f:
        for _ in range(size_mb):
            data = "".join(
                random.choices(string.ascii_letters + string.digits, k=chunk_size)
            ).encode()
            f.write(data)

    return file_path


def test_format():
    """Test format from bit7z"""
    assert core.FormatSevenZip.extension().endswith(".7z")
    assert core.FormatSevenZip != core.FormatZip
    assert core.FormatSevenZip == core.FormatSevenZip
    assert core.FormatSevenZip.has_feature(core.FormatFeatures.CompressionLevel)
    assert core.FormatSevenZip.has_feature(core.FormatFeatures.Encryption)
    assert core.FormatSevenZip.has_feature(core.FormatFeatures.MultipleFiles)
    assert core.FormatSevenZip.has_feature(core.FormatFeatures.HeaderEncryption)
    assert core.FormatSevenZip.has_feature(core.FormatFeatures.SolidArchive)


def test_format_features():
    """Test format features detection"""
    fmt_7z = core.FormatSevenZip
    assert isinstance(fmt_7z, core.BitInOutFormat)

    # Test format properties
    assert fmt_7z.has_feature(core.FormatFeatures.CompressionLevel)
    assert fmt_7z.has_feature(core.FormatFeatures.Encryption)
    assert fmt_7z.has_feature(core.FormatFeatures.MultipleFiles)

    assert fmt_7z.extension() == ".7z"


def test_basic_compression(temp_dir):
    """Test basic file compression using BitFileCompressor"""
    # Create a test file
    test_file: Path = temp_dir / "test.txt"
    test_file.write_text("Hello, bit7z!")

    # Create output archive path
    archive_path: Path = temp_dir / "test.7z"

    # Create a compressor for 7z format
    compressor = core.BitFileCompressor(core.FormatSevenZip)

    # Set compression options
    compressor.set_compression_level(core.BitCompressionLevel.Normal)
    compressor.set_compression_method(core.BitCompressionMethod.Lzma2)

    # Compress the file
    compressor.compress_files([str(test_file)], str(archive_path))

    assert archive_path.exists(), "Archive was not created"
    assert archive_path.stat().st_size > 0, "Archive is empty"


def test_archive_extraction(temp_dir):
    """Test archive extraction using BitFileExtractor"""
    # Create a test archive first
    test_file = temp_dir / "test.txt"
    test_file.write_text("Hello from bit7z!")

    archive_path = temp_dir / "test.7z"
    compressor = core.BitFileCompressor(core.FormatSevenZip)
    compressor.compress([str(test_file)], str(archive_path))

    # Now extract it to a different directory
    extract_dir: Path = temp_dir / "extracted"
    extract_dir.mkdir()

    extractor = core.BitFileExtractor(core.FormatSevenZip)
    extractor.extract(str(archive_path), str(extract_dir))

    # Verify extraction
    extracted_file: Path = extract_dir / "test.txt"
    assert extracted_file.exists(), "File was not extracted"
    assert (
        extracted_file.read_text() == "Hello from bit7z!"
    ), "Extracted content doesn't match"


def test_error_handling(temp_dir):
    """Test error handling and exceptions"""
    # Test non-existent file
    nonexistent_file = temp_dir / "nonexistent.txt"
    archive_path = temp_dir / "test.7z"

    compressor = core.BitFileCompressor(core.FormatSevenZip)

    with pytest.raises(core.BitException):
        compressor.compress([str(nonexistent_file)], str(archive_path))

    # Test invalid password extraction
    test_file: Path = temp_dir / "secret.txt"
    test_file.write_text("Secret content")

    # Create password-protected archive
    compressor.set_password("correct_password")
    compressor.compress([str(test_file)], str(archive_path))

    extract_dir: Path = temp_dir / "extracted"
    extract_dir.mkdir()

    extractor = core.BitFileExtractor(core.FormatSevenZip)
    extractor.set_password("wrong_password")

    with pytest.raises(core.BitException, match="wrong password"):
        extractor.extract(str(archive_path), str(extract_dir))


def test_large_file_handling(temp_dir, large_file):
    """Test handling of large files"""

    # Test different compression levels with large file
    for level in [
        core.BitCompressionLevel.Fastest,
        core.BitCompressionLevel.Normal,
        core.BitCompressionLevel.Max,
    ]:
        level_archive = temp_dir / f"large_{level}.7z"
        compressor = core.BitFileCompressor(core.FormatSevenZip)
        compressor.set_compression_level(level)

        compressor.compress([str(large_file)], str(level_archive))
        assert (
            level_archive.exists()
        ), f"Large file archive not created for level {level}"

    # Extract and verify
    for level in [
        core.BitCompressionLevel.Fastest,
        core.BitCompressionLevel.Normal,
        core.BitCompressionLevel.Max,
    ]:
        level_archive = temp_dir / f"large_{level}.7z"
        extract_dir: Path = temp_dir / "extracted_large"

        extractor = core.BitFileExtractor(core.FormatSevenZip)
        extractor.extract(str(level_archive), str(extract_dir))

        extracted_file: Path = extract_dir / large_file.name
        assert extracted_file.exists(), "Large file was not extracted"
        assert (
            extracted_file.stat().st_size == large_file.stat().st_size
        ), "Extracted file size mismatch"


def test_multi_file_archive(temp_dir):
    """Test creating and extracting multi-file archives"""
    # Create multiple test files
    files_data = {
        "text1.txt": "Content 1",
        "text2.txt": "Content 2",
        "subdir/text3.txt": "Content 3",
        "subdir/text4.txt": "Content 4",
    }

    for file_path, content in files_data.items():
        full_path: Path = temp_dir / file_path
        full_path.parent.mkdir(exist_ok=True)
        full_path.write_text(content)

    # Create archive
    archive_path = temp_dir / "multi.7z"
    compressor = core.BitFileCompressor(core.FormatSevenZip)
    compressor.compress([str(temp_dir)], str(archive_path))

    # Extract to new location
    extract_dir = temp_dir / "extracted_multi"
    extractor = core.BitFileExtractor(core.FormatSevenZip)
    extractor.extract(str(archive_path), str(extract_dir))

    # Verify all files
    for file_path, content in files_data.items():
        extracted_file: Path = extract_dir / temp_dir.name / file_path
        assert extracted_file.exists(), f"File {file_path} not extracted"
        assert extracted_file.read_text() == content, f"Content mismatch in {file_path}"


def test_compression_methods_comparison(temp_dir, large_file):
    """Test and compare different compression methods"""
    methods = [
        core.BitCompressionMethod.Lzma2,
        core.BitCompressionMethod.Lzma,
        core.BitCompressionMethod.BZip2,
        core.BitCompressionMethod.Copy,
    ]

    results = {}
    for method in methods:
        archive_path: Path = temp_dir / f"test_{method}.7z"
        compressor = core.BitFileCompressor(core.FormatSevenZip)
        compressor.set_compression_method(method)

        compressor.compress([str(large_file)], str(archive_path))
        results[method] = archive_path.stat().st_size

    # Verify that COPY method creates the largest archive
    assert results[core.BitCompressionMethod.Copy] >= max(
        size
        for method, size in results.items()
        if method != core.BitCompressionMethod.Copy
    ), "COPY method should create the largest archive"


def test_archive_metadata(temp_dir):
    """Test archive metadata and properties"""
    # Create test file with known timestamp
    test_file: Path = temp_dir / "test.txt"
    test_file.write_text("Test content")

    archive_path = temp_dir / "test.7z"
    compressor = core.BitFileCompressor(core.FormatSevenZip)
    compressor.compress([str(test_file)], str(archive_path))

    # Read archive
    reader = core.BitArchiveReader(str(archive_path), core.FormatAuto)
    items = reader.items()

    assert len(items) == 1, "Expected exactly one item in archive"
    item = items[0]

    # Check metadata
    assert item.name() == "test.txt"
    assert item.size() > 0
    assert not item.is_dir()
    assert item.crc()

    # Time values should be reasonable
    assert isinstance(item.creation_time(), datetime.datetime)
    assert isinstance(item.last_write_time(), datetime.datetime)

    # Extract and terminate holded resources
    extracted_dir = temp_dir / "extracted"
    reader.extract_to(str(extracted_dir))


def test_mem_to_bytes():
    """Test stream compression and extraction"""
    # Save compressed data
    test_data = b"Stream compression test data" * 1000

    # Compress to memory
    mem_compressor = core.BitMemCompressor(core.FormatSevenZip)
    compressed_data = mem_compressor.compress_file(test_data)

    # Extract to memory
    mem_extractor = core.BitMemExtractor(core.FormatSevenZip)
    extracted_data = mem_extractor.extract(compressed_data)

    assert (
        extracted_data["[Content]"] == test_data
    ), "Stream compression/extraction failed"
    assert len(compressed_data) < len(test_data), "Compression did not reduce data size"


def test_different_formats(temp_dir):
    """Test compression with different archive formats"""
    test_file: Path = temp_dir / "test.txt"
    test_file.write_text("Testing different formats")

    formats = [
        (core.FormatSevenZip, "test.7z"),
        (core.FormatZip, "test.zip"),
        (core.FormatBZip2, "test.txt.bz2"),
        (core.FormatGZip, "test.gz"),
    ]

    for format_type, filename in formats:
        archive_path: Path = temp_dir / filename
        compressor = core.BitFileCompressor(format_type)
        compressor.compress([str(test_file)], str(archive_path))

        assert archive_path.exists(), f"Archive {filename} was not created"
        assert (
            archive_path.suffix == format_type.extension()
        ), f"Wrong extension for {filename}"

        # Test extraction
        extract_dir = temp_dir / f"extracted_{filename}"

        extractor = core.BitFileExtractor(format_type)
        extractor.extract(str(archive_path), str(extract_dir))

        extracted_file: Path = extract_dir / "test.txt"
        assert extracted_file.exists(), f"File was not extracted from {filename}"
        assert (
            extracted_file.read_text() == "Testing different formats"
        ), f"Content mismatch in {filename}"
