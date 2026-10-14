from __future__ import annotations

import datetime
import gc
from pathlib import Path

import pytest

import pybit7z


def test_format():
    """Test format from bit7z"""
    assert pybit7z.FormatSevenZip.extension().endswith(".7z")
    assert pybit7z.FormatSevenZip != pybit7z.FormatZip
    assert pybit7z.FormatSevenZip == pybit7z.FormatSevenZip
    assert pybit7z.FormatSevenZip.has_feature(pybit7z.FormatFeatures.CompressionLevel)
    assert pybit7z.FormatSevenZip.has_feature(pybit7z.FormatFeatures.Encryption)
    assert pybit7z.FormatSevenZip.has_feature(pybit7z.FormatFeatures.MultipleFiles)
    assert pybit7z.FormatSevenZip.has_feature(pybit7z.FormatFeatures.HeaderEncryption)
    assert pybit7z.FormatSevenZip.has_feature(pybit7z.FormatFeatures.SolidArchive)


def test_format_features():
    """Test format features detection"""
    fmt_7z = pybit7z.FormatSevenZip
    assert isinstance(fmt_7z, pybit7z.BitInOutFormat)

    # Test format properties
    assert fmt_7z.has_feature(pybit7z.FormatFeatures.CompressionLevel)
    assert fmt_7z.has_feature(pybit7z.FormatFeatures.Encryption)
    assert fmt_7z.has_feature(pybit7z.FormatFeatures.MultipleFiles)

    assert fmt_7z.extension() == ".7z"


def test_basic_compression(temp_dir):
    """Test basic file compression using BitFileCompressor"""
    # Create a test file
    test_file: Path = temp_dir / "test.txt"
    test_file.write_text("Hello, bit7z!")

    # Create output archive path
    archive_path: Path = temp_dir / "test.7z"

    with pybit7z.lib7zip_context() as lib:
        # Create a compressor for 7z format
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)

        # Set compression options
        compressor.set_compression_level(pybit7z.BitCompressionLevel.Normal)
        compressor.set_compression_method(pybit7z.BitCompressionMethod.Lzma2)

        # Compress the file
        compressor.compress_files([str(test_file)], str(archive_path))

    assert archive_path.exists(), "Archive was not created"
    assert archive_path.stat().st_size > 0, "Archive is empty"


def test_archive_extraction(temp_dir):
    """Test archive extraction using BitFileExtractor"""
    # Create a test archive first
    test_file: Path = temp_dir / "test.txt"
    test_file.write_text("Hello from bit7z!")

    archive_path = temp_dir / "test.7z"
    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
        compressor.compress([str(test_file)], str(archive_path))

        # Now extract it to a different directory
        extract_dir: Path = temp_dir / "extracted"
        extract_dir.mkdir()

        extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
        extractor.extract(str(archive_path), str(extract_dir))

    # Verify extraction
    extracted_file: Path = extract_dir / "test.txt"
    assert extracted_file.exists(), "File was not extracted"
    assert extracted_file.read_text() == "Hello from bit7z!", (
        "Extracted content doesn't match"
    )


def test_error_handling(temp_dir):
    """Test error handling and exceptions"""
    # Test non-existent file
    nonexistent_file = temp_dir / "nonexistent.txt"
    archive_path = temp_dir / "test.7z"

    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)

        with pytest.raises(pybit7z.BitException):
            compressor.compress([str(nonexistent_file)], str(archive_path))

        # Test invalid password extraction
        test_file: Path = temp_dir / "secret.txt"
        test_file.write_text("Secret content")

        # Create password-protected archive
        compressor.set_password("correct_password")
        compressor.compress([str(test_file)], str(archive_path))

        extract_dir: Path = temp_dir / "extracted"
        extract_dir.mkdir()

        extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
        extractor.set_password("wrong_password")

        with pytest.raises(pybit7z.BitException, match="wrong password"):
            extractor.extract(str(archive_path), str(extract_dir))


