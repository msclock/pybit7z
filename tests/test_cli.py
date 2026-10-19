from __future__ import annotations

import io
import os
import sys
from pathlib import Path
from typing import Optional

import pytest

from pybit7z.cli import main


class _CLIResult:
    """Lightweight stand-in for subprocess.CompletedProcess.

    ``stdout`` and ``stderr`` are ``bytes`` so the existing test assertions
    (``result.stdout.decode()``, ``result.stdout[:6]`` ...) keep working.
    """

    def __init__(self, returncode: int, stdout: bytes, stderr: bytes) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


@pytest.fixture
def run_cli(capsysbinary):
    """Run the CLI entry point in-process and capture its output.

    Uses ``capsysbinary`` (instead of ``capsys``) because the CLI can write
    raw binary bytes to stdout (``-o -`` / ``--to-stdout``), and ``capsys``
    would fail trying to UTF-8-decode them. ``capsysbinary`` returns ``bytes``
    directly, matching the previous subprocess behaviour.
    """

    def _run(args: list[str], cwd=None, stdin: Optional[bytes] = None) -> _CLIResult:
        old_cwd = Path.cwd()
        old_stdin = sys.stdin

        if cwd is not None:
            os.chdir(cwd)
        if stdin is not None:
            sys.stdin = io.TextIOWrapper(io.BytesIO(stdin), encoding="utf-8")

        returncode = 0
        try:
            try:
                main(list(args))
            except SystemExit as exc:
                code = exc.code
                returncode = int(code) if code is not None else 0
        finally:
            os.chdir(old_cwd)
            sys.stdin = old_stdin

        captured = capsysbinary.readouterr()
        return _CLIResult(returncode, captured.out, captured.err)

    return _run


@pytest.fixture
def make_archive(run_cli):
    """Helper: compress one or more files into a 7z archive."""

    def _make_archive(
        temp_dir: Path,
        files: list[Path],
        name: str = "archive.7z",
        extra: Optional[list[str]] = None,
    ) -> Path:
        files = files or []
        paths = [str(f) for f in files]
        out = str(temp_dir / name)
        cmd = ["compress", *paths, "-o", out]
        if extra:
            cmd += extra
        result = run_cli(cmd, cwd=str(temp_dir))
        assert result.returncode == 0, result.stderr.decode(errors="replace")
        return Path(out)

    return _make_archive


def test_cli_help(run_cli):
    """Test the CLI help message"""
    result = run_cli(["--help"])
    assert result.returncode == 0
    assert "pybit7z command-line compression tool" in result.stdout.decode()


def test_compress_basic(temp_dir, run_cli):
    """Test basic compression functionality"""
    test_file = temp_dir / "test.txt"
    test_file.write_text("sample content")
    output = temp_dir / "test.7z"

    result = run_cli(["compress", str(test_file), "-o", str(output), "-f", "7z"])

    assert result.returncode == 0
    assert output.exists()
    assert "Successfully created archive" in result.stdout.decode()


def test_decompress_basic(temp_dir, run_cli):
    """Test basic decompression functionality"""
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")
    archive = temp_dir / "test.7z"
    run_cli(["compress", str(test_file), "-o", str(archive)])

    output_dir = temp_dir / "output"
    result = run_cli(["decompress", str(archive), "-o", str(output_dir)])

    assert result.returncode == 0
    assert (output_dir / test_file.name).exists()


def test_invalid_parameters(temp_dir, run_cli):
    """Test handling of invalid parameters"""
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")
    output = temp_dir / "test.invalid"

    result = run_cli(["compress", str(test_file), "-o", str(output), "-f", "invalid"])

    assert result.returncode != 0
    assert "error: argument -f/--format" in result.stderr.decode()

    result = run_cli(["decompress", str(test_file), "-f", "7z"])

    assert result.returncode != 0
    assert "Output file/directory path is required" in result.stderr.decode()


def test_password_protection(temp_dir, run_cli):
    """Test password protection for compression and decryption"""
    test_file = temp_dir / "secret.txt"
    test_file.write_text("confidential")
    output = temp_dir / "protected.7z"

    assert (
        run_cli(
            ["compress", str(test_file), "-o", str(output), "-p", "mypassword"]
        ).returncode
        == 0
    )

    extract_dir = temp_dir / "extracted"
    result = run_cli(["decompress", str(output), "-o", str(extract_dir)])
    assert result.returncode != 0
    assert "a password is required" in result.stderr.decode().lower()

    result = run_cli(
        ["decompress", str(output), "-o", str(extract_dir), "-p", "mypassword"]
    )
    assert result.returncode == 0
    assert (extract_dir / test_file.name).exists()


