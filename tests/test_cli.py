from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Optional

import pytest


def _run(args: list[str], cwd=None, stdin=None):
    """Run the CLI module directly to avoid the pybit7z.exe launcher crash."""
    cmd = [sys.executable, "-m", "pybit7z.cli", *args]
    return subprocess.run(cmd, cwd=cwd, input=stdin, capture_output=True, check=False)


def _make_archive(
    temp_dir: Path,
    files: list[Path],
    name: str = "archive.7z",
    extra: Optional[list[str]] = None,
):
    """Helper: compress one or more files into a 7z archive."""
    files = files or []
    paths = [str(f) for f in files]
    out = str(temp_dir / name)
    cmd = ["compress", *paths, "-o", out]
    if extra:
        cmd += extra
    result = _run(cmd, cwd=str(temp_dir))
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    return Path(out)


def test_cli_help():
    """Test the CLI help message"""
    result = _run(["--help"])
    assert result.returncode == 0
    assert "pybit7z command-line compression tool" in result.stdout.decode()


def test_compress_basic(temp_dir):
    """Test basic compression functionality"""
    test_file = temp_dir / "test.txt"
    test_file.write_text("sample content")
    output = temp_dir / "test.7z"

    result = _run(["compress", str(test_file), "-o", str(output), "-f", "7z"])

    assert result.returncode == 0
    assert output.exists()
    assert "Successfully created archive" in result.stdout.decode()


def test_decompress_basic(temp_dir):
    """Test basic decompression functionality"""
    # Create test archive
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")
    archive = temp_dir / "test.7z"
    _run(["compress", str(test_file), "-o", str(archive)])

    # Test decompression
    output_dir = temp_dir / "output"
    result = _run(["decompress", str(archive), "-o", str(output_dir)])

    assert result.returncode == 0
    assert (output_dir / test_file.name).exists()


def test_invalid_parameters(temp_dir):
    """Test handling of invalid parameters"""
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")
    output = temp_dir / "test.invalid"

    result = _run(["compress", str(test_file), "-o", str(output), "-f", "invalid"])

    assert result.returncode != 0
    assert "error: argument -f/--format" in result.stderr.decode()

    result = _run(["decompress", str(test_file), "-f", "7z"])

    assert result.returncode != 0
    assert "Output file/directory path is required" in result.stderr.decode()


def test_password_protection(temp_dir):
    """Test password protection for compression and decryption"""
    test_file = temp_dir / "secret.txt"
    test_file.write_text("confidential")
    output = temp_dir / "protected.7z"

    # Compress with password
    assert (
        _run(
            ["compress", str(test_file), "-o", str(output), "-p", "mypassword"]
        ).returncode
        == 0
    )

    # Decompress without password should fail
    extract_dir = temp_dir / "extracted"
    result = _run(["decompress", str(output), "-o", str(extract_dir)])
    assert result.returncode != 0
    assert "a password is required" in result.stderr.decode().lower()

    # Decompress with correct password
    result = _run(
        ["decompress", str(output), "-o", str(extract_dir), "-p", "mypassword"]
    )
    assert result.returncode == 0
    assert (extract_dir / test_file.name).exists()


def test_list_output(temp_dir):
    """
    Test the 'list' command to ensure it correctly lists files in an archive.
    """
    # Create archive with multiple files
    archive = temp_dir / "multi.7z"
    files = [temp_dir / f"file{i}.txt" for i in range(3)]
    for f in files:
        f.write_text("data")

    _run(["compress"] + [str(f) for f in files] + ["-o", str(archive)])

    # Test archive listing
    result = _run(["list", str(archive)])

    assert result.returncode == 0
    for f in files:
        assert f.name in result.stdout.decode()


# ---------------------------------------------------------------------------
# Compress tests
# ---------------------------------------------------------------------------


def test_compress_format_autodetect_zip(temp_dir):
    """Compression format should be auto-detected from the output extension."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("hello")
    output = temp_dir / "out.zip"

    result = _run(["compress", str(test_file), "-o", str(output)])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert output.exists()
    # A real zip file starts with PK\x03\x04.
    assert output.read_bytes()[:4] == b"PK\x03\x04"


def test_compress_different_levels(temp_dir):
    """Different compression levels should produce archives successfully."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("A" * 1000)

    for level in ("Fastest", "Fast", "Normal", "Max", "Ultra"):
        out = temp_dir / f"lvl_{level}.7z"
        result = _run(
            ["compress", str(test_file), "-o", str(out), "-l", level, "-f", "7z"]
        )
        assert result.returncode == 0, result.stderr.decode(errors="replace")
        assert out.exists()


