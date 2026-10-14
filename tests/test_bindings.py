from __future__ import annotations

import datetime

import pybit7z
from pybit7z import (
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


def _make_archive(lib, files, archive_path, fmt=FormatSevenZip):
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

    def test_string_via_property(self, tmp_path):
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

    def test_from_file_path(self, tmp_path):
        f = tmp_path / "input.txt"
        f.write_text("file content here")
        item = BitInputItem(str(f))
        assert not item.is_dir()
        assert item.size() == len(b"file content here")
        assert str(f) in item.path()

    def test_from_file_path_with_archive_path(self, tmp_path):
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
    def _make(self, lib, tmp_path):
        f1 = tmp_path / "a.txt"
        f1.write_text("aaa")
        f2 = tmp_path / "b.txt"
        f2.write_text("bbb")
        arc = str(tmp_path / "test.7z")
        _make_archive(lib, [str(f1), str(f2)], arc)
        return arc

    def test_counts_and_contains(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            assert reader.items_count() == 2
            assert reader.files_count() == 2
            assert reader.folders_count() == 0
            assert reader.contains("a.txt")
            assert not reader.contains("nope.txt")

    def test_item_at(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            item = reader.item_at(0)
            assert isinstance(item, BitArchiveItem)
            assert item.name() in ("a.txt", "b.txt")

    def test_is_item_folder_encrypted(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            assert not reader.is_item_folder(0)
            assert not reader.is_item_encrypted(0)

    def test_detected_and_extraction_format(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            assert reader.detected_format() == FormatSevenZip
            assert reader.extraction_format() == FormatSevenZip

    def test_archive_path(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            assert reader.archive_path().endswith("test.7z")

    def test_test_method(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            reader.test()


# ---------------------------------------------------------------------------
# BitArchiveEditor: delete_item & rename_item
# ---------------------------------------------------------------------------


class TestBitArchiveEditorDeleteRename:
    def _make(self, lib, tmp_path):
        f1 = tmp_path / "a.txt"
        f1.write_text("aaa")
        f2 = tmp_path / "b.txt"
        f2.write_text("bbb")
        f3 = tmp_path / "c.log"
        f3.write_text("ccc")
        arc = str(tmp_path / "test.7z")
        _make_archive(lib, [str(f1), str(f2), str(f3)], arc)
        return arc

    def test_delete_by_index(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            editor = BitArchiveEditor(lib, arc, FormatSevenZip)
            editor.delete_item(0)
            editor.apply_changes()

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            names = sorted(i.name() for i in reader.items())
            assert names == ["b.txt", "c.log"]

    def test_delete_by_path(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            editor = BitArchiveEditor(lib, arc, FormatSevenZip)
            editor.delete_item("b.txt")
            editor.apply_changes()

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            names = sorted(i.name() for i in reader.items())
            assert names == ["a.txt", "c.log"]

    def test_rename_by_index(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            editor = BitArchiveEditor(lib, arc, FormatSevenZip)
            editor.rename_item(0, "renamed.txt")
            editor.apply_changes()

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            names = [i.name() for i in reader.items()]
            assert "renamed.txt" in names

    def test_rename_by_path(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            editor = BitArchiveEditor(lib, arc, FormatSevenZip)
            editor.rename_item("b.txt", "new_b.txt")
            editor.apply_changes()

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            names = [i.name() for i in reader.items()]
            assert "new_b.txt" in names
            assert "b.txt" not in names

    def test_set_update_mode(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            arc = self._make(lib, tmp_path)
            editor = BitArchiveEditor(lib, arc, FormatSevenZip)
            editor.set_update_mode(UpdateMode.Append)
            editor.apply_changes()


# ---------------------------------------------------------------------------
# BitOutputArchive: add_files / add_directory / compress_to
# ---------------------------------------------------------------------------


class TestBitOutputArchiveMethods:
    def test_add_files_list(self, tmp_path):
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

    def test_add_directory(self, tmp_path):
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

    def test_add_directory_contents(self, tmp_path):
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

    def test_add_file_item_returns_input_item(self, tmp_path):
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
    def test_item_fields(self, tmp_path):
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

    def test_item_property(self, tmp_path):
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
    def test_compress_with_renamed_map(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            f = tmp_path / "a.txt"
            f.write_text("aaa")
            arc = str(tmp_path / "out.7z")
            comp = BitFileCompressor(lib, FormatSevenZip)
            comp.compress({str(f): "renamed.txt"}, arc)

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            names = [i.name() for i in reader.items()]
            assert names == ["renamed.txt"]

    def test_compress_directory(self, tmp_path):
        with pybit7z.lib7zip_context() as lib:
            sub = tmp_path / "sub"
            sub.mkdir()
            (sub / "a.txt").write_text("a")
            arc = str(tmp_path / "out.7z")
            comp = BitFileCompressor(lib, FormatSevenZip)
            comp.compress_directory(str(sub), arc)

            reader = BitArchiveReader(lib, arc, FormatSevenZip)
            assert reader.files_count() == 1

    def test_compress_files(self, tmp_path):
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