def test_list_output(temp_dir, run_cli):
    """
    Test the 'list' command to ensure it correctly lists files in an archive.
    """
    archive = temp_dir / "multi.7z"
    files = [temp_dir / f"file{i}.txt" for i in range(3)]
    for f in files:
        f.write_text("data")

    run_cli(["compress"] + [str(f) for f in files] + ["-o", str(archive)])

    result = run_cli(["list", str(archive)])

    assert result.returncode == 0
    for f in files:
        assert f.name in result.stdout.decode()


# ---------------------------------------------------------------------------
# Compress tests
# ---------------------------------------------------------------------------


def test_compress_format_autodetect_zip(temp_dir, run_cli):
    """Compression format should be auto-detected from the output extension."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("hello")
    output = temp_dir / "out.zip"

    result = run_cli(["compress", str(test_file), "-o", str(output)])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert output.exists()
    assert output.read_bytes()[:4] == b"PK\x03\x04"


def test_compress_different_levels(temp_dir, run_cli):
    """Different compression levels should produce archives successfully."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("A" * 1000)

    for level in ("Fastest", "Fast", "Normal", "Max", "Ultra"):
        out = temp_dir / f"lvl_{level}.7z"
        result = run_cli(
            ["compress", str(test_file), "-o", str(out), "-l", level, "-f", "7z"]
        )
        assert result.returncode == 0, result.stderr.decode(errors="replace")
        assert out.exists()