def test_compress_different_methods(temp_dir):
    """Compression with explicit methods should work for the chosen format."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("compressible data " * 100)

    # Methods valid for 7z format.
    for method in ("Lzma", "Lzma2", "BZip2", "Ppmd", "Copy"):
        out = temp_dir / f"m_{method}.7z"
        result = _run(
            ["compress", str(test_file), "-o", str(out), "-m", method, "-f", "7z"]
        )
        assert result.returncode == 0, result.stderr.decode(errors="replace")
        assert out.exists()

    # Deflate is valid for zip format.
    out = temp_dir / "m_deflate.zip"
    result = _run(
        ["compress", str(test_file), "-o", str(out), "-m", "Deflate", "-f", "zip"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()


@pytest.mark.parametrize(
    "codec",
    ["brotli", "flzma2", "lizard", "lz4", "lz5", "zstd"],
)
def test_compress_external_codec_roundtrip(temp_dir, codec):
    """Each external codec must compress and extract losslessly via the CLI."""
    test_file = temp_dir / "data.txt"
    content = "external codec roundtrip content " * 50
    test_file.write_text(content)

    archive = temp_dir / f"{codec}.7z"
    result = _run(
        ["compress", str(test_file), "-o", str(archive), "-m", codec, "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert archive.exists()
    assert archive.stat().st_size > 0

    extract_dir = temp_dir / "out"
    result = _run(["extract", str(archive), "-o", str(extract_dir)])
    assert result.returncode == 0, result.stderr.decode(errors="replace")

    extracted = (extract_dir / test_file.name).read_text()
    assert extracted == content


def test_compress_solid_mode(temp_dir):
    """Solid compression should work for 7z format."""
    files = []
    for i in range(3):
        f = temp_dir / f"solid_{i}.txt"
        f.write_text(f"content {i} " * 50)
        files.append(f)

    out = temp_dir / "solid.7z"
    result = _run(
        ["compress"] + [str(f) for f in files] + ["-o", str(out), "--solid", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()


def test_compress_threads(temp_dir):
    """Multi-threaded compression should work."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data " * 2000)

    out = temp_dir / "threads.7z"
    result = _run(
        ["compress", str(test_file), "-o", str(out), "--threads", "4", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()


def test_compress_password_crypt_headers(temp_dir):
    """Archive with encrypted headers should require a password to list."""
    test_file = temp_dir / "secret.txt"
    test_file.write_text("confidential")

    out = temp_dir / "locked.7z"
    result = _run(
        ["compress", str(test_file), "-o", str(out), "-p", "pass123", "--crypt-headers"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()

    # Listing without a password should fail (headers are encrypted).
    result = _run(["list", str(out)])
    assert result.returncode != 0

    # Listing with the correct password should succeed.
    result = _run(["list", str(out), "-p", "pass123"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "secret.txt" in result.stdout.decode()


def test_compress_exclude(temp_dir):
    """Exclude patterns should skip matching files."""
    keep = temp_dir / "keep.txt"
    skip = temp_dir / "skip.log"
    keep.write_text("kept")
    skip.write_text("skipped")

    out = temp_dir / "excluded.7z"
    result = _run(
        ["compress", str(temp_dir), "-o", str(out), "-x", "*.log", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")

    # Only keep.txt should be in the archive.
    result = _run(["list", str(out)])
    assert "keep.txt" in result.stdout.decode()
    assert "skip.log" not in result.stdout.decode()


def test_compress_delete_after(temp_dir):
    """--delete-after should remove source files after compression."""
    test_file = temp_dir / "todelete.txt"
    test_file.write_text("gone soon")

    out = temp_dir / "del_after.7z"
    result = _run(
        ["compress", str(test_file), "-o", str(out), "--delete-after", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert not test_file.exists()
    assert out.exists()


def test_compress_stdin(temp_dir):
    """Reading input from stdin should compress it under stdin-name."""
    out = temp_dir / "from_stdin.7z"
    payload = b"stdin payload data"
    result = _run(
        [
            "compress",
            "--stdin",
            "--stdin-name",
            "payload.bin",
            "-o",
            str(out),
            "-f",
            "7z",
        ],
        stdin=payload,
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()

    # The archive should contain the payload.
    extracted = temp_dir / "stdin_out"
    result = _run(["extract", str(out), "-o", str(extracted)])
    assert result.returncode == 0
    assert (extracted / "payload.bin").read_bytes() == payload


def test_compress_to_stdout(temp_dir):
    """Compressing to stdout ('-o -') should write the archive bytes to stdout."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("pipe me")

    result = _run(["compress", str(test_file), "-o", "-", "-f", "7z"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    # 7z signature starts with '7z\xbc\xaf\x27\x1c'.
    assert result.stdout[:6] == b"7z\xbc\xaf\x27\x1c"


def test_compress_no_store_times(temp_dir):
    """--no-store-times should not crash and produce an archive."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("timeless")

    out = temp_dir / "notimes.7z"
    result = _run(
        ["compress", str(test_file), "-o", str(out), "--no-store-times", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()


def test_compress_dictionary_word_size(temp_dir):
    """Dictionary and word size options should be accepted."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("dictionary data " * 200)

    out = temp_dir / "dictsize.7z"
    result = _run(
        [
            "compress",
            str(test_file),
            "-o",
            str(out),
            "--dictionary-size",
            "16777216",  # 16 MB
            "--word-size",
            "64",
            "-f",
            "7z",
        ]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()


def test_compress_multiple_formats(temp_dir):
    """All writable formats should produce a valid archive."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("multi format test")

    for fmt, ext in (
        ("7z", ".7z"),
        ("zip", ".zip"),
        ("tar", ".tar"),
        ("gzip", ".gz"),
        ("bzip2", ".bz2"),
        ("xz", ".xz"),
    ):
        out = temp_dir / f"out{ext}"
        result = _run(["compress", str(test_file), "-o", str(out), "-f", fmt])
        assert result.returncode == 0, (
            f"{fmt}: {result.stderr.decode(errors='replace')}"
        )
        assert out.exists()
        assert out.stat().st_size > 0


def test_compress_show_files(temp_dir):
    """--show-files should log each processed file to stderr."""
    test_file = temp_dir / "logged.txt"
    test_file.write_text("logged content")

    out = temp_dir / "shown.7z"
    result = _run(
        ["compress", str(test_file), "-o", str(out), "--show-files", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "logged.txt" in result.stderr.decode(errors="replace")


def test_compress_progress(temp_dir):
    """--progress should not crash and should emit progress output."""
    test_file = temp_dir / "prog.txt"
    test_file.write_text("progress data " * 500)

    out = temp_dir / "progress.7z"
    result = _run(
        ["compress", str(test_file), "-o", str(out), "--progress", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "Progress" in result.stderr.decode(errors="replace")


def test_compress_ratio(temp_dir):
    """--ratio should report compression ratio on stderr."""
    test_file = temp_dir / "ratio.txt"
    test_file.write_text("compressible " * 1000)

    out = temp_dir / "ratio.7z"
    result = _run(["compress", str(test_file), "-o", str(out), "--ratio", "-f", "7z"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "Ratio" in result.stderr.decode(errors="replace")


# ---------------------------------------------------------------------------
# Extract tests
# ---------------------------------------------------------------------------


def test_extract_by_indices(temp_dir):
    """Extracting by index should only retrieve the selected items."""
    files = [temp_dir / f"f{i}.txt" for i in range(3)]
    for i, f in enumerate(files):
        f.write_text(f"file {i}")
    archive = _make_archive(temp_dir, files)

    out = temp_dir / "idx_out"
    result = _run(["extract", str(archive), "-o", str(out), "-i", "0"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    # Only item 0 should be extracted.
    extracted = list(out.rglob("*.txt"))
    assert len(extracted) == 1
    assert extracted[0].read_text() == "file 0"


def test_extract_match_wildcard(temp_dir):
    """Wildcard matching should extract only the matching items."""
    files = [temp_dir / "keep.txt", temp_dir / "skip.log"]
    for f in files:
        f.write_text("data")
    archive = _make_archive(temp_dir, files)

    out = temp_dir / "match_out"
    result = _run(["extract", str(archive), "-o", str(out), "--match", "*.txt"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    names = {p.name for p in out.rglob("*") if p.is_file()}
    assert names == {"keep.txt"}


def test_extract_match_regex(temp_dir):
    """Regex matching should extract matching items."""
    files = [temp_dir / "alpha.txt", temp_dir / "beta.log"]
    for f in files:
        f.write_text("data")
    archive = _make_archive(temp_dir, files)

    out = temp_dir / "re_out"
    result = _run(
        ["extract", str(archive), "-o", str(out), "--match-regex", r".*\.log"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    names = {p.name for p in out.rglob("*") if p.is_file()}
    assert names == {"beta.log"}


def test_extract_filter_policy_exclude(temp_dir):
    """Exclude filter policy should extract everything except matches."""
    files = [temp_dir / "a.txt", temp_dir / "b.log"]
    for f in files:
        f.write_text("data")
    archive = _make_archive(temp_dir, files)

    out = temp_dir / "filt_out"
    result = _run(
        [
            "extract",
            str(archive),
            "-o",
            str(out),
            "--match",
            "*.log",
            "--filter-policy",
            "exclude",
        ]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    names = {p.name for p in out.rglob("*") if p.is_file()}
    assert names == {"a.txt"}


@pytest.mark.parametrize(
    ("extra_args", "expected"),
    [
        ([], b"first content"),
        (["-i", "1"], b"second content"),
    ],
)
def test_extract_to_stdout(temp_dir, extra_args, expected):
    """--to-stdout should write the selected item's content to stdout."""
    files = [temp_dir / "first.txt", temp_dir / "second.txt"]
    files[0].write_text("first content")
    files[1].write_text("second content")
    archive = _make_archive(temp_dir, files)

    result = _run(["extract", str(archive), "--to-stdout", *extra_args])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert result.stdout == expected


def test_extract_password(temp_dir):
    """Extracting a password-protected archive should require the password."""
    test_file = temp_dir / "secret.txt"
    test_file.write_text("secret data")
    archive = _make_archive(temp_dir, [test_file], name="pwd.7z", extra=["-p", "abc"])

    out = temp_dir / "pwd_out"
    # Without password should fail.
    result = _run(["extract", str(archive), "-o", str(out)])
    assert result.returncode != 0

    # With password should succeed.
    out2 = temp_dir / "pwd_out2"
    result = _run(["extract", str(archive), "-o", str(out2), "-p", "abc"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert (out2 / "secret.txt").exists()


def test_extract_show_files(temp_dir):
    """--show-files during extraction should log files to stderr."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = _make_archive(temp_dir, [test_file])

    out = temp_dir / "show_out"
    result = _run(["extract", str(archive), "-o", str(out), "--show-files"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "data.txt" in result.stderr.decode(errors="replace")


def test_extract_progress(temp_dir):
    """--progress during extraction should not crash."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data " * 500)
    archive = _make_archive(temp_dir, [test_file])

    out = temp_dir / "prog_out"
    result = _run(["extract", str(archive), "-o", str(out), "--progress"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")


# ---------------------------------------------------------------------------
# List tests
# ---------------------------------------------------------------------------


def test_list_verbose(temp_dir):
    """Verbose listing should include solid/encrypted/volumes info."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = _make_archive(temp_dir, [test_file])

    result = _run(["list", str(archive), "-v"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    out = result.stdout.decode()
    assert "Solid" in out
    assert "Encrypted" in out
    assert "Volumes" in out
    assert "data.txt" in out


# ---------------------------------------------------------------------------
# Test archive integrity
# ---------------------------------------------------------------------------


def test_test_archive_valid(temp_dir):
    """The 'test' command should report a valid archive as passing."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = _make_archive(temp_dir, [test_file])

    result = _run(["test", str(archive)])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "integrity test passed" in result.stdout.decode().lower()


def test_test_archive_invalid(temp_dir):
    """The 'test' command should fail on a corrupted archive."""
    archive = temp_dir / "broken.7z"
    archive.write_bytes(b"not a real archive")

    result = _run(["test", str(archive)])
    assert result.returncode != 0


# ---------------------------------------------------------------------------
# Info tests
# ---------------------------------------------------------------------------


def test_info_archive(temp_dir):
    """The 'info' command should print archive metadata."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("info data")
    archive = _make_archive(temp_dir, [test_file])

    result = _run(["info", str(archive)])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    out = result.stdout.decode()
    assert "Format:" in out
    assert "Items count:" in out
    assert "Solid:" in out
    assert "Encrypted:" in out


def test_info_verbose(temp_dir):
    """Verbose info should print archive properties."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("info data")
    archive = _make_archive(temp_dir, [test_file])

    result = _run(["info", str(archive), "-v"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "Archive properties" in result.stdout.decode()


# ---------------------------------------------------------------------------
# Update tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "delete_args",
    [
        ["--delete", "a.txt"],
        ["--delete-index", "0"],
    ],
)
def test_update_delete(temp_dir, delete_args):
    """Deleting an item (by path or index) should remove it from the archive."""
    files = [temp_dir / "a.txt", temp_dir / "b.txt"]
    for f in files:
        f.write_text("data")
    archive = _make_archive(temp_dir, files)

    result = _run(["update", str(archive), "-f", "7z", *delete_args])
    assert result.returncode == 0, result.stderr.decode(errors="replace")

    listing = _run(["list", str(archive)]).stdout.decode()
    assert "a.txt" not in listing
    assert "b.txt" in listing


@pytest.mark.parametrize(
    "rename_args",
    [
        ["--rename", "old_name.txt=new_name.txt"],
        ["--rename-index", "0:new_name.txt"],
    ],
)
def test_update_rename(temp_dir, rename_args):
    """Renaming an item (by path or index) should change its name."""
    test_file = temp_dir / "old_name.txt"
    test_file.write_text("data")
    archive = _make_archive(temp_dir, [test_file])

    result = _run(["update", str(archive), "-f", "7z", *rename_args])
    assert result.returncode == 0, result.stderr.decode(errors="replace")

    listing = _run(["list", str(archive)]).stdout.decode()
    assert "new_name.txt" in listing
    assert "old_name.txt" not in listing


def test_update_requires_format(temp_dir):
    """Update with auto format should report an error."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = _make_archive(temp_dir, [test_file])

    result = _run(["update", str(archive), "--delete", "data.txt"])
    assert result.returncode != 0
    assert "explicit writable format" in result.stderr.decode().lower()


def test_update_no_operations(temp_dir):
    """Update without any operation should exit with code 2."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = _make_archive(temp_dir, [test_file])

    result = _run(["update", str(archive), "-f", "7z"])
    assert result.returncode == 2


# ---------------------------------------------------------------------------
# Error handling tests
# ---------------------------------------------------------------------------


def test_compress_missing_output():
    """Compression without an output path should error."""
    result = _run(["compress", "anything"])
    assert result.returncode != 0
    assert "Output file path is required" in result.stderr.decode()


def test_compress_missing_inputs():
    """Compression without input paths (and no --stdin) should error."""
    result = _run(["compress", "-o", "out.7z"])
    assert result.returncode != 0
    assert "Input paths are required" in result.stderr.decode()


def test_extract_missing_output():
    """Extraction without output or --to-stdout should error."""
    result = _run(["extract", "any.7z"])
    assert result.returncode != 0
    assert "Output file/directory path is required" in result.stderr.decode()


def test_compress_invalid_format_property(temp_dir):
    """An invalid --format-property should raise a clear error."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    out = temp_dir / "badprop.7z"

    result = _run(
        [
            "compress",
            str(test_file),
            "-o",
            str(out),
            "--format-property",
            "notanumber",
            "-f",
            "7z",
        ]
    )
    assert result.returncode != 0
    assert "Invalid --format-property" in result.stderr.decode()


def test_update_invalid_rename_spec(temp_dir):
    """An invalid --rename spec should raise a clear error."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = _make_archive(temp_dir, [test_file])

    result = _run(["update", str(archive), "-f", "7z", "--rename", "bad-spec"])
    assert result.returncode != 0
    assert "Invalid --rename spec" in result.stderr.decode()