def test_large_file_handling(temp_dir, large_file):
    """Test handling of large files"""

    with pybit7z.lib7zip_context() as lib:
        # Test different compression levels with large file
        for level in [
            pybit7z.BitCompressionLevel.Fastest,
            pybit7z.BitCompressionLevel.Normal,
            pybit7z.BitCompressionLevel.Max,
        ]:
            level_archive = temp_dir / f"large_{level}.7z"
            compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
            compressor.set_compression_level(level)

            compressor.compress([str(large_file)], str(level_archive))
            assert level_archive.exists(), (
                f"Large file archive not created for level {level}"
            )

        # Extract and verify
        for level in [
            pybit7z.BitCompressionLevel.Fastest,
            pybit7z.BitCompressionLevel.Normal,
            pybit7z.BitCompressionLevel.Max,
        ]:
            level_archive = temp_dir / f"large_{level}.7z"
            extract_dir: Path = temp_dir / "extracted_large"

            extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
            extractor.extract(str(level_archive), str(extract_dir))

            extracted_file: Path = extract_dir / large_file.name
            assert extracted_file.exists(), "Large file was not extracted"
            assert extracted_file.stat().st_size == large_file.stat().st_size, (
                "Extracted file size mismatch"
            )


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

    with pybit7z.lib7zip_context() as lib:
        # Create archive
        archive_path = temp_dir / "multi.7z"
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
        compressor.compress([str(temp_dir)], str(archive_path))

        # Extract to new location
        extract_dir = temp_dir / "extracted_multi"
        extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
        extractor.extract(str(archive_path), str(extract_dir))

    # Verify all files
    for file_path, content in files_data.items():
        extracted_file: Path = extract_dir / temp_dir.name / file_path
        assert extracted_file.exists(), f"File {file_path} not extracted"
        assert extracted_file.read_text() == content, f"Content mismatch in {file_path}"


def test_compression_methods_comparison(temp_dir, large_file):
    """Test and compare different compression methods"""
    methods = [
        pybit7z.BitCompressionMethod.Lzma2,
        pybit7z.BitCompressionMethod.Lzma,
        pybit7z.BitCompressionMethod.BZip2,
        pybit7z.BitCompressionMethod.Copy,
    ]

    results = {}
    with pybit7z.lib7zip_context() as lib:
        for method in methods:
            archive_path: Path = temp_dir / f"test_{method}.7z"
            compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
            compressor.set_compression_method(method)

            compressor.compress([str(large_file)], str(archive_path))
            results[method] = archive_path.stat().st_size

    # Verify that COPY method creates the largest archive
    assert results[pybit7z.BitCompressionMethod.Copy] >= max(
        size
        for method, size in results.items()
        if method != pybit7z.BitCompressionMethod.Copy
    ), "COPY method should create the largest archive"


def test_archive_metadata(temp_dir):
    """Test archive metadata and properties"""
    # Create test file with known timestamp
    test_file: Path = temp_dir / "test.txt"
    test_file.write_text("Test content")

    archive_path = temp_dir / "test.7z"
    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
        compressor.compress([str(test_file)], str(archive_path))

        # Read archive
        reader = pybit7z.BitArchiveReader(lib, str(archive_path), pybit7z.FormatAuto)
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

        # Extract
        extracted_dir = temp_dir / "extracted"
        reader.extract_to(str(extracted_dir))


def test_mem_to_bytes():
    """Test stream compression and extraction"""
    # Save compressed data
    test_data = b"Stream compression test data" * 1000

    with pybit7z.lib7zip_context() as lib:
        # Compress to memory
        mem_compressor = pybit7z.BitMemCompressor(lib, pybit7z.FormatSevenZip)
        compressed_data = mem_compressor.compress_file(test_data)

        # Extract to memory
        mem_extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        extracted_data = mem_extractor.extract(compressed_data)

    assert extracted_data["[Content]"] == test_data, (
        "Stream compression/extraction failed"
    )
    assert len(compressed_data) < len(test_data), "Compression did not reduce data size"


def test_different_formats(temp_dir):
    """Test compression with different archive formats"""
    test_file: Path = temp_dir / "test.txt"
    test_file.write_text("Testing different formats")

    formats = [
        (pybit7z.FormatSevenZip, "test.7z"),
        (pybit7z.FormatZip, "test.zip"),
        (pybit7z.FormatBZip2, "test.txt.bz2"),
        (pybit7z.FormatGZip, "test.gz"),
    ]

    with pybit7z.lib7zip_context() as lib:
        for format_type, filename in formats:
            archive_path: Path = temp_dir / filename
            compressor = pybit7z.BitFileCompressor(lib, format_type)
            compressor.compress([str(test_file)], str(archive_path))

            assert archive_path.exists(), f"Archive {filename} was not created"
            assert archive_path.suffix == format_type.extension(), (
                f"Wrong extension for {filename}"
            )

            # Test extraction
            extract_dir = temp_dir / f"extracted_{filename}"

            extractor = pybit7z.BitFileExtractor(lib, format_type)
            extractor.extract(str(archive_path), str(extract_dir))

            extracted_file: Path = extract_dir / "test.txt"
            assert extracted_file.exists(), f"File was not extracted from {filename}"
            assert extracted_file.read_text() == "Testing different formats", (
                f"Content mismatch in {filename}"
            )


