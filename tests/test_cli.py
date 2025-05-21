from __future__ import annotations

import subprocess


def test_cli_help():
    """Test the CLI help message"""
    result = subprocess.run(
        ["pybit7z", "--help"], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0
    assert "pybit7z command-line compression tool" in result.stdout


def test_compress_basic(temp_dir):
    """Test basic compression functionality"""
    test_file = temp_dir / "test.txt"
    test_file.write_text("sample content")
    output = temp_dir / "test.7z"

    result = subprocess.run(
        ["pybit7z", "compress", str(test_file), "-o", str(output), "-f", "7z"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert output.exists()
    assert "Successfully created archive" in result.stdout


def test_decompress_basic(temp_dir):
    """Test basic decompression functionality"""
    # Create test archive
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")
    archive = temp_dir / "test.7z"
    subprocess.run(
        ["pybit7z", "compress", str(test_file), "-o", str(archive)],
        capture_output=True,
        check=False,
    )

    # Test decompression
    output_dir = temp_dir / "output"
    result = subprocess.run(
        ["pybit7z", "decompress", str(archive), "-o", str(output_dir)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert (output_dir / test_file.name).exists()


def test_invalid_parameters(temp_dir):
    """Test handling of invalid parameters"""
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")
    output = temp_dir / "test.invalid"

    result = subprocess.run(
        ["pybit7z", "compress", str(test_file), "-o", str(output), "-f", "invalid"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "error: argument -f/--format" in result.stderr

    result = subprocess.run(
        ["pybit7z", "decompress", str(test_file), "-f", "7z"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "Output file/directory path is required" in result.stderr


def test_password_protection(temp_dir):
    """Test password protection for compression and decryption"""
    test_file = temp_dir / "secret.txt"
    test_file.write_text("confidential")
    output = temp_dir / "protected.7z"

    # Compress with password
    compress_cmd = [
        "pybit7z",
        "compress",
        str(test_file),
        "-o",
        str(output),
        "-p",
        "mypassword",
    ]
    assert subprocess.run(compress_cmd, check=False).returncode == 0

    # Decompress without password should fail
    extract_dir = temp_dir / "extracted"
    result = subprocess.run(
        ["pybit7z", "decompress", str(output), "-o", str(extract_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "a password is required" in result.stderr.lower()

    # Decompress with correct password
    result = subprocess.run(
        [
            "pybit7z",
            "decompress",
            str(output),
            "-o",
            str(extract_dir),
            "-p",
            "mypassword",
        ],
        capture_output=True,
        text=True,
        check=False,
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

    subprocess.run(
        ["pybit7z", "compress"] + [str(f) for f in files] + ["-o", str(archive)],
        capture_output=True,
        check=False,
    )

    # Test archive listing
    result = subprocess.run(
        ["pybit7z", "list", str(archive)], capture_output=True, text=True, check=False
    )

    assert result.returncode == 0
    for f in files:
        assert f.name in result.stdout