def test_compress_different_methods(temp_dir, run_cli):
    """Compression with explicit methods should work for the chosen format."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("compressible data " * 100)

    for method in ("Lzma", "Lzma2", "BZip2", "Ppmd", "Copy"):
        out = temp_dir / f"m_{method}.7z"
        result = run_cli(
            ["compress", str(test_file), "-o", str(out), "-m", method, "-f", "7z"]
        )
        assert result.returncode == 0, result.stderr.decode(errors="replace")
        assert out.exists()

    out = temp_dir / "m_deflate.zip"
    result = run_cli(
        ["compress", str(test_file), "-o", str(out), "-m", "Deflate", "-f", "zip"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()


@pytest.mark.parametrize(
    "codec",
    ["brotli", "flzma2", "lizard", "lz4", "lz5", "zstd"],
)
def test_compress_external_codec_roundtrip(temp_dir, run_cli, codec):
    """Each external codec must compress and extract losslessly via the CLI."""
    test_file = temp_dir / "data.txt"
    content = "external codec roundtrip content " * 50
    test_file.write_text(content)

    archive = temp_dir / f"{codec}.7z"
    result = run_cli(
        ["compress", str(test_file), "-o", str(archive), "-m", codec, "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert archive.exists()
    assert archive.stat().st_size > 0

    extract_dir = temp_dir / "out"
    result = run_cli(["extract", str(archive), "-o", str(extract_dir)])
    assert result.returncode == 0, result.stderr.decode(errors="replace")

    extracted = (extract_dir / test_file.name).read_text()
    assert extracted == content


def test_compress_solid_mode(temp_dir, run_cli):
    """Solid compression should work for 7z format."""
    files = []
    for i in range(3):
        f = temp_dir / f"solid_{i}.txt"
        f.write_text(f"content {i} " * 50)
        files.append(f)

    out = temp_dir / "solid.7z"
    result = run_cli(
        ["compress"] + [str(f) for f in files] + ["-o", str(out), "--solid", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()


def test_compress_threads(temp_dir, run_cli):
    """Multi-threaded compression should work."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data " * 2000)

    out = temp_dir / "threads.7z"
    result = run_cli(
        ["compress", str(test_file), "-o", str(out), "--threads", "4", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()


def test_compress_password_crypt_headers(temp_dir, run_cli):
    """Archive with encrypted headers should require a password to list."""
    test_file = temp_dir / "secret.txt"
    test_file.write_text("confidential")

    out = temp_dir / "locked.7z"
    result = run_cli(
        ["compress", str(test_file), "-o", str(out), "-p", "pass123", "--crypt-headers"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()

    result = run_cli(["list", str(out)])
    assert result.returncode != 0

    result = run_cli(["list", str(out), "-p", "pass123"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "secret.txt" in result.stdout.decode()


def test_compress_exclude(temp_dir, run_cli):
    """Exclude patterns should skip matching files."""
    keep = temp_dir / "keep.txt"
    skip = temp_dir / "skip.log"
    keep.write_text("kept")
    skip.write_text("skipped")

    out = temp_dir / "excluded.7z"
    result = run_cli(
        ["compress", str(temp_dir), "-o", str(out), "-x", "*.log", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")

    result = run_cli(["list", str(out)])
    assert "keep.txt" in result.stdout.decode()
    assert "skip.log" not in result.stdout.decode()


def test_compress_delete_after(temp_dir, run_cli):
    """--delete-after should remove source files after compression."""
    test_file = temp_dir / "todelete.txt"
    test_file.write_text("gone soon")

    out = temp_dir / "del_after.7z"
    result = run_cli(
        ["compress", str(test_file), "-o", str(out), "--delete-after", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert not test_file.exists()
    assert out.exists()


def test_compress_stdin(temp_dir, run_cli):
    """Reading input from stdin should compress it under stdin-name."""
    out = temp_dir / "from_stdin.7z"
    payload = b"stdin payload data"
    result = run_cli(
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

    extracted = temp_dir / "stdin_out"
    result = run_cli(["extract", str(out), "-o", str(extracted)])
    assert result.returncode == 0
    assert (extracted / "payload.bin").read_bytes() == payload


def test_compress_to_stdout(temp_dir, run_cli):
    """Compressing to stdout ('-o -') should write the archive bytes to stdout."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("pipe me")

    result = run_cli(["compress", str(test_file), "-o", "-", "-f", "7z"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert result.stdout[:6] == b"7z\xbc\xaf\x27\x1c"


def test_compress_no_store_times(temp_dir, run_cli):
    """--no-store-times should not crash and produce an archive."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("timeless")

    out = temp_dir / "notimes.7z"
    result = run_cli(
        ["compress", str(test_file), "-o", str(out), "--no-store-times", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()


def test_compress_dictionary_word_size(temp_dir, run_cli):
    """Dictionary and word size options should be accepted."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("dictionary data " * 200)

    out = temp_dir / "dictsize.7z"
    result = run_cli(
        [
            "compress",
            str(test_file),
            "-o",
            str(out),
            "--dictionary-size",
            "16777216",
            "--word-size",
            "64",
            "-f",
            "7z",
        ]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert out.exists()


def test_compress_multiple_formats(temp_dir, run_cli):
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
        result = run_cli(["compress", str(test_file), "-o", str(out), "-f", fmt])
        assert result.returncode == 0, (
            f"{fmt}: {result.stderr.decode(errors='replace')}"
        )
        assert out.exists()
        assert out.stat().st_size > 0


def test_compress_show_files(temp_dir, run_cli):
    """--show-files should log each processed file to stderr."""
    test_file = temp_dir / "logged.txt"
    test_file.write_text("logged content")

    out = temp_dir / "shown.7z"
    result = run_cli(
        ["compress", str(test_file), "-o", str(out), "--show-files", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "logged.txt" in result.stderr.decode(errors="replace")


def test_compress_progress(temp_dir, run_cli):
    """--progress should not crash and should emit progress output."""
    test_file = temp_dir / "prog.txt"
    test_file.write_text("progress data " * 500)

    out = temp_dir / "progress.7z"
    result = run_cli(
        ["compress", str(test_file), "-o", str(out), "--progress", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "Progress" in result.stderr.decode(errors="replace")


def test_compress_ratio(temp_dir, run_cli):
    """--ratio should report compression ratio on stderr."""
    test_file = temp_dir / "ratio.txt"
    test_file.write_text("compressible " * 1000)

    out = temp_dir / "ratio.7z"
    result = run_cli(
        ["compress", str(test_file), "-o", str(out), "--ratio", "-f", "7z"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "Ratio" in result.stderr.decode(errors="replace")


# ---------------------------------------------------------------------------
# Extract tests
# ---------------------------------------------------------------------------


def test_extract_by_indices(temp_dir, run_cli, make_archive):
    """Extracting by index should only retrieve the selected items."""
    files = [temp_dir / f"f{i}.txt" for i in range(3)]
    for i, f in enumerate(files):
        f.write_text(f"file {i}")
    archive = make_archive(temp_dir, files)

    out = temp_dir / "idx_out"
    result = run_cli(["extract", str(archive), "-o", str(out), "-i", "0"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    extracted = list(out.rglob("*.txt"))
    assert len(extracted) == 1
    assert extracted[0].read_text() == "file 0"


def test_extract_match_wildcard(temp_dir, run_cli, make_archive):
    """Wildcard matching should extract only the matching items."""
    files = [temp_dir / "keep.txt", temp_dir / "skip.log"]
    for f in files:
        f.write_text("data")
    archive = make_archive(temp_dir, files)

    out = temp_dir / "match_out"
    result = run_cli(["extract", str(archive), "-o", str(out), "--match", "*.txt"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    names = {p.name for p in out.rglob("*") if p.is_file()}
    assert names == {"keep.txt"}


def test_extract_match_regex(temp_dir, run_cli, make_archive):
    """Regex matching should extract matching items."""
    files = [temp_dir / "alpha.txt", temp_dir / "beta.log"]
    for f in files:
        f.write_text("data")
    archive = make_archive(temp_dir, files)

    out = temp_dir / "re_out"
    result = run_cli(
        ["extract", str(archive), "-o", str(out), "--match-regex", r".*\.log"]
    )
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    names = {p.name for p in out.rglob("*") if p.is_file()}
    assert names == {"beta.log"}


def test_extract_filter_policy_exclude(temp_dir, run_cli, make_archive):
    """Exclude filter policy should extract everything except matches."""
    files = [temp_dir / "a.txt", temp_dir / "b.log"]
    for f in files:
        f.write_text("data")
    archive = make_archive(temp_dir, files)

    out = temp_dir / "filt_out"
    result = run_cli(
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
def test_extract_to_stdout(temp_dir, run_cli, make_archive, extra_args, expected):
    """--to-stdout should write the selected item's content to stdout."""
    files = [temp_dir / "first.txt", temp_dir / "second.txt"]
    files[0].write_text("first content")
    files[1].write_text("second content")
    archive = make_archive(temp_dir, files)

    result = run_cli(["extract", str(archive), "--to-stdout", *extra_args])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert result.stdout == expected


def test_extract_password(temp_dir, run_cli, make_archive):
    """Extracting a password-protected archive should require the password."""
    test_file = temp_dir / "secret.txt"
    test_file.write_text("secret data")
    archive = make_archive(temp_dir, [test_file], name="pwd.7z", extra=["-p", "abc"])

    out = temp_dir / "pwd_out"
    result = run_cli(["extract", str(archive), "-o", str(out)])
    assert result.returncode != 0

    out2 = temp_dir / "pwd_out2"
    result = run_cli(["extract", str(archive), "-o", str(out2), "-p", "abc"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert (out2 / "secret.txt").exists()


def test_extract_show_files(temp_dir, run_cli, make_archive):
    """--show-files during extraction should log files to stderr."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = make_archive(temp_dir, [test_file])

    out = temp_dir / "show_out"
    result = run_cli(["extract", str(archive), "-o", str(out), "--show-files"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "data.txt" in result.stderr.decode(errors="replace")


def test_extract_progress(temp_dir, run_cli, make_archive):
    """--progress during extraction should not crash."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data " * 500)
    archive = make_archive(temp_dir, [test_file])

    out = temp_dir / "prog_out"
    result = run_cli(["extract", str(archive), "-o", str(out), "--progress"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")


# ---------------------------------------------------------------------------
# List tests
# ---------------------------------------------------------------------------


def test_list_verbose(temp_dir, run_cli, make_archive):
    """Verbose listing should include solid/encrypted/volumes info."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = make_archive(temp_dir, [test_file])

    result = run_cli(["list", str(archive), "-v"])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    out = result.stdout.decode()
    assert "Solid" in out
    assert "Encrypted" in out
    assert "Volumes" in out
    assert "data.txt" in out


# ---------------------------------------------------------------------------
# Test archive integrity
# ---------------------------------------------------------------------------


def test_test_archive_valid(temp_dir, run_cli, make_archive):
    """The 'test' command should report a valid archive as passing."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = make_archive(temp_dir, [test_file])

    result = run_cli(["test", str(archive)])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    assert "integrity test passed" in result.stdout.decode().lower()


def test_test_archive_invalid(temp_dir, run_cli):
    """The 'test' command should fail on a corrupted archive."""
    archive = temp_dir / "broken.7z"
    archive.write_bytes(b"not a real archive")

    result = run_cli(["test", str(archive)])
    assert result.returncode != 0


# ---------------------------------------------------------------------------
# Info tests
# ---------------------------------------------------------------------------


def test_info_archive(temp_dir, run_cli, make_archive):
    """The 'info' command should print archive metadata."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("info data")
    archive = make_archive(temp_dir, [test_file])

    result = run_cli(["info", str(archive)])
    assert result.returncode == 0, result.stderr.decode(errors="replace")
    out = result.stdout.decode()
    assert "Format:" in out
    assert "Items count:" in out
    assert "Solid:" in out
    assert "Encrypted:" in out


def test_info_verbose(temp_dir, run_cli, make_archive):
    """Verbose info should print archive properties."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("info data")
    archive = make_archive(temp_dir, [test_file])

    result = run_cli(["info", str(archive), "-v"])
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
def test_update_delete(temp_dir, run_cli, make_archive, delete_args):
    """Deleting an item (by path or index) should remove it from the archive."""
    files = [temp_dir / "a.txt", temp_dir / "b.txt"]
    for f in files:
        f.write_text("data")
    archive = make_archive(temp_dir, files)

    result = run_cli(["update", str(archive), "-f", "7z", *delete_args])
    assert result.returncode == 0, result.stderr.decode(errors="replace")

    listing = run_cli(["list", str(archive)]).stdout.decode()
    assert "a.txt" not in listing
    assert "b.txt" in listing


@pytest.mark.parametrize(
    "rename_args",
    [
        ["--rename", "old_name.txt=new_name.txt"],
        ["--rename-index", "0:new_name.txt"],
    ],
)
def test_update_rename(temp_dir, run_cli, make_archive, rename_args):
    """Renaming an item (by path or index) should change its name."""
    test_file = temp_dir / "old_name.txt"
    test_file.write_text("data")
    archive = make_archive(temp_dir, [test_file])

    result = run_cli(["update", str(archive), "-f", "7z", *rename_args])
    assert result.returncode == 0, result.stderr.decode(errors="replace")

    listing = run_cli(["list", str(archive)]).stdout.decode()
    assert "new_name.txt" in listing
    assert "old_name.txt" not in listing


def test_update_requires_format(temp_dir, run_cli, make_archive):
    """Update with auto format should report an error."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = make_archive(temp_dir, [test_file])

    result = run_cli(["update", str(archive), "--delete", "data.txt"])
    assert result.returncode != 0
    assert "explicit writable format" in result.stderr.decode().lower()


def test_update_no_operations(temp_dir, run_cli, make_archive):
    """Update without any operation should exit with code 2."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = make_archive(temp_dir, [test_file])

    result = run_cli(["update", str(archive), "-f", "7z"])
    assert result.returncode == 2


# ---------------------------------------------------------------------------
# Error handling tests
# ---------------------------------------------------------------------------


def test_compress_missing_output(run_cli):
    """Compression without an output path should error."""
    result = run_cli(["compress", "anything"])
    assert result.returncode != 0
    assert "Output file path is required" in result.stderr.decode()


def test_compress_missing_inputs(run_cli):
    """Compression without input paths (and no --stdin) should error."""
    result = run_cli(["compress", "-o", "out.7z"])
    assert result.returncode != 0
    assert "Input paths are required" in result.stderr.decode()


def test_extract_missing_output(run_cli):
    """Extraction without output or --to-stdout should error."""
    result = run_cli(["extract", "any.7z"])
    assert result.returncode != 0
    assert "Output file/directory path is required" in result.stderr.decode()


def test_compress_invalid_format_property(temp_dir, run_cli):
    """An invalid --format-property should raise a clear error."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    out = temp_dir / "badprop.7z"

    result = run_cli(
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


def test_update_invalid_rename_spec(temp_dir, run_cli, make_archive):
    """An invalid --rename spec should raise a clear error."""
    test_file = temp_dir / "data.txt"
    test_file.write_text("data")
    archive = make_archive(temp_dir, [test_file])

    result = run_cli(["update", str(archive), "-f", "7z", "--rename", "bad-spec"])
    assert result.returncode != 0
    assert "Invalid --rename spec" in result.stderr.decode()