def test_archive_reader_bytes_input(temp_dir):
    """Test BitArchiveReader correctly dispatches the bytes (memory buffer) overload."""
    test_file: Path = temp_dir / "test.txt"
    test_content = "BitArchiveReader memory buffer test content"
    test_file.write_text(test_content)

    archive_path: Path = temp_dir / "test.7z"
    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
        compressor.compress([str(test_file)], str(archive_path))

        archive_bytes = archive_path.read_bytes()

        reader = pybit7z.BitArchiveReader(lib, archive_bytes, pybit7z.FormatSevenZip)

        items = reader.items()
        assert len(items) == 1, "Expected exactly one item in archive"
        assert reader.files_count() == 1
        assert items[0].name() == "test.txt"

        extracted = reader.extract_to()
        assert isinstance(extracted, dict), "extract_to() should return a dict"
        assert len(extracted) == 1
        assert next(iter(extracted.values())) == test_content.encode(), (
            "Extracted content from memory buffer does not match original"
        )


def test_archive_reader_str_input(temp_dir):
    """Test BitArchiveReader correctly dispatches the str (file path) overload."""
    test_file: Path = temp_dir / "test.txt"
    test_file.write_text("BitArchiveReader file path test content")

    archive_path: Path = temp_dir / "test.7z"
    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
        compressor.compress([str(test_file)], str(archive_path))

        reader = pybit7z.BitArchiveReader(
            lib, str(archive_path), pybit7z.FormatSevenZip
        )

        items = reader.items()
        assert len(items) == 1, "Expected exactly one item in archive"
        assert items[0].name() == "test.txt"

        extract_dir: Path = temp_dir / "extracted"
        reader.extract_to(str(extract_dir))

    extracted_file: Path = extract_dir / "test.txt"
    assert extracted_file.exists(), "File was not extracted"
    assert extracted_file.read_text() == "BitArchiveReader file path test content"


def test_is_header_encrypted_bytes_and_str(temp_dir):
    """Test is_header_encrypted dispatches correctly for both bytes and str inputs."""
    test_file: Path = temp_dir / "secret.txt"
    test_file.write_text("Encrypted content")

    archive_path: Path = temp_dir / "encrypted.7z"
    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
        compressor.set_password("secret")
        compressor.compress([str(test_file)], str(archive_path))

        archive_bytes = archive_path.read_bytes()

        str_result = pybit7z.BitArchiveReader.is_header_encrypted(
            lib, str(archive_path), pybit7z.FormatSevenZip
        )
        bytes_result = pybit7z.BitArchiveReader.is_header_encrypted(
            lib, archive_bytes, pybit7z.FormatSevenZip
        )

    assert isinstance(str_result, bool)
    assert isinstance(bytes_result, bool)
    assert str_result == bytes_result, (
        "is_header_encrypted should return the same result for str and bytes inputs"
    )


def test_archive_writer_bytes_input(temp_dir):
    """Test BitArchiveWriter correctly dispatches the bytes (memory buffer) overload."""
    test_file: Path = temp_dir / "test.txt"
    test_file.write_text("BitArchiveWriter memory buffer test content")

    archive_path: Path = temp_dir / "test.7z"
    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
        compressor.compress([str(test_file)], str(archive_path))

        archive_bytes = archive_path.read_bytes()

        writer = pybit7z.BitArchiveWriter(lib, archive_bytes, pybit7z.FormatSevenZip)

        assert writer.items_count() == 1, "Expected exactly one item in archive"

        output_bytes = writer.compress_to()
        assert isinstance(output_bytes, bytes)
        assert len(output_bytes) > 0


@pytest.fixture
def multi_file_archive_bytes(temp_dir):
    """Create a multi-file 7z archive in memory for extractor tests."""
    files = {
        "a.txt": b"content of file a",
        "b.txt": b"content of file b",
        "c.log": b"content of file c log",
    }
    for name, data in files.items():
        (temp_dir / name).write_bytes(data)

    archive_path = temp_dir / "multi.7z"
    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
        compressor.compress([str(temp_dir / f) for f in files], str(archive_path))

    return archive_path.read_bytes(), files


# ---------------------------------------------------------------------------
# BitMemExtractor: all zero-copy bytes overloads
# ---------------------------------------------------------------------------


def test_mem_extractor_extract_to_dict(multi_file_archive_bytes):
    archive_bytes, files = multi_file_archive_bytes
    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract(archive_bytes)

    assert isinstance(result, dict)
    for name, data in files.items():
        assert name in result
        assert result[name] == data


def test_mem_extractor_extract_to_dir(multi_file_archive_bytes, temp_dir):
    archive_bytes, files = multi_file_archive_bytes
    out_dir = temp_dir / "out"
    out_dir.mkdir()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        extractor.extract(archive_bytes, str(out_dir))

    for name, data in files.items():
        assert (out_dir / name).read_bytes() == data


def test_mem_extractor_extract_single_by_index(multi_file_archive_bytes):
    archive_bytes, files = multi_file_archive_bytes
    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        first_data = extractor.extract(archive_bytes, 0)

    assert first_data in files.values()


def test_mem_extractor_extract_matching_to_dir(multi_file_archive_bytes, temp_dir):
    archive_bytes, files = multi_file_archive_bytes
    out_dir = temp_dir / "out"
    out_dir.mkdir()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        extractor.extract_matching(archive_bytes, "*.txt", str(out_dir))

    assert (out_dir / "a.txt").read_bytes() == files["a.txt"]
    assert (out_dir / "b.txt").read_bytes() == files["b.txt"]
    assert not (out_dir / "c.log").exists()


def test_mem_extractor_extract_matching_to_bytes(multi_file_archive_bytes):
    archive_bytes, files = multi_file_archive_bytes
    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract_matching(
            archive_bytes, "*.txt", pybit7z.FilterPolicy.Include
        )

    assert result == files["b.txt"]


def test_mem_extractor_extract_items(multi_file_archive_bytes, temp_dir):
    archive_bytes, files = multi_file_archive_bytes
    out_dir = temp_dir / "out"
    out_dir.mkdir()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        extractor.extract_items(archive_bytes, [0, 2], str(out_dir))

    extracted = {p.name: p.read_bytes() for p in out_dir.iterdir() if p.is_file()}
    assert len(extracted) == 2
    for data in extracted.values():
        assert data in files.values()


def test_mem_extractor_extract_matching_regex_to_dir(
    multi_file_archive_bytes, temp_dir
):
    archive_bytes, files = multi_file_archive_bytes
    out_dir = temp_dir / "out"
    out_dir.mkdir()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        extractor.extract_matching_regex(archive_bytes, r".*\.log$", str(out_dir))

    assert (out_dir / "c.log").read_bytes() == files["c.log"]
    assert not (out_dir / "a.txt").exists()


def test_mem_extractor_extract_matching_regex_to_bytes(multi_file_archive_bytes):
    archive_bytes, files = multi_file_archive_bytes
    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract_matching_regex(
            archive_bytes, r".*\.log$", pybit7z.FilterPolicy.Include
        )

    assert result == files["c.log"]


def test_mem_extractor_test(multi_file_archive_bytes):
    archive_bytes, _ = multi_file_archive_bytes
    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        extractor.test(archive_bytes)


def test_mem_extractor_test_invalid():
    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        with pytest.raises(pybit7z.BitException):
            extractor.test(b"not a valid archive")


def test_mem_extractor_large_data():
    """Verify zero-copy path works for large data without extra copies."""
    test_data = bytes(range(256)) * 4000  # ~1 MB
    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitMemCompressor(lib, pybit7z.FormatSevenZip)
        compressed = compressor.compress_file(test_data)

        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract(compressed)

    assert result["[Content]"] == test_data


# ---------------------------------------------------------------------------
# BitMemCompressor: zero-copy bytes overloads
# ---------------------------------------------------------------------------


def test_mem_compressor_to_file(temp_dir):
    test_data = b"BitMemCompressor to file test data" * 100
    out_file = temp_dir / "out.7z"

    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitMemCompressor(lib, pybit7z.FormatSevenZip)
        compressor.compress_file(test_data, str(out_file))

    assert out_file.exists()
    assert out_file.stat().st_size > 0

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract(str(out_file))

    assert next(iter(result.values())) == test_data


def test_mem_compressor_to_bytes():
    test_data = b"BitMemCompressor to bytes test data" * 100
    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitMemCompressor(lib, pybit7z.FormatSevenZip)
        compressed = compressor.compress_file(test_data)

    assert isinstance(compressed, bytes)
    assert len(compressed) > 0
    assert len(compressed) < len(test_data)


# ---------------------------------------------------------------------------
# BitOutputArchive.add_file(bytes, name)
# ---------------------------------------------------------------------------


def test_output_archive_add_file_to_bytes():
    data1 = b"data for file one" * 50
    data2 = b"data for file two" * 50

    with pybit7z.lib7zip_context() as lib:
        writer = pybit7z.BitArchiveWriter(lib, pybit7z.FormatSevenZip)
        writer.add_file(data1, "one.bin")
        writer.add_file(data2, "two.bin")
        archive_bytes = writer.compress_to()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract(archive_bytes)

    assert result["one.bin"] == data1
    assert result["two.bin"] == data2


def test_output_archive_add_file_to_file(temp_dir):
    data = b"output archive add file to disk" * 50
    out_file = temp_dir / "out.7z"

    with pybit7z.lib7zip_context() as lib:
        writer = pybit7z.BitArchiveWriter(lib, pybit7z.FormatSevenZip)
        writer.add_file(data, "payload.bin")
        writer.compress_to(str(out_file))

    assert out_file.exists()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract(str(out_file))

    assert next(iter(result.values())) == data


def test_output_archive_add_file_lifetime_survives_gc():
    """CRITICAL: bytes passed to add_file must remain valid until compress_to.

    The old implementation copied bytes into a local vector that was destroyed
    when add_file returned, leaving a dangling reference inside the archive.
    This test drops the Python bytes reference and forces GC before compress_to
    to prove the new keep_alive + capsule mechanism keeps the data alive.
    """
    data = b"lifetime test payload" * 100

    with pybit7z.lib7zip_context() as lib:
        writer = pybit7z.BitArchiveWriter(lib, pybit7z.FormatSevenZip)
        payload = bytes(data)  # own reference
        writer.add_file(payload, "payload.bin")
        del payload
        gc.collect()
        # At this point the only thing keeping the bytes alive is keep_alive.
        archive_bytes = writer.compress_to()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract(archive_bytes)

    assert result["payload.bin"] == data


def test_output_archive_add_multiple_files_lifetime():
    """Multiple add_file calls with bytes that go out of scope before compress_to."""
    with pybit7z.lib7zip_context() as lib:
        writer = pybit7z.BitArchiveWriter(lib, pybit7z.FormatSevenZip)
        for i in range(5):
            payload = bytes(f"file-{i}-content-{i}".encode()) * 30
            writer.add_file(payload, f"file_{i}.txt")
            del payload
        gc.collect()
        archive_bytes = writer.compress_to()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitMemExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract(archive_bytes)

    for i in range(5):
        assert result[f"file_{i}.txt"] == bytes(f"file-{i}-content-{i}".encode()) * 30


# ---------------------------------------------------------------------------
# BitArchiveEditor.update_item(bytes)
# ---------------------------------------------------------------------------


@pytest.fixture
def editable_archive(temp_dir):
    """Create a 7z archive on disk that can be opened with BitArchiveEditor."""
    test_file = temp_dir / "original.txt"
    test_file.write_bytes(b"original content")

    archive_path = temp_dir / "edit.7z"
    with pybit7z.lib7zip_context() as lib:
        compressor = pybit7z.BitFileCompressor(lib, pybit7z.FormatSevenZip)
        compressor.compress([str(test_file)], str(archive_path))

    return archive_path


def test_editor_update_item_by_index(editable_archive):
    new_data = b"updated content via index"

    with pybit7z.lib7zip_context() as lib:
        editor = pybit7z.BitArchiveEditor(
            lib, str(editable_archive), pybit7z.FormatSevenZip
        )
        editor.update_item(0, new_data)
        editor.apply_changes()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract(str(editable_archive))

    assert next(iter(result.values())) == new_data


def test_editor_update_item_by_path(editable_archive):
    new_data = b"updated content via path"

    with pybit7z.lib7zip_context() as lib:
        editor = pybit7z.BitArchiveEditor(
            lib, str(editable_archive), pybit7z.FormatSevenZip
        )
        editor.update_item("original.txt", new_data)
        editor.apply_changes()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract(str(editable_archive))

    assert next(iter(result.values())) == new_data


def test_editor_update_item_lifetime_survives_gc(editable_archive):
    """CRITICAL: bytes passed to update_item must remain valid until apply_changes.

    Same dangling-reference scenario as add_file: the old local vector was
    destroyed at the end of update_item, so apply_changes would read freed
    memory. Here we drop the bytes reference and force GC before apply_changes.
    """
    new_data = b"lifetime update payload" * 50

    with pybit7z.lib7zip_context() as lib:
        editor = pybit7z.BitArchiveEditor(
            lib, str(editable_archive), pybit7z.FormatSevenZip
        )
        payload = bytes(new_data)
        editor.update_item(0, payload)
        del payload
        gc.collect()
        editor.apply_changes()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract(str(editable_archive))

    assert next(iter(result.values())) == new_data


def test_editor_update_item_by_path_lifetime(editable_archive):
    new_data = b"lifetime update via path" * 50

    with pybit7z.lib7zip_context() as lib:
        editor = pybit7z.BitArchiveEditor(
            lib, str(editable_archive), pybit7z.FormatSevenZip
        )
        payload = bytes(new_data)
        editor.update_item("original.txt", payload)
        del payload
        gc.collect()
        editor.apply_changes()

    with pybit7z.lib7zip_context() as lib:
        extractor = pybit7z.BitFileExtractor(lib, pybit7z.FormatSevenZip)
        result = extractor.extract(str(editable_archive))

    assert next(iter(result.values())) == new_data


from __future__ import annotations

from pybit7z import (
    Bit7zLibrary,
    BitArchiveEditor,
    BitArchiveItem,
    BitArchiveReader,
    BitArchiveWriter,
    BitCompressionLevel,
    BitFileCompressor,
    BitInputItem,
    BitProperty,
    BitPropVariant,
    BitPropVariantType,
    FormatSevenZip,
    SymlinkPolicy,
    UpdateMode,
)


def _make_archive(
    lib: Bit7zLibrary,
    files: list[str],
    archive_path: str,
    fmt=FormatSevenZip,
):
    """Helper to create a multi-file archive on disk."""
    comp = BitFileCompressor(lib, fmt)
    comp.compress(files, archive_path)


# ---------------------------------------------------------------------------
# BitPropVariant
# ---------------------------------------------------------------------------


class TestBitPropVariant:
    def test_empty(self):
        v = BitPropVariant()
        assert v.type() == BitPropVariantType.Empty
        assert not v.is_bool()
        assert not v.is_string()
        assert not v.is_uint64()

    def test_bool(self):
        v = BitPropVariant(True)
        assert v.is_bool()
        assert v.get_bool() is True
        assert v.type() == BitPropVariantType.Bool

    def test_uint64(self):
        v = BitPropVariant(123456789)
        assert v.is_uint64()
        assert v.get_uint64() == 123456789
        assert v.type() == BitPropVariantType.UInt64

    def test_string_via_property(self, tmp_path: Path):
        """String variants are obtained from archive item properties."""
        with pybit7z.lib7zip_context() as lib:
            f = tmp_path / "a.txt"
            f.write_text("hello")
            arc = str(tmp_path / "t.7z")
            comp = BitFileCompressor(lib, FormatSevenZip)
            comp.compress([str(f)], arc)

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            item = reader.item_at(0)
            pv = item.item_property(BitProperty.Path)
            assert pv.is_string()
            assert "a.txt" in pv.get_string()

    def test_clear(self):
        v = BitPropVariant(42)
        assert v.is_uint64()
        v.clear()
        assert v.type() == BitPropVariantType.Empty


# ---------------------------------------------------------------------------
# BitInputItem
# ---------------------------------------------------------------------------


class TestBitInputItem:
    def test_from_bytes(self):
        data = b"hello world"
        item = BitInputItem(data, "hello.txt")
        assert item.size() == len(data)
        assert not item.is_dir()
        assert not item.is_sym_link()
        assert item.in_archive_path() == "hello.txt"
        assert item.has_new_data()

    def test_from_file_path(self, tmp_path: Path):
        f = tmp_path / "input.txt"
        f.write_text("file content here")
        item = BitInputItem(str(f))
        assert not item.is_dir()
        assert item.size() == len(b"file content here")
        assert str(f) in item.path()

    def test_from_file_path_with_archive_path(self, tmp_path: Path):
        f = tmp_path / "input.txt"
        f.write_text("data")
        item = BitInputItem(str(f), "renamed.txt")
        assert item.in_archive_path() == "renamed.txt"

    def test_set_times(self):
        item = BitInputItem(b"data", "x.bin")
        t = datetime.datetime(2025, 6, 1, 12, 30, 45)
        item.set_creation_time(t)
        item.set_last_write_time(t)
        item.set_last_access_time(t)

    def test_attributes(self):
        item = BitInputItem(b"data", "x.bin")
        assert isinstance(item.attributes(), int)

    def test_item_property(self):
        item = BitInputItem(b"data", "x.bin")
        pv = item.item_property(BitProperty.Size)
        assert pv.is_uint64()
        assert pv.get_uint64() == 4

    def test_bytes_lifetime_with_compression(self):
        """Bytes-backed add_file must stay valid throughout compression."""
        with pybit7z.lib7zip_context() as lib:
            data = b"lifetime data payload"
            writer = BitArchiveWriter(lib, FormatSevenZip)
            item = writer.add_file(data, "payload.bin")
            assert isinstance(item, BitInputItem)
            assert item.size() == len(data)
            buf = writer.compress_to()
            assert isinstance(buf, (bytes, bytearray))
            assert len(buf) > 0


# ---------------------------------------------------------------------------
# BitInputArchive / BitArchiveReader extra methods
# ---------------------------------------------------------------------------


class TestBitInputArchive:
    def _make(self, lib: Bit7zLibrary, tmp_path: Path):
        f1 = tmp_path / "a.txt"
        f1.write_text("aaa")
        f2 = tmp_path / "b.txt"
        f2.write_text("bbb")
        arc = str(tmp_path / "test.7z")
        _make_archive(lib, [str(f1), str(f2)], arc)
        return arc

    def test_counts_and_contains(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            assert reader.items_count() == 2
            assert reader.files_count() == 2
            assert reader.folders_count() == 0
            assert reader.contains("a.txt")
            assert not reader.contains("nope.txt")

    def test_item_at(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            item = reader.item_at(0)
            assert isinstance(item, BitArchiveItem)
            assert item.name() in ("a.txt", "b.txt")

    def test_is_item_folder_encrypted(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            assert not reader.is_item_folder(0)
            assert not reader.is_item_encrypted(0)

    def test_detected_and_extraction_format(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            assert reader.detected_format() == FormatSevenZip
            assert reader.extraction_format() == FormatSevenZip

    def test_archive_path(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            assert reader.archive_path().endswith("test.7z")

    def test_test_method(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            reader.test()


# ---------------------------------------------------------------------------
# BitArchiveEditor: delete_item & rename_item
# ---------------------------------------------------------------------------


class TestBitArchiveEditorDeleteRename:
    def _make(self, lib: Bit7zLibrary, tmp_path: Path):
        f1 = tmp_path / "a.txt"
        f1.write_text("aaa")
        f2 = tmp_path / "b.txt"
        f2.write_text("bbb")
        f3 = tmp_path / "c.log"
        f3.write_text("ccc")
        arc = str(tmp_path / "test.7z")
        _make_archive(lib, [str(f1), str(f2), str(f3)], arc)
        return arc

    def test_delete_by_index(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            editor = BitArchiveEditor(lib, arc, FormatSevenZip)
            editor.delete_item(0)
            editor.apply_changes()

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            names = sorted(i.name() for i in reader.items())
            assert names == ["b.txt", "c.log"]

    def test_delete_by_path(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            editor = BitArchiveEditor(lib, arc, FormatSevenZip)
            editor.delete_item("b.txt")
            editor.apply_changes()

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            names = sorted(i.name() for i in reader.items())
            assert names == ["a.txt", "c.log"]

    def test_rename_by_index(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            editor = BitArchiveEditor(lib, arc, FormatSevenZip)
            editor.rename_item(0, "renamed.txt")
            editor.apply_changes()

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            names = [i.name() for i in reader.items()]
            assert "renamed.txt" in names

    def test_rename_by_path(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            editor = BitArchiveEditor(lib, arc, FormatSevenZip)
            editor.rename_item("b.txt", "new_b.txt")
            editor.apply_changes()

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            names = [i.name() for i in reader.items()]
            assert "new_b.txt" in names
            assert "b.txt" not in names

    def test_set_update_mode(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            editor = BitArchiveEditor(lib, arc, FormatSevenZip)
            editor.set_update_mode(UpdateMode.Append)
            editor.apply_changes()


# ---------------------------------------------------------------------------
# BitOutputArchive: add_files / add_directory / compress_to
# ---------------------------------------------------------------------------


class TestBitOutputArchiveMethods:
    def test_add_files_list(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            f1 = tmp_path / "a.txt"
            f1.write_text("aaa")
            f2 = tmp_path / "b.txt"
            f2.write_text("bbb")

            writer = BitArchiveWriter(lib, FormatSevenZip)
            writer.add_files([str(f1), str(f2)])
            out = tmp_path / "out.7z"
            writer.compress_to(str(out))

            reader = BitArchiveReader(lib, str(out), FormatSevenZip)
            assert reader.items_count() == 2

    def test_add_directory(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            sub = tmp_path / "subdir"
            sub.mkdir()
            (sub / "x.txt").write_text("x")
            (sub / "y.txt").write_text("y")

            writer = BitArchiveWriter(lib, FormatSevenZip)
            writer.add_directory(str(sub))
            out = tmp_path / "out.7z"
            writer.compress_to(str(out))

            reader = BitArchiveReader(lib, str(out), FormatSevenZip)
            assert reader.files_count() == 2

    def test_add_directory_contents(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            sub = tmp_path / "subdir"
            sub.mkdir()
            (sub / "x.txt").write_text("x")

            writer = BitArchiveWriter(lib, FormatSevenZip)
            writer.add_directory_contents(str(sub))
            out = tmp_path / "out.7z"
            writer.compress_to(str(out))

            reader = BitArchiveReader(lib, str(out), FormatSevenZip)
            assert reader.files_count() == 1

    def test_add_file_item_returns_input_item(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            f = tmp_path / "a.txt"
            f.write_text("aaa")
            writer = BitArchiveWriter(lib, FormatSevenZip)
            item = writer.add_file(str(f))
            assert isinstance(item, BitInputItem)


# ---------------------------------------------------------------------------
# BitAbstractArchiveHandler / Creator setters
# ---------------------------------------------------------------------------


class TestHandlerSetters:
    def test_password_and_compression_settings(self):
        with pybit7z.lib7zip_context() as lib:
            writer = BitArchiveWriter(lib, FormatSevenZip)
            writer.set_password("secret")
            assert writer.is_password_defined()
            writer.clear_password()
            assert not writer.is_password_defined()

            writer.set_compression_level(BitCompressionLevel.Ultra)
            writer.set_compression_method(pybit7z.BitCompressionMethod.Lzma2)
            writer.set_solid_mode(False)
            writer.set_overwrite_mode(pybit7z.OverwriteMode.Overwrite)

    def test_keep_alive_library(self):
        """format() must keep a reference to the owning library alive."""
        with pybit7z.lib7zip_context() as lib:
            writer = BitArchiveWriter(lib, FormatSevenZip)
            fmt = writer.compression_format()
            assert fmt.extension().endswith(".7z")


# ---------------------------------------------------------------------------
# SymlinkPolicy enum
# ---------------------------------------------------------------------------


def test_symlink_policy_enum():
    assert SymlinkPolicy.Follow != SymlinkPolicy.DoNotFollow
    item = BitInputItem(b"x", "x.bin")
    assert item.in_archive_path() == "x.bin"


# ---------------------------------------------------------------------------
# BitArchiveItem metadata accessors
# ---------------------------------------------------------------------------


class TestBitArchiveItemMetadata:
    def test_item_fields(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            f = tmp_path / "a.txt"
            f.write_text("hello")
            arc = str(tmp_path / "t.7z")
            _make_archive(lib, [str(f)], arc)

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            item = reader.item_at(0)
            assert item.name() == "a.txt"
            assert item.size() == 5
            assert not item.is_dir()
            assert not item.is_encrypted()
            assert item.index() == 0

    def test_item_property(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            f = tmp_path / "a.txt"
            f.write_text("hello")
            arc = str(tmp_path / "t.7z")
            _make_archive(lib, [str(f)], arc)

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            item = reader.item_at(0)
            pv = item.item_property(BitProperty.Size)
            assert pv.is_uint64()
            assert pv.get_uint64() == 5


# ---------------------------------------------------------------------------
# BitFileCompressor additional overloads
# ---------------------------------------------------------------------------


class TestBitFileCompressorExtra:
    def test_compress_with_renamed_map(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            f = tmp_path / "a.txt"
            f.write_text("aaa")
            arc = str(tmp_path / "out.7z")
            comp = BitFileCompressor(lib, FormatSevenZip)
            comp.compress({str(f): "renamed.txt"}, arc)

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            names = [i.name() for i in reader.items()]
            assert names == ["renamed.txt"]

    def test_compress_directory(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            sub = tmp_path / "sub"
            sub.mkdir()
            (sub / "a.txt").write_text("a")
            arc = str(tmp_path / "out.7z")
            comp = BitFileCompressor(lib, FormatSevenZip)
            comp.compress_directory(str(sub), arc)

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            assert reader.files_count() == 1

    def test_compress_files(self, tmp_path: Path):
        with pybit7z.lib7zip_context() as lib:
            f1 = tmp_path / "a.txt"
            f1.write_text("a")
            f2 = tmp_path / "b.txt"
            f2.write_text("b")
            arc = str(tmp_path / "out.7z")
            comp = BitFileCompressor(lib, FormatSevenZip)
            comp.compress_files([str(f1), str(f2)], arc)

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            assert reader.items_count() == 2


# ---------------------------------------------------------------------------
# End-to-end: BitInputItem with BitMemCompressor and extraction
# ---------------------------------------------------------------------------


def test_bit_input_item_roundtrip():
    with pybit7z.lib7zip_context() as lib:
        writer = BitArchiveWriter(lib, FormatSevenZip)
        item1 = writer.add_file(b"first data", "1.txt")
        item2 = writer.add_file(b"second data", "2.txt")
        assert item1.in_archive_path() == "1.txt"
        assert item2.in_archive_path() == "2.txt"
        buf = writer.compress_to()

        reader = BitArchiveReader(lib, buf, FormatSevenZip)
        assert reader.items_count() == 2
        names = sorted(i.name() for i in reader.items())
        assert names == ["1.txt", "2.txt"]
