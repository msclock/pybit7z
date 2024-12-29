#include <pybind11/chrono.h>
#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include "_core.hpp"
#include "pybit7z.hpp"

namespace py = pybind11;
using namespace py::literals;

PYBIND11_MODULE(_core, m) {
    m.doc() = R"pbdoc(
      Pybind11 _core plugin
      -----------------------
      .. currentmodule:: _core
    )pbdoc";

    m.def("version", []() { return _core::ProjectVersion(); }, R"pbdoc(
        The _core plugin version.
    )pbdoc");

    m.def(
        "set_lib7zip_path",
        [](const std::string &path = std::string()) {
            if (path.empty()) {
                return _core::default_library_path();
            }
            _core::default_library_path() = path;
            return _core::default_library_path();
        },
        py::arg("lib7zip_path") = std::string(),
        py::doc(R"pbdoc(Configure the path to the 7zip library.)pbdoc"));

    m.def(
        "set_large_page_mode",
        []() { const_cast<bit7z::Bit7zLibrary &>(_core::Bit7zipSingleton::getInstance()).setLargePageMode(); },
        py::doc(R"pbdoc(Enable large page mode for 7zip library. This can improve performance on some systems.)pbdoc"));

    // Exception handling
    py::register_exception<bit7z::BitException>(m, "BitException");

    // CompressionLevel enum bindings
    py::enum_<bit7z::BitCompressionLevel>(m, "BitCompressionLevel", R"pbdoc(Compression level for 7zip library)pbdoc")
        .value("Nothing", bit7z::BitCompressionLevel::None)
        .value("Fastest", bit7z::BitCompressionLevel::Fastest)
        .value("Fast", bit7z::BitCompressionLevel::Fast)
        .value("Normal", bit7z::BitCompressionLevel::Normal)
        .value("Max", bit7z::BitCompressionLevel::Max)
        .value("Ultra", bit7z::BitCompressionLevel::Ultra)
        .export_values();

    // CompressionMethod enum bindings
    py::enum_<bit7z::BitCompressionMethod>(m,
                                           "BitCompressionMethod",
                                           R"pbdoc(Compression method by bit7z when creating archives.)pbdoc")
        .value("Copy", bit7z::BitCompressionMethod::Copy)
        .value("Deflate", bit7z::BitCompressionMethod::Deflate)
        .value("Deflate64", bit7z::BitCompressionMethod::Deflate64)
        .value("BZip2", bit7z::BitCompressionMethod::BZip2)
        .value("Lzma", bit7z::BitCompressionMethod::Lzma)
        .value("Lzma2", bit7z::BitCompressionMethod::Lzma2)
        .value("Ppmd", bit7z::BitCompressionMethod::Ppmd)
        .export_values();

    // FormatFeatures enum bindings
    py::enum_<bit7z::FormatFeatures>(m, "FormatFeatures", R"pbdoc(Features of a format supported by bit7z)pbdoc")
        .value("MultipleFiles", bit7z::FormatFeatures::MultipleFiles, R"pbdoc(Archive supports multiple files.)pbdoc")
        .value("SolidArchive", bit7z::FormatFeatures::SolidArchive, R"pbdoc(Archive supports solid mode.)pbdoc")
        .value("CompressionLevel",
               bit7z::FormatFeatures::CompressionLevel,
               R"pbdoc(Archive supports compression level.)pbdoc")
        .value("Encryption", bit7z::FormatFeatures::Encryption, R"pbdoc(Archive supports encryption.)pbdoc")
        .value("HeaderEncryption",
               bit7z::FormatFeatures::HeaderEncryption,
               R"pbdoc(Archive supports encrypted headers.)pbdoc")
        .value("MultipleMethods",
               bit7z::FormatFeatures::MultipleMethods,
               R"pbdoc(Archive supports multiple compression methods.)pbdoc");

    // bit7z:: DeletePolicy enum bindings
    py::enum_<bit7z::DeletePolicy>(m, "DeletePolicy", R"pbdoc(Delete policy for archive items.)pbdoc")
        .value("ItemOnly", bit7z::DeletePolicy::ItemOnly)
        .value("RecurseDirs", bit7z::DeletePolicy::RecurseDirs)
        .export_values();

    // bit7z::BitInFormat class bindings
    py::class_<bit7z::BitInFormat>(m,
                                   "BitInFormat",
                                   R"pbdoc(The BitInFormat class specifies an extractable archive format.)pbdoc")
        .def("value", &bit7z::BitInFormat::value, py::doc(R"pbdoc(the value of the format in the 7z SDK.)pbdoc"))
        .def("__eq__", &bit7z::BitInFormat::operator==)
        .def("__ne__", &bit7z::BitInFormat::operator!=);

    // bit7z::BitInOutFormat class bindings
    py::class_<bit7z::BitInOutFormat, bit7z::BitInFormat>(
        m,
        "BitInOutFormat",
        R"pbdoc(The BitInOutFormat class specifies a format available for creating new archives and extract old ones.)pbdoc")
        .def("extension",
             &bit7z::BitInOutFormat::extension,
             py::doc(R"pbdoc(the default file extension of the archive format.)pbdoc"))
        .def("features",
             &bit7z::BitInOutFormat::features,
             py::doc(R"pbdoc(the bitset of the features supported by the format.)pbdoc"))
        .def("has_feature",
             &bit7z::BitInOutFormat::hasFeature,
             py::doc(R"pbdoc(Checks if the format has a specific feature (see FormatFeatures enum)
Args:
    feature (FormatFeatures): the feature to check
Returns:
    bool: a boolean value indicating whether the format has the given feature.)pbdoc"))
        .def("default_method",
             &bit7z::BitInOutFormat::defaultMethod,
             py::doc(R"pbdoc(the default method used for compressing the archive format.)pbdoc"));

    // Expose format constants as module attributes
    m.attr("FormatAuto") = py::cast(bit7z::BitFormat::Auto, py::return_value_policy::reference);
    m.attr("FormatRar") = py::cast(bit7z::BitFormat::Rar, py::return_value_policy::reference);
    m.attr("FormatArj") = py::cast(bit7z::BitFormat::Arj, py::return_value_policy::reference);
    m.attr("FormatZ") = py::cast(bit7z::BitFormat::Z, py::return_value_policy::reference);
    m.attr("FormatLzh") = py::cast(bit7z::BitFormat::Lzh, py::return_value_policy::reference);
    m.attr("FormatCab") = py::cast(bit7z::BitFormat::Cab, py::return_value_policy::reference);
    m.attr("FormatNsis") = py::cast(bit7z::BitFormat::Nsis, py::return_value_policy::reference);
    m.attr("FormatLzma") = py::cast(bit7z::BitFormat::Lzma, py::return_value_policy::reference);
    m.attr("FormatLzma86") = py::cast(bit7z::BitFormat::Lzma86, py::return_value_policy::reference);
    m.attr("FormatPpmd") = py::cast(bit7z::BitFormat::Ppmd, py::return_value_policy::reference);
    m.attr("FormatVhdx") = py::cast(bit7z::BitFormat::Vhdx, py::return_value_policy::reference);
    m.attr("FormatCoff") = py::cast(bit7z::BitFormat::COFF, py::return_value_policy::reference);
    m.attr("FormatExt") = py::cast(bit7z::BitFormat::Ext, py::return_value_policy::reference);
    m.attr("FormatVmdk") = py::cast(bit7z::BitFormat::VMDK, py::return_value_policy::reference);
    m.attr("FormatVdi") = py::cast(bit7z::BitFormat::VDI, py::return_value_policy::reference);
    m.attr("FormatQcow") = py::cast(bit7z::BitFormat::QCow, py::return_value_policy::reference);
    m.attr("FormatGpt") = py::cast(bit7z::BitFormat::GPT, py::return_value_policy::reference);
    m.attr("FormatRar5") = py::cast(bit7z::BitFormat::Rar5, py::return_value_policy::reference);
    m.attr("FormatIHex") = py::cast(bit7z::BitFormat::IHex, py::return_value_policy::reference);
    m.attr("FormatHxs") = py::cast(bit7z::BitFormat::Hxs, py::return_value_policy::reference);
    m.attr("FormatTE") = py::cast(bit7z::BitFormat::TE, py::return_value_policy::reference);
    m.attr("FormatUEFIc") = py::cast(bit7z::BitFormat::UEFIc, py::return_value_policy::reference);
    m.attr("FormatUEFIs") = py::cast(bit7z::BitFormat::UEFIs, py::return_value_policy::reference);
    m.attr("FormatSquashFS") = py::cast(bit7z::BitFormat::SquashFS, py::return_value_policy::reference);
    m.attr("FormatCramFS") = py::cast(bit7z::BitFormat::CramFS, py::return_value_policy::reference);
    m.attr("FormatAPM") = py::cast(bit7z::BitFormat::APM, py::return_value_policy::reference);
    m.attr("FormatMslz") = py::cast(bit7z::BitFormat::Mslz, py::return_value_policy::reference);
    m.attr("FormatFlv") = py::cast(bit7z::BitFormat::Flv, py::return_value_policy::reference);
    m.attr("FormatSwf") = py::cast(bit7z::BitFormat::Swf, py::return_value_policy::reference);
    m.attr("FormatSwfc") = py::cast(bit7z::BitFormat::Swfc, py::return_value_policy::reference);
    m.attr("FormatNtfs") = py::cast(bit7z::BitFormat::Ntfs, py::return_value_policy::reference);
    m.attr("FormatFat") = py::cast(bit7z::BitFormat::Fat, py::return_value_policy::reference);
    m.attr("FormatMbr") = py::cast(bit7z::BitFormat::Mbr, py::return_value_policy::reference);
    m.attr("FormatVhd") = py::cast(bit7z::BitFormat::Vhd, py::return_value_policy::reference);
    m.attr("FormatPe") = py::cast(bit7z::BitFormat::Pe, py::return_value_policy::reference);
    m.attr("FormatElf") = py::cast(bit7z::BitFormat::Elf, py::return_value_policy::reference);
    m.attr("FormatMacho") = py::cast(bit7z::BitFormat::Macho, py::return_value_policy::reference);
    m.attr("FormatUdf") = py::cast(bit7z::BitFormat::Udf, py::return_value_policy::reference);
    m.attr("FormatXar") = py::cast(bit7z::BitFormat::Xar, py::return_value_policy::reference);
    m.attr("FormatMub") = py::cast(bit7z::BitFormat::Mub, py::return_value_policy::reference);
    m.attr("FormatHfs") = py::cast(bit7z::BitFormat::Hfs, py::return_value_policy::reference);
    m.attr("FormatDmg") = py::cast(bit7z::BitFormat::Dmg, py::return_value_policy::reference);
    m.attr("FormatCompound") = py::cast(bit7z::BitFormat::Compound, py::return_value_policy::reference);
    m.attr("FormatIso") = py::cast(bit7z::BitFormat::Iso, py::return_value_policy::reference);
    m.attr("FormatChm") = py::cast(bit7z::BitFormat::Chm, py::return_value_policy::reference);
    m.attr("FormatSplit") = py::cast(bit7z::BitFormat::Split, py::return_value_policy::reference);
    m.attr("FormatRpm") = py::cast(bit7z::BitFormat::Rpm, py::return_value_policy::reference);
    m.attr("FormatDeb") = py::cast(bit7z::BitFormat::Deb, py::return_value_policy::reference);
    m.attr("FormatCpio") = py::cast(bit7z::BitFormat::Cpio, py::return_value_policy::reference);
    m.attr("FormatZip") = py::cast(bit7z::BitFormat::Zip, py::return_value_policy::reference);
    m.attr("FormatBZip2") = py::cast(bit7z::BitFormat::BZip2, py::return_value_policy::reference);
    m.attr("FormatSevenZip") = py::cast(bit7z::BitFormat::SevenZip, py::return_value_policy::reference);
    m.attr("FormatXz") = py::cast(bit7z::BitFormat::Xz, py::return_value_policy::reference);
    m.attr("FormatWim") = py::cast(bit7z::BitFormat::Wim, py::return_value_policy::reference);
    m.attr("FormatTar") = py::cast(bit7z::BitFormat::Tar, py::return_value_policy::reference);
    m.attr("FormatGZip") = py::cast(bit7z::BitFormat::GZip, py::return_value_policy::reference);

    // BitProperty enum bindings
    py::enum_<bit7z::BitProperty>(
        m,
        "BitProperty",
        R"pbdoc(The BitProperty enum represents the archive/item properties that 7-zip can read or write.)pbdoc")
        .value("NoProperty", bit7z::BitProperty::NoProperty)
        .value("MainSubfile", bit7z::BitProperty::MainSubfile)
        .value("HandlerItemIndex", bit7z::BitProperty::HandlerItemIndex)
        .value("Path", bit7z::BitProperty::Path)
        .value("Name", bit7z::BitProperty::Name)
        .value("Extension", bit7z::BitProperty::Extension)
        .value("IsDir", bit7z::BitProperty::IsDir)
        .value("Size", bit7z::BitProperty::Size)
        .value("PackSize", bit7z::BitProperty::PackSize)
        .value("Attrib", bit7z::BitProperty::Attrib)
        .value("CTime", bit7z::BitProperty::CTime)
        .value("ATime", bit7z::BitProperty::ATime)
        .value("MTime", bit7z::BitProperty::MTime)
        .value("Solid", bit7z::BitProperty::Solid)
        .value("Commented", bit7z::BitProperty::Commented)
        .value("Encrypted", bit7z::BitProperty::Encrypted)
        .value("SplitBefore", bit7z::BitProperty::SplitBefore)
        .value("SplitAfter", bit7z::BitProperty::SplitAfter)
        .value("DictionarySize", bit7z::BitProperty::DictionarySize)
        .value("CRC", bit7z::BitProperty::CRC)
        .value("Type", bit7z::BitProperty::Type)
        .value("IsAnti", bit7z::BitProperty::IsAnti)
        .value("Method", bit7z::BitProperty::Method)
        .value("HostOS", bit7z::BitProperty::HostOS)
        .value("FileSystem", bit7z::BitProperty::FileSystem)
        .value("User", bit7z::BitProperty::User)
        .value("Group", bit7z::BitProperty::Group)
        .value("Block", bit7z::BitProperty::Block)
        .value("Comment", bit7z::BitProperty::Comment)
        .value("Position", bit7z::BitProperty::Position)
        .value("Prefix", bit7z::BitProperty::Prefix)
        .value("NumSubDirs", bit7z::BitProperty::NumSubDirs)
        .value("NumSubFiles", bit7z::BitProperty::NumSubFiles)
        .value("UnpackVer", bit7z::BitProperty::UnpackVer)
        .value("Volume", bit7z::BitProperty::Volume)
        .value("IsVolume", bit7z::BitProperty::IsVolume)
        .value("Offset", bit7z::BitProperty::Offset)
        .value("Links", bit7z::BitProperty::Links)
        .value("NumBlocks", bit7z::BitProperty::NumBlocks)
        .value("NumVolumes", bit7z::BitProperty::NumVolumes)
        .value("TimeType", bit7z::BitProperty::TimeType)
        .value("Bit64", bit7z::BitProperty::Bit64)
        .value("BigEndian", bit7z::BitProperty::BigEndian)
        .value("Cpu", bit7z::BitProperty::Cpu)
        .value("PhySize", bit7z::BitProperty::PhySize)
        .value("HeadersSize", bit7z::BitProperty::HeadersSize)
        .value("Checksum", bit7z::BitProperty::Checksum)
        .value("Characters", bit7z::BitProperty::Characts)
        .value("Va", bit7z::BitProperty::Va)
        .value("Id", bit7z::BitProperty::Id)
        .value("ShortName", bit7z::BitProperty::ShortName)
        .value("CreatorApp", bit7z::BitProperty::CreatorApp)
        .value("SectorSize", bit7z::BitProperty::SectorSize)
        .value("PosixAttrib", bit7z::BitProperty::PosixAttrib)
        .value("SymLink", bit7z::BitProperty::SymLink)
        .value("Error", bit7z::BitProperty::Error)
        .value("TotalSize", bit7z::BitProperty::TotalSize)
        .value("FreeSpace", bit7z::BitProperty::FreeSpace)
        .value("ClusterSize", bit7z::BitProperty::ClusterSize)
        .value("VolumeName", bit7z::BitProperty::VolumeName)
        .value("LocalName", bit7z::BitProperty::LocalName)
        .value("Provider", bit7z::BitProperty::Provider)
        .value("NtSecure", bit7z::BitProperty::NtSecure)
        .value("IsAltStream", bit7z::BitProperty::IsAltStream)
        .value("IsAux", bit7z::BitProperty::IsAux)
        .value("IsDeleted", bit7z::BitProperty::IsDeleted)
        .value("IsTree", bit7z::BitProperty::IsTree)
        .value("Sha1", bit7z::BitProperty::Sha1)
        .value("Sha256", bit7z::BitProperty::Sha256)
        .value("ErrorType", bit7z::BitProperty::ErrorType)
        .value("NumErrors", bit7z::BitProperty::NumErrors)
        .value("ErrorFlags", bit7z::BitProperty::ErrorFlags)
        .value("WarningFlags", bit7z::BitProperty::WarningFlags)
        .value("Warning", bit7z::BitProperty::Warning)
        .value("NumStreams", bit7z::BitProperty::NumStreams)
        .value("NumAltStreams", bit7z::BitProperty::NumAltStreams)
        .value("AltStreamsSize", bit7z::BitProperty::AltStreamsSize)
        .value("VirtualSize", bit7z::BitProperty::VirtualSize)
        .value("UnpackSize", bit7z::BitProperty::UnpackSize)
        .value("TotalPhySize", bit7z::BitProperty::TotalPhySize)
        .value("VolumeIndex", bit7z::BitProperty::VolumeIndex)
        .value("SubType", bit7z::BitProperty::SubType)
        .value("ShortComment", bit7z::BitProperty::ShortComment)
        .value("CodePage", bit7z::BitProperty::CodePage)
        .value("IsNotArcType", bit7z::BitProperty::IsNotArcType)
        .value("PhySizeCantBeDetected", bit7z::BitProperty::PhySizeCantBeDetected)
        .value("ZerosTailIsAllowed", bit7z::BitProperty::ZerosTailIsAllowed)
        .value("TailSize", bit7z::BitProperty::TailSize)
        .value("EmbeddedStubSize", bit7z::BitProperty::EmbeddedStubSize)
        .value("NtReparse", bit7z::BitProperty::NtReparse)
        .value("HardLink", bit7z::BitProperty::HardLink)
        .value("INode", bit7z::BitProperty::INode)
        .value("StreamId", bit7z::BitProperty::StreamId)
        .value("ReadOnly", bit7z::BitProperty::ReadOnly)
        .value("OutName", bit7z::BitProperty::OutName)
        .value("CopyLink", bit7z::BitProperty::CopyLink)
        .export_values();

    // bit7z::BitPropVariantType enum bindings

    py::enum_<bit7z::BitPropVariantType>(
        m,
        "BitPropVariantType",
        R"pbdoc(The BitPropVariantType enum represents the possible types that a BitPropVariant can store.)pbdoc")
        .value("Empty", bit7z::BitPropVariantType::Empty)
        .value("Bool", bit7z::BitPropVariantType::Bool)
        .value("String", bit7z::BitPropVariantType::String)
        .value("UInt8", bit7z::BitPropVariantType::UInt8)
        .value("UInt16", bit7z::BitPropVariantType::UInt16)
        .value("UInt32", bit7z::BitPropVariantType::UInt32)
        .value("UInt64", bit7z::BitPropVariantType::UInt64)
        .value("Int8", bit7z::BitPropVariantType::Int8)
        .value("Int16", bit7z::BitPropVariantType::Int16)
        .value("Int32", bit7z::BitPropVariantType::Int32)
        .value("Int64", bit7z::BitPropVariantType::Int64)
        .value("FileTime", bit7z::BitPropVariantType::FileTime)
        .export_values();

    py::class_<bit7z::BitPropVariant>(
        m,
        "BitPropVariant",
        R"pbdoc(The BitPropVariant struct is a light extension to the WinAPI PROPVARIANT struct providing useful getters.)pbdoc")
        .def(py::init<>())
        .def(py::init<bool>(), py::arg("value"))
        .def(py::init<uint64_t>(), py::arg("value"))
        .def("get_string", &bit7z::BitPropVariant::getString)
        .def("get_native_string", &bit7z::BitPropVariant::getNativeString)
        .def("get_uint64", &bit7z::BitPropVariant::getUInt64)
        .def("get_int64", &bit7z::BitPropVariant::getInt64)
        .def("get_bool", &bit7z::BitPropVariant::getBool)
        .def("get_file_time", &bit7z::BitPropVariant::getTimePoint)
        .def("is_string", &bit7z::BitPropVariant::isString)
        .def("is_bool", &bit7z::BitPropVariant::isBool)
        .def("is_int8", &bit7z::BitPropVariant::isInt8)
        .def("is_int32", &bit7z::BitPropVariant::isInt32)
        .def("is_int16", &bit7z::BitPropVariant::isInt16)
        .def("is_int64", &bit7z::BitPropVariant::isInt64)
        .def("is_uint8", &bit7z::BitPropVariant::isUInt8)
        .def("is_uint16", &bit7z::BitPropVariant::isUInt16)
        .def("is_uint32", &bit7z::BitPropVariant::isUInt32)
        .def("is_uint64", &bit7z::BitPropVariant::isUInt64)
        .def("is_file_time", &bit7z::BitPropVariant::isFileTime)
        .def("type", &bit7z::BitPropVariant::type, py::doc(R"pbdoc(Returns the type of the variant.)pbdoc"))
        .def("clear", &bit7z::BitPropVariant::clear, py::doc(R"pbdoc(Clears the variant.)pbdoc"));

    // bit7z::BitGenericItem class bindings
    py::class_<bit7z::BitGenericItem>(
        m,
        "BitGenericItem",

        R"pbdoc(The BitGenericItem interface class represents a generic item (either inside or outside an archive).)pbdoc")
        .def("is_dir", &bit7z::BitGenericItem::isDir)
        .def("size", &bit7z::BitGenericItem::size, py::doc(R"pbdoc(the uncompressed size of the item.)pbdoc"))
        .def(
            "name",
            &bit7z::BitGenericItem::name,
            py::doc(
                R"pbdoc(the name of the item, if available or inferable from the path, or an empty string otherwise.)pbdoc"))
        .def("path", &bit7z::BitGenericItem::path, py::doc(R"pbdoc(the path of the item.)pbdoc"))
        .def("attributes", &bit7z::BitGenericItem::attributes, py::doc(R"pbdoc(the item attributes.)pbdoc"));

    // bit7z::BitArchiveItem class bindings
    py::class_<bit7z::BitArchiveItem, bit7z::BitGenericItem>(
        m,
        "BitArchiveItem",
        R"pbdoc(The BitArchiveItem class represents a generic item inside an archive.)pbdoc")
        .def("index", &bit7z::BitArchiveItem::index, py::doc(R"pbdoc(the index of the item in the archive.)pbdoc"))
        .def(
            "extension",
            &bit7z::BitArchiveItem::extension,
            py::doc(
                R"pbdoc(the extension of the item, if available or if it can be inferred from the name; otherwise it returns an empty string (e.g., when the item is a folder).)pbdoc"))
        .def(
            "native_path",
            &bit7z::BitArchiveItem::nativePath,
            py::doc(
                R"pbdoc(the path of the item in the archive, if available or inferable from the name, or an empty string otherwise.)pbdoc"))
        .def("creation_time", &bit7z::BitArchiveItem::creationTime)
        .def("last_access_time", &bit7z::BitArchiveItem::lastAccessTime)
        .def("last_write_time", &bit7z::BitArchiveItem::lastWriteTime)
        .def("attributes", &bit7z::BitArchiveItem::attributes, py::doc(R"pbdoc(the item attributes.)pbdoc"))
        .def("pack_size", &bit7z::BitArchiveItem::packSize, py::doc(R"pbdoc(the compressed size of the item.)pbdoc"))
        .def("crc", &bit7z::BitArchiveItem::crc, py::doc(R"pbdoc(the CRC of the item.)pbdoc"))
        .def("is_encrypted",
             &bit7z::BitArchiveItem::isEncrypted,
             py::doc(R"pbdoc(true if and only if the item is encrypted.)pbdoc"));

    // bit7z::BitArchiveItemOffset class bindings
    py::class_<bit7z::BitArchiveItemOffset, bit7z::BitArchiveItem>(
        m,
        "BitArchiveItemOffset",
        R"pbdoc(The BitArchiveItemOffset class represents an archived item but doesn't store its properties.)pbdoc")
        .def("__eq__", &bit7z::BitArchiveItemOffset::operator==)
        .def("__ne__", &bit7z::BitArchiveItemOffset::operator!=)
        .def("__iadd__", [](bit7z::BitArchiveItemOffset &self, int val) { return self.operator++(val); })
        .def("item_property",
             &bit7z::BitArchiveItemOffset::itemProperty,
             py::doc(R"pbdoc(Gets the specified item property.

Args:
    property_id (bit7z::BitProperty): The ID of the property to get.

Returns:
    BitPropVariant: the value of the item property, if available, or an empty BitPropVariant.
)pbdoc"));

    // bit7z::BitArchiveItemInfo class bindings
    py::class_<bit7z::BitArchiveItemInfo, bit7z::BitArchiveItem>(
        m,
        "BitArchiveItemInfo",

        R"pbdoc(The BitArchiveItemInfo class represents an archived item and that stores all its properties for later use.)pbdoc")
        .def("item_property",
             &bit7z::BitArchiveItemInfo::itemProperty,
             py::doc(R"pbdoc(Gets the specified item property.
Args:
    property_id (bit7z::BitProperty): The ID of the property to get.
Returns:
    BitPropVariant: the value of the item property, if available, or an empty BitPropVariant.
)pbdoc"))
        .def(
            "item_properties",
            &bit7z::BitArchiveItemInfo::itemProperties,
            py::doc(
                R"pbdoc(a map of all the available (i.e., non-empty) item properties and their respective values.)pbdoc"));

    py::enum_<bit7z::OverwriteMode>(
        m,
        "OverwriteMode",
        R"pbdoc(Enumeration representing how a handler should deal when an output file already exists.)pbdoc")
        .value("Nothing",
               bit7z::OverwriteMode::None,
               R"pbdoc(The handler will throw an exception if the output file or buffer already exists.)pbdoc")
        .value("Overwrite",
               bit7z::OverwriteMode::Overwrite,
               R"pbdoc(The handler will overwrite the old file or buffer with the new one.)pbdoc")
        .value("Skip",
               bit7z::OverwriteMode::Skip,
               R"pbdoc(The handler will skip writing to the output file or buffer.)pbdoc")
        .export_values();

    // bit7z:: BitAbstractArchiveHandler class bindings
    py::class_<bit7z::BitAbstractArchiveHandler>(m,
                                                 "BitAbstractArchiveHandler",
                                                 R"pbdoc(Abstract class representing a generic archive handler.)pbdoc")
        .def("format",
             &bit7z::BitAbstractArchiveHandler::format,
             py::doc(R"pbdoc(the format used by the handler for extracting or compressing.)pbdoc"))
        .def("password",
             &bit7z::BitAbstractArchiveHandler::password,
             py::doc(R"pbdoc(the password used to open, extract, or encrypt the archive.)pbdoc"))
        .def(
            "retainDirectories",
            &bit7z::BitAbstractArchiveHandler::retainDirectories,
            py::doc(
                R"pbdoc(a boolean value indicating whether the directory structure must be preserved while extracting or compressing the archive.)pbdoc"))
        .def("is_password_defined",
             &bit7z::BitAbstractArchiveHandler::isPasswordDefined,
             py::doc(R"pbdoc(a boolean value indicating whether a password is defined or not.)pbdoc"))
        .def("total_callback",
             &bit7z::BitAbstractArchiveHandler::totalCallback,
             py::doc(R"pbdoc(the current total callback.)pbdoc"))
        .def("progress_callback",
             &bit7z::BitAbstractArchiveHandler::progressCallback,
             py::doc(R"pbdoc(the current progress callback.)pbdoc"))
        .def("ratio_callback",
             &bit7z::BitAbstractArchiveHandler::ratioCallback,
             py::doc(R"pbdoc(the current ratio callback.)pbdoc"))
        .def("file_callback",
             &bit7z::BitAbstractArchiveHandler::fileCallback,
             py::doc(R"pbdoc(the current file callback.)pbdoc"))
        .def("password_callback",
             &bit7z::BitAbstractArchiveHandler::passwordCallback,
             py::doc(R"pbdoc(the current password callback.)pbdoc"))
        .def("overwrite_mode",
             &bit7z::BitAbstractArchiveHandler::overwriteMode,
             py::doc(R"pbdoc(the overwrite mode.)pbdoc"))
        .def("set_password",
             &bit7z::BitAbstractArchiveHandler::setPassword,
             py::arg("password"),
             py ::doc(R"pbdoc(Sets up a password to be used by the archive handler.

The password will be used to encrypt/decrypt archives by using the default cryptographic method of the archive format.

Args:
    password: the password to be used.

Note:
    Calling this method when the input archive is not encrypted does not have any effect on the extraction process.
    Calling this method when the output format doesn't support archive encryption (e.g., GZip, BZip2, etc...) does not have any effects (in other words, it doesn't throw exceptions, and it has no effects on compression operations).
    After a password has been set, it will be used for every subsequent operation. To disable the use of the password, you need to call the clear_password method, which is equivalent to calling set_password(L"").)pbdoc"))
        .def("clear_password",
             &bit7z::BitAbstractArchiveHandler::clearPassword,
             py::doc(R"pbdoc(Clear the current password used by the handler.

Calling clear_password() will disable the encryption/decryption of archives.

Note:
    This is equivalent to calling set_password(L"").)pbdoc"))
        .def("set_retain_directories",
             &bit7z::BitAbstractArchiveHandler::setRetainDirectories,
             py::arg("retain"),
             py::doc(R"pbdoc(Sets whether the operations' output will preserve the input's directory structure or not.

Args:
    retain: the setting for preserving or not the input directory structure)pbdoc"))
        .def("set_total_callback",
             &bit7z::BitAbstractArchiveHandler::setTotalCallback,
             py::arg("callback"),
             py::doc(R"pbdoc(Sets the function to be called when the total size of an operation is available.

Args:
    callback: the total callback to be used.
)pbdoc"))
        .def("set_progress_callback",
             &bit7z::BitAbstractArchiveHandler::setProgressCallback,
             py::arg("callback"),
             py::doc(R"pbdoc(Sets the function to be called when the processed size of the ongoing operation is updated.

Args:
    callback: the progress callback to be used.
Note:
    The completion percentage of the current operation can be obtained by calculating int((100.0 * processed_size) / total_size).
)pbdoc"))
        .def(
            "set_ratio_callback",
            &bit7z::BitAbstractArchiveHandler::setRatioCallback,
            py::arg("callback"),
            py::doc(
                R"pbdoc(Sets the function to be called when the input processed size and current output size of the ongoing operation are known.

Args:
    callback: the ratio callback to be used.
Note:
    The ratio percentage of a compression operation can be obtained by calculating int((100.0 * output_size) / input_size).
)pbdoc"))
        .def("set_file_callback",
             &bit7z::BitAbstractArchiveHandler::setFileCallback,
             py::arg("callback"),
             py::doc(R"pbdoc(Sets the function to be called when the current file being processed changes.

Args:
    callback: the file callback to be used.
)pbdoc"))
        .def("set_password_callback",
             &bit7z::BitAbstractArchiveHandler::setPasswordCallback,
             py::arg("callback"),
             py::doc(R"pbdoc(Sets the function to be called when a password is needed to complete the ongoing operation.

Args:
    callback: the password callback to be used.
)pbdoc"))
        .def("set_overwrite_mode",
             &bit7z::BitAbstractArchiveHandler::setOverwriteMode,
             py::arg("mode"),
             py::doc(
                 R"pbdoc(Sets how the handler should behave when it tries to output to an existing file or buffer.
Args:
    mode: the OverwriteMode to be used by the handler.)pbdoc"));

    // bit7z::BitAbstractArchiveOpener class bindings
    py::class_<bit7z::BitAbstractArchiveOpener, bit7z::BitAbstractArchiveHandler>(m, "BitAbstractArchiveOpener")
        .def("extraction_format",
             &bit7z::BitAbstractArchiveOpener::extractionFormat,
             py::doc(R"pbdoc(the archive format used by the archive opener.)pbdoc"));

    // bit7z::UpdateMode enum bindings
    py::enum_<bit7z::UpdateMode>(m, "UpdateMode")
        .value("Nothing", bit7z::UpdateMode::None)
        .value("Append", bit7z::UpdateMode::Append)
        .value("Update", bit7z::UpdateMode::Update);

    // bit7z::BitAbstractArchiveCreator class bindings
    py::class_<bit7z::BitAbstractArchiveCreator, bit7z::BitAbstractArchiveHandler>(
        m,
        "BitAbstractArchiveCreator",
        R"pbdoc(Abstract class representing a generic archive creator.)pbdoc")
        .def("compression_format",
             &bit7z::BitAbstractArchiveCreator::compressionFormat,
             py::doc(R"pbdoc(the format used for creating/updating an archive.)pbdoc"))
        .def("crypt_headers",
             &bit7z::BitAbstractArchiveCreator::cryptHeaders,
             py::doc(R"pbdoc(whether the creator crypts also the headers of archives or not.)pbdoc"))
        .def("compression_method",
             &bit7z::BitAbstractArchiveCreator::compressionMethod,
             py::doc(R"pbdoc(the compression method used for creating/updating an archive.)pbdoc"))
        .def("dictionary_size",
             &bit7z::BitAbstractArchiveCreator::dictionarySize,
             py::doc(R"pbdoc(the dictionary size used for creating/updating an archive.)pbdoc"))
        .def("word_size",
             &bit7z::BitAbstractArchiveCreator::wordSize,
             py::doc(R"pbdoc(the word size used for creating/updating an archive.)pbdoc"))
        .def("solid_mode",
             &bit7z::BitAbstractArchiveCreator::solidMode,
             py::doc(R"pbdoc(whether the archive creator uses solid compression or not.)pbdoc"))
        .def("update_mode",
             &bit7z::BitAbstractArchiveCreator::updateMode,
             py::doc(R"pbdoc(the update mode used when updating existing archives.)pbdoc"))
        .def(
            "volume_size",
            &bit7z::BitAbstractArchiveCreator::volumeSize,
            py::doc(
                R"pbdoc(the volume size (in bytes) used when creating multi-volume archives (a 0 value means that all files are going in a single archive).)pbdoc"))
        .def(
            "threads_count",
            &bit7z::BitAbstractArchiveCreator::threadsCount,
            py::doc(
                R"pbdoc(the number of threads used when creating/updating an archive (a 0 value means that it will use the 7-zip default value).)pbdoc"))
        .def("store_symbolic_links",
             &bit7z::BitAbstractArchiveCreator::storeSymbolicLinks,
             py::doc(R"pbdoc(whether the archive creator stores symbolic links as links in the output archive.)pbdoc"))
        .def("set_password",
             static_cast<void (bit7z::BitAbstractArchiveCreator::*)(const std::string &)>(
                 &bit7z::BitAbstractArchiveCreator::setPassword),
             py::arg("password"),
             py::doc(R"pydoc(Sets up a password for the output archives.

When setting a password, the produced archives will be encrypted using the default cryptographic method of the output format. The option "crypt headers" remains unchanged, in contrast with what happens when calling the set_password(tstring, bool) method.

Args:
    password: the password to be used when creating/updating archives.

Note:
    Calling set_password when the output format doesn't support archive encryption (e.g., GZip, BZip2, etc...) does not have any effects (in other words, it doesn't throw exceptions, and it has no effects on compression operations).
    After a password has been set, it will be used for every subsequent operation. To disable the use of the password, you need to call the clearPassword method (inherited from BitAbstractArchiveHandler), which is equivalent to set_password(L"").)pydoc"))
        .def("set_password",
             static_cast<void (bit7z::BitAbstractArchiveCreator::*)(const std::string &, bool)>(
                 &bit7z::BitAbstractArchiveCreator::setPassword),
             py::arg("password"),
             py::arg("crypt_headers"),
             py::doc(R"pydoc(Sets up a password for the output archive.

When setting a password, the produced archive will be encrypted using the default cryptographic method of the output format. If the format is 7z, and the option "cryptHeaders" is set to true, the headers of the archive will be encrypted, resulting in a password request every time the output file will be opened.

Args:
    password: the password to be used when creating/updating archives.
    crypt_headers: if true, the headers of the output archives will be encrypted (valid only when using the 7z format).

Note:
    Calling set_password when the output format doesn't support archive encryption (e.g., GZip, BZip2, etc...) does not have any effects (in other words, it doesn't throw exceptions, and it has no effects on compression operations).
    Calling set_password with "cryptHeaders" set to true does not have effects on formats different from 7z.
    After a password has been set, it will be used for every subsequent operation. To disable the use of the password, you need to call the clearPassword method (inherited from BitAbstractArchiveHandler), which is equivalent to set_password(L"").)pydoc"))
        .def("set_compression_level",
             &bit7z::BitAbstractArchiveCreator::setCompressionLevel,
             py::arg("level"),
             py::doc(R"pydoc(Sets the compression level to be used when creating/updating an archive.

Args:
    level: the compression level desired.)pydoc"))
        .def("set_compression_method",
             &bit7z::BitAbstractArchiveCreator::setCompressionMethod,
             py::arg("method"),
             py::doc(R"pydoc(Sets the compression method to be used when creating/updating an archive.

Args:
    method: the compression method desired.)pydoc"))
        .def("set_dictionary_size",
             &bit7z::BitAbstractArchiveCreator::setDictionarySize,
             py::arg("dictionary_size"),
             py::doc(R"pydoc(Sets the dictionary size to be used when creating/updating an archive.

Args:
    dictionary_size: the dictionary size desired.)pydoc"))
        .def("set_word_size",
             &bit7z::BitAbstractArchiveCreator::setWordSize,
             py::arg("word_size"),
             py::doc(R"pydoc(Sets the word size to be used when creating/updating an archive.

Args:
    word_size: the word size desired.)pydoc"))
        .def("set_solid_mode",
             &bit7z::BitAbstractArchiveCreator::setSolidMode,
             py::arg("solid_mode"),
             py::doc(R"pydoc(Sets whether the archive creator uses solid compression or not.

Args:
    solid_mode: the solid mode desired.
Note:
    Setting the solid compression mode to true has effect only when using the 7z format with multiple input files.)pydoc"))
        .def("set_update_mode",
             static_cast<void (bit7z::BitAbstractArchiveCreator::*)(bit7z::UpdateMode)>(
                 &bit7z::BitAbstractArchiveCreator::setUpdateMode),
             py::arg("mode"),
             py::doc(R"pydoc(Sets whether and how the creator can update existing archives or not.

Args:
    mode: the desired update mode.

Note:
    If set to UpdateMode::None, a subsequent compression operation may throw an exception if it targets an existing archive.)pydoc"))
        .def("set_volume_size",
             &bit7z::BitAbstractArchiveCreator::setVolumeSize,
             py::arg("volume_size"),
             py::doc(R"pydoc(Sets the volumeSize (in bytes) of the output archive volumes.

Args:
    volume_size: The dimension of a volume.

Note:
    This setting has effects only when the destination archive is on the filesystem.
)pydoc"))
        .def("set_threads_count",
             &bit7z::BitAbstractArchiveCreator::setThreadsCount,
             py::arg("threads_count"),
             py::doc(R"pydoc(Sets the number of threads to be used when creating/updating an archive.

Args:
    threads_count: the number of threads desired.
)pydoc"))
        .def("set_store_symbolic_links",
             &bit7z::BitAbstractArchiveCreator::setStoreSymbolicLinks,
             py::arg("store_symbolic_links"),
             py::doc(R"pydoc(Sets whether the creator will store symbolic links as links in the output archive.

Args:
    store_symbolic_links: if true, symbolic links will be stored as links.
)pydoc"));

    // bit7z::BitInputArchive
    py::class_<bit7z::BitInputArchive>(m, "BitInputArchive")
        .def("detected_format",
             &bit7z::BitInputArchive::detectedFormat,
             py::doc(R"pydoc(the detected format of the file.)pydoc"))
        .def("archive_property",
             &bit7z::BitInputArchive::archiveProperty,
             py::doc(R"pydoc(Gets the specified archive property.

Args:
    property: the property to be retrieved.

Returns:
    the current value of the archive property or an empty BitPropVariant if no value is specified.)pydoc"))
        .def("item_property",
             &bit7z::BitInputArchive::itemProperty,
             py::arg("index"),
             py::arg("property"),
             py::doc(R"pydoc(Gets the specified item property.

Args:
    index: the index of the item to retrieve the property from.
    property: the property to be retrieved.

Returns:
    the current value of the item property or an empty BitPropVariant if no value is specified.)pydoc"))
        .def("items_count",
             &bit7z::BitInputArchive::itemsCount,
             py::doc(R"pydoc(the number of items in the archive.)pydoc"))
        .def("is_item_folder",
             &bit7z::BitInputArchive::isItemFolder,
             py::arg("index"),
             py::doc(R"pydoc(Whether the item at the given index is a folder.
Args:
    index: the index of an item in the archive.

Returns:
    true if and only if the item at the given index is a folder.)pydoc"))
        .def("is_item_encrypted",
             &bit7z::BitInputArchive::isItemEncrypted,
             py::arg("index"),
             py::doc(R"pydoc(Whether the item at the given index is encrypted.

Args:
    index: the index of an item in the archive.

Returns:
    true if and only if the item at the given index is encrypted.)pydoc"))
        .def("archive_path",
             &bit7z::BitInputArchive::archivePath,
             py::doc(R"pydoc(the path to the archive (the empty string for buffer/stream archives).)pydoc"))
        .def("extract_to",
             static_cast<void (bit7z::BitInputArchive::*)(const std::string &) const>(
                 &bit7z::BitInputArchive::extractTo),
             py::arg("path"),
             py::doc(R"pydoc(Extracts the archive to the chosen directory.

Args:
    outDir: the output directory where the extracted files will be put.)pydoc"))
        .def("extract_to",
             static_cast<void (bit7z::BitInputArchive::*)(const std::string &, const std::vector<uint32_t> &) const>(
                 &bit7z::BitInputArchive::extractTo),
             py::arg("out_dir"),
             py::arg("indices"),
             py::doc(R"pydoc(Extracts the specified items to the chosen directory.

Args:
    out_dir: the output directory where the extracted files will be put.
    indices: the array of indices of the files in the archive that must be extracted.)pydoc"))
        .def(
            "extract_to",
            [](bit7z::BitInputArchive &self, uint32_t index) -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                self.extractTo(out_buffer, index);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("index"),
            py::doc(R"pydoc(Extracts a file to the output buffer.

Args:
    index: the index of the file to be extracted.)pydoc"))
        .def(
            "extract_to",
            [](bit7z::BitInputArchive &self) -> std::map<std::string, py::bytes> {
                std::map<std::string, std::vector<bit7z::byte_t>> out_buffer;
                self.extractTo(out_buffer);
                std::map<std::string, py::bytes> result;
                for (auto const &item : out_buffer) {
                    result[item.first] =
                        py::bytes(reinterpret_cast<const char *>(item.second.data()), item.second.size());
                }
                return result;
            },
            py::doc(
                R"pydoc(Extracts the content of the archive to a map of memory buffers, where the keys are the paths of the files (inside the archive), and the values are their decompressed contents.)pydoc"))
        .def("test", &bit7z::BitInputArchive::test, py::doc(R"pydoc(Tests the archive without extracting its content.

If the archive is not valid, a BitException is thrown!)pydoc"))
        .def("test_item",
             &bit7z::BitInputArchive::testItem,
             py::arg("index"),
             py::doc(R"pydoc(Tests the item at the given index inside the archive without extracting it.

If the archive is not valid, or there's no item at the given index, a BitException is thrown!)pydoc"))
        .def("contains",
             &bit7z::BitInputArchive::contains,
             py::arg("path"),
             py::doc(R"pydoc(Find if there is an item in the archive that has the given path.

Args:
    path: the path of the file or folder to be checked.

Returns:
    true if and only if the archive contains the specified file or folder.)pydoc"))
        .def("item_at",
             &bit7z::BitInputArchive::itemAt,
             py::arg("index"),
             py::doc(R"pydoc(Retrieve the item at the given index.

Args:
    index: the index of the item to be retrieved.

Returns:
    the item at the given index within the archive.)pydoc"));

    // FilterPolicy enum bindings
    py::enum_<bit7z::FilterPolicy>(m, "FilterPolicy")
        .value("Include",
               bit7z::FilterPolicy::Include,
               R"pydoc(Extract/compress the items that match the pattern.)pydoc")
        .value("Exclude",
               bit7z::FilterPolicy::Exclude,
               R"pydoc(Do not extract/compress the items that match the pattern.)pydoc")
        .export_values();

    // bit7z::BitOutputArchive
    py::class_<bit7z::BitOutputArchive>(m, "BitOutputArchive")
        .def("add_items",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::vector<std::string> &)>(
                 &bit7z::BitOutputArchive::addItems),
             py::arg("paths"),
             py::doc(R"pydoc(Adds all the items that can be found by indexing the given vector of filesystem paths.

Args:
    paths: the paths to be added to the archive.
)pydoc"))
        .def(
            "add_items",
            static_cast<void (bit7z::BitOutputArchive::*)(const std::map<std::string, std::string> &)>(
                &bit7z::BitOutputArchive::addItems),
            py::arg("files"),
            py::doc(
                R"pydoc(Adds all the items that can be found by indexing the keys of the given map of filesystem paths; the corresponding mapped values are the user-defined paths wanted inside the output archive.

Args:
    files: the map of file paths and their contents to be added to the archive.
)pydoc"))
        .def("add_file",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::string &, const std::string &)>(
                 &bit7z::BitOutputArchive::addFile),
             py::arg("in_file"),
             py::arg("name"),
             py::doc(
                 R"pydoc(Adds the given file path, with an optional user-defined path to be used in the output archive.

Args:
    in_file:  the path to the filesystem file to be added to the output archive.
    name: (optional) user-defined path to be used inside the output archive.
Note:
    If a directory path is given, a BitException is thrown.
)pydoc"))
        .def(
            "add_file",
            [](bit7z::BitOutputArchive &self, py::bytes input, const std::string &path) {
                auto input_str = input.cast<std::string>();
                std::vector<bit7z::byte_t> input_bytes(input_str.begin(), input_str.end());
                self.addFile(input_bytes, path);
            },
            py::arg("input"),
            py::arg("name"),
            py::doc(
                R"pydoc(Adds the given memory buffer, with an optional user-defined path to be used in the output archive.

Args:
    input: the memory buffer to be added to the output archive.
    name: user-defined path to be used inside the output archive.)pydoc"))
        .def("add_files",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::vector<std::string> &)>(
                 &bit7z::BitOutputArchive::addFiles),
             py::arg("in_files"),
             py::doc(R"pydoc(Adds all the files in the given vector of filesystem paths.

Args:
    in_files: the paths to be added to the archive.
Note:
    Paths to directories are ignored.
)pydoc"))
        .def("add_files",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::string &, const std::string &, bool)>(
                 &bit7z::BitOutputArchive::addFiles),
             py::arg("in_dir"),
             py::arg("filter"),
             py::arg("recursive"),
             py::doc(R"pydoc(Adds all the files inside the given directory path that match the given wildcard filter.

Args:
    in_dir: the directory where to search for files to be added to the output archive.
    filter: (optional) the filter pattern to be used to select the files to be added.
    recursive: (optional) if true, the directory will be searched recursively.
Note:
    If a file path is given, a BitException is thrown.
)pydoc"))
        .def(
            "add_files",
            static_cast<void (
                bit7z::BitOutputArchive::*)(const std::string &, const std::string &, bit7z::FilterPolicy, bool)>(
                &bit7z::BitOutputArchive::addFiles),
            py::arg("in_dir"),
            py::arg("filter"),
            py::arg("recursive"),
            py::arg("policy"),
            py::doc(
                R"pydoc(Adds all the files inside the given directory path that match the given wildcard filter, with the specified filter policy.

Args:
    in_dir: the directory where to search for files to be added to the output archive.
    filter: (optional) the wildcard filter to be used for searching the files.
    recursive: (optional) recursively search the files in the given directory and all of its subdirectories.
    policy: (optional) the filtering policy to be applied to the matched items.
)pydoc"))
        .def("add_directory",
             &bit7z::BitOutputArchive::addDirectory,
             py::arg("in_dir"),
             py::doc(
                 R"pydoc(Adds the given directory path and all its content.
Args:
    in_dir: the path of the directory to be added to the archive.)pydoc"))
        .def("add_directory_contents",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::string &, const std::string &, bool)>(
                 &bit7z::BitOutputArchive::addDirectoryContents),
             py::arg("in_dir"),
             py::arg("filter"),
             py::arg("recursive"),
             py::doc(R"pydoc(Adds the contents of the given directory path.

This function iterates through the specified directory and adds its contents based on the provided wildcard filter. Optionally, the operation can be recursive, meaning it will include subdirectories and their contents.

Args:
    in_dir: the directory where to search for files to be added to the output archive.
    filter: the wildcard filter to be used for searching the files.
    recursive: recursively search the files in the given directory and all of its subdirectories.
)pydoc"))
        .def("add_directory_contents",
             static_cast<void (
                 bit7z::BitOutputArchive::*)(const std::string &, const std::string &, bit7z::FilterPolicy, bool)>(
                 &bit7z::BitOutputArchive::addDirectoryContents),
             py::arg("in_dir"),
             py::arg("filter"),
             py::arg("recursive"),
             py::arg("policy"),
             py::doc(
                 R"pydoc(Adds the contents of the given directory path.

This function iterates through the specified directory and adds its contents based on the provided wildcard filter and policy. Optionally, the operation can be recursive, meaning it will include subdirectories and their contents.

Args:
    in_dir: the directory where to search for files to be added to the output archive.
    filter: the wildcard filter to be used for searching the files.
    recursive: recursively search the files in the given directory and all of its subdirectories.
    policy: the filtering policy to be applied to the matched items.
)pydoc"))
        .def("compress_to",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::string &)>(&bit7z::BitOutputArchive::compressTo),
             py::arg("out_file"),
             py::doc(R"pydoc(Compresses all the items added to this object to the specified archive file path.

Args:
    out_file: the output archive file path.

Note:
    If this object was created by passing an input archive file path, and this latter is the same as the outFile path parameter, the file will be updated.
)pydoc"))
        .def(
            "compress_to",
            [](bit7z::BitOutputArchive &self) -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                self.compressTo(out_buffer);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::doc(R"pydoc(Compresses all the items added to this object to the specified buffer.)pydoc"))
        .def("items_count",
             &bit7z::BitOutputArchive::itemsCount,
             py::doc(R"pydoc(the number of items in the archive.)pydoc"));

    // bit7z::BitArchiveReader class bindings
    py::class_<bit7z::BitArchiveReader, bit7z::BitAbstractArchiveOpener, bit7z::BitInputArchive>(m, "BitArchiveReader")
        .def(py::init([](const std::string &in_archive,
                         const bit7z::BitInFormat &format,
                         const std::string &password = std::string()) {
                 return new bit7z::BitArchiveReader(_core::Bit7zipSingleton::getInstance(),
                                                    in_archive,
                                                    format,
                                                    password);
             }),
             py::arg("in_archive"),
             py::arg("format"),
             py::arg("password") = std::string(),
             py::doc(R"pydoc(Constructs a BitArchiveReader object, opening the input file archive.

Args:
    in_archive: the path to the archive to be read.
    format: the format of the input archive.
    password: the password needed for opening the input archive.)pydoc"))
        .def(
            py::init([](py::bytes in_archive,
                        const bit7z::BitInFormat &format,
                        const std::string &password = std::string()) {
                std::string in_archive_str = py::cast<std::string>(in_archive);
                std::vector<bit7z::byte_t> in_buffer(in_archive_str.begin(), in_archive_str.end());
                return new bit7z::BitArchiveReader(_core::Bit7zipSingleton::getInstance(), in_buffer, format, password);
            }),
            py::arg("in_archive"),
            py::arg("format"),
            py::arg("password") = std::string(),
            py::doc(R"pydoc(Constructs a BitArchiveReader object, opening the input memory buffer archive.

Args:
    in_archive: the input buffer containing the archive to be read.
    format: the format of the input archive.
    password: the password needed for opening the input archive.)pydoc"))
        .def("items",
             &bit7z::BitArchiveReader::items,
             py::doc(R"pydoc(the list of all the archive items as BitArchiveItem objects.)pydoc"))
        .def(
            "archive_properties",
            &bit7z::BitArchiveReader::archiveProperties,
            py::doc(
                R"pydoc(a map of all the available (i.e., non-empty) archive properties and their respective values.)pydoc"))
        .def("folders_count",
             &bit7z::BitArchiveReader::foldersCount,
             py::doc(R"pydoc(the number of folders in the archive.)pydoc"))
        .def("files_count",
             &bit7z::BitArchiveReader::filesCount,
             py::doc(R"pydoc(the number of files in the archive.)pydoc"))
        .def("size",
             &bit7z::BitArchiveReader::size,
             py::doc(R"pydoc(the total uncompressed size of the archive content.)pydoc"))
        .def("pack_size",
             &bit7z::BitArchiveReader::packSize,
             py::doc(R"pydoc(the total compressed size of the archive content.)pydoc"))
        .def("has_encrypted_items",
             &bit7z::BitArchiveReader::hasEncryptedItems,
             py::doc(R"pydoc(true if and only if the archive has at least one encrypted item.)pydoc"))
        .def("is_encrypted",
             static_cast<bool (bit7z::BitArchiveReader::*)() const>(&bit7z::BitArchiveReader::isEncrypted),
             py::doc(R"pydoc(true if and only if the archive has only encrypted items.)pydoc"))
        .def("volumes_count",
             &bit7z::BitArchiveReader::volumesCount,
             py::doc(R"pydoc(the number of volumes in the archive.)pydoc"))
        .def("is_multi_volume",
             &bit7z::BitArchiveReader::isMultiVolume,
             py::doc(R"pydoc(true if and only if the archive is composed by multiple volumes.)pydoc"))
        .def("is_solid",
             &bit7z::BitArchiveReader::isSolid,
             py::doc(R"pydoc(true if and only if the archive was created using solid compression.)pydoc"))
        .def_static(
            "is_header_encrypted",
            [](const std::string &in_archive, const bit7z::BitInFormat &format) -> bool {
                return bit7z::BitArchiveReader::isHeaderEncrypted(_core::Bit7zipSingleton::getInstance(),
                                                                  in_archive,
                                                                  format);
            },
            py::arg("in_archive"),
            py::arg("format"),
            py::doc(R"pydoc(Checks if the given archive is header-encrypted or not.)pydoc"))
        .def_static(
            "is_header_encrypted",
            [](py::bytes in_archive, const bit7z::BitInFormat &format) -> bool {
                std::string in_archive_str = py::cast<std::string>(in_archive);
                std::vector<bit7z::byte_t> in_buffer(in_archive_str.begin(), in_archive_str.end());
                return bit7z::BitArchiveReader::isHeaderEncrypted(_core::Bit7zipSingleton::getInstance(),
                                                                  in_buffer,
                                                                  format);
            },
            py::arg("in_archive"),
            py::arg("format"),
            py::doc(R"pydoc(Checks if the given memory buffer archive is header-encrypted or not.)pydoc"));

    // bit7z::BitArchiveWriter class bindings
    py::class_<bit7z::BitArchiveWriter, bit7z::BitAbstractArchiveCreator, bit7z::BitOutputArchive>(m,
                                                                                                   "BitArchiveWriter")
        .def(
            py::init([](const bit7z::BitInOutFormat &format) {
                return new bit7z::BitArchiveWriter(_core::Bit7zipSingleton::getInstance(), format);
            }),
            py::arg("format"),
            py::doc(
                R"pydoc(Constructs an empty BitArchiveWriter object that can write archives of the specified format.)pydoc"))
        .def(py::init([](const std::string &in_archive,
                         const bit7z::BitInOutFormat &format,
                         const std::string &password = std::string()) {
                 return new bit7z::BitArchiveWriter(_core::Bit7zipSingleton::getInstance(),
                                                    in_archive,
                                                    format,
                                                    password);
             }),
             py::arg("in_archive"),
             py::arg("format"),
             py::arg("password") = std::string(),
             py::doc(R"pydoc(Constructs a BitArchiveWriter object, reading the given archive file path.)pydoc"))
        .def(
            py::init([](py::bytes in_archive,
                        const bit7z::BitInOutFormat &format,
                        const std::string &password = std::string()) {
                std::string in_archive_str = py::cast<std::string>(in_archive);
                std::vector<bit7z::byte_t> in_buffer(in_archive_str.begin(), in_archive_str.end());
                return new bit7z::BitArchiveWriter(_core::Bit7zipSingleton::getInstance(), in_buffer, format, password);
            }),
            py::arg("in_archive"),
            py::arg("format"),
            py::arg("password") = std::string(),
            py::doc(R"pydoc(Constructs a BitArchiveWriter object, reading the given memory buffer archive.)pydoc"));

    // BitExtractor class bindings
    using BitStringExtractInput = const std::string &;
    using BitStringExtractor = bit7z::BitExtractor<BitStringExtractInput>;
    py::class_<BitStringExtractor, bit7z::BitAbstractArchiveOpener> bitStringExtractor(m, "BitStringExtractor");
    bitStringExtractor
        .def(py::init([](const bit7z::BitInFormat &format) {
                 return new BitStringExtractor(_core::Bit7zipSingleton::getInstance(), format);
             }),
             py::arg("format"),
             py::doc(R"pydoc(Constructs a BitStringExtractor object, opening the input archive.)pydoc"))
        .def("extract",
             static_cast<void (BitStringExtractor::*)(BitStringExtractInput, const std::string &) const>(
                 &BitStringExtractor::extract),
             py::arg("in_archive"),
             py::arg("out_dir"),
             py::doc(R"pydoc(Extracts the given archive to the chosen directory.)pydoc"))
        .def(
            "extract",
            [](BitStringExtractor &self, const std::string &input, uint32_t index) -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                self.extract(input, out_buffer, index);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("in_archive"),
            py::arg("index"),
            py::doc(R"pydoc(Extracts the specified item from the given archive to a memory buffer.)pydoc"))
        .def(
            "extract",
            [](BitStringExtractor &self, const std::string &input) -> std::map<std::string, py::bytes> {
                std::map<std::string, std::vector<bit7z::byte_t>> out_buffer;
                self.extract(input, out_buffer);
                std::map<std::string, py::bytes> result;
                for (const auto &item : out_buffer) {
                    result[item.first] =
                        py::bytes(reinterpret_cast<const char *>(item.second.data()), item.second.size());
                }
                return result;
            },
            py::arg("in_archive"),
            py::doc(R"pydoc(Extracts all the items from the given archive to a dictionary of memory buffers.)pydoc"))
        .def(
            "extract_matching",
            static_cast<void (BitStringExtractor::*)(BitStringExtractInput,
                                                     const std::string &,
                                                     const std::string &,
                                                     bit7z::FilterPolicy) const>(&BitStringExtractor::extractMatching),
            py::arg("in_archive"),
            py::arg("pattern"),
            py::arg("out_dir"),
            py::arg("filter_policy"),
            py::doc(
                R"pydoc(Extracts the files in the archive that match the given wildcard pattern to the chosen directory.)pydoc"))
        .def(
            "extract_matching",
            [](BitStringExtractor &self,
               const std::string &input,
               const std::string &pattern,
               bit7z::FilterPolicy filter_policy) -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                self.extractMatching(input, pattern, out_buffer, filter_policy);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("in_archive"),
            py::arg("pattern"),
            py::arg("filter_policy"),
            py::doc(
                R"pydoc(Extracts to the output buffer the first file in the archive matching the given wildcard pattern.)pydoc"))
        .def("extract_items",
             &BitStringExtractor::extractItems,
             py::arg("in_archive"),
             py::arg("indices"),
             py::arg("out_dir") = std::string())
        .def(
            "extract_matching_regex",
            static_cast<void (BitStringExtractor::*)(BitStringExtractInput,
                                                     const std::string &,
                                                     const std::string &,
                                                     bit7z::FilterPolicy) const>(
                &BitStringExtractor::extractMatchingRegex),
            py::arg("in_archive"),
            py::arg("regex"),
            py::arg("out_dir"),
            py::arg("filter_policy"),
            py::doc(
                R"pydoc(Extracts the files in the archive that match the given regex pattern to the chosen directory.)pydoc"))
        .def(
            "extract_matching_regex",
            [](BitStringExtractor &self,
               const std::string &input,
               const std::string &regex,
               bit7z::FilterPolicy filter_policy) -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                self.extractMatchingRegex(input, regex, out_buffer, filter_policy);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("in_archive"),
            py::arg("regex"),
            py::arg("filter_policy"),
            py::doc(
                R"pydoc(Extracts to the output buffer the first file in the archive matching the given regex pattern.)pydoc"))
        .def("test",
             &BitStringExtractor::test,
             py::arg("in_archive"),
             py::doc(R"pydoc(Tests the given archive without extracting its content.

If the archive is not valid, a BitException is thrown!

Args:
    in_archive: the input archive to be tested.)pydoc"));

    m.attr("BitFileExtractor") = bitStringExtractor;

    // bit7z::BitMemExtractor class bindings
    using BitMemExtractorInput = const std::vector<bit7z::byte_t> &;
    using BitMemExtractor = bit7z::BitExtractor<const std::vector<bit7z::byte_t> &>;
    py::class_<BitMemExtractor, bit7z::BitAbstractArchiveOpener>(m, "BitMemExtractor")
        .def(py::init([](const bit7z::BitInFormat &format) {
                 return new BitMemExtractor(_core::Bit7zipSingleton::getInstance(), format);
             }),
             py::arg("format"),
             py::doc(R"pydoc(Constructs a BitMemExtractor object, opening the input archive.)pydoc"))
        .def("extract",
             static_cast<void (BitMemExtractor::*)(BitMemExtractorInput, const std::string &) const>(
                 &BitMemExtractor::extract),
             py::arg("in_archive"),
             py::arg("out_dir") = std::string(),
             py::doc(R"pydoc(Extracts the given archive to the chosen directory.)pydoc"))
        .def(
            "extract",
            [](BitMemExtractor &self, py::bytes input, uint32_t index) -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                self.extract(in_buffer, out_buffer, index);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("in_archive"),
            py::arg("index"),
            py::doc(R"pydoc(Extracts the specified item from the given archive to a memory buffer.)pydoc"))
        .def(
            "extract",
            [](BitMemExtractor &self, py::bytes input) -> std::map<std::string, py::bytes> {
                std::map<std::string, std::vector<bit7z::byte_t>> out_buffer;
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                self.extract(in_buffer, out_buffer);
                std::map<std::string, py::bytes> result;
                for (const auto &item : out_buffer) {
                    result[item.first] =
                        py::bytes(reinterpret_cast<const char *>(item.second.data()), item.second.size());
                }
                return result;
            },
            py::arg("in_archive"),
            py::doc(R"pydoc(Extracts all the items from the given archive to a dictionary of memory buffers.)pydoc"))
        .def(
            "extract_matching",
            static_cast<void (
                BitMemExtractor::*)(BitMemExtractorInput, const std::string &, const std::string &, bit7z::FilterPolicy)
                            const>(&BitMemExtractor::extractMatching),
            py::arg("in_archive"),
            py::arg("pattern"),
            py::arg("out_dir"),
            py::arg("filter_policy"),
            py::doc(
                R"pydoc(Extracts the files in the archive that match the given wildcard pattern to the chosen directory.)pydoc"))
        .def(
            "extract_matching",
            [](BitMemExtractor &self, py::bytes input, py::bytes pattern, bit7z::FilterPolicy filter_policy)
                -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                std::string pattern_str = py::cast<std::string>(pattern);
                self.extractMatching(in_buffer, pattern_str, out_buffer, filter_policy);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("in_archive"),
            py::arg("pattern"),
            py::arg("filter_policy"),
            py::doc(
                R"pydoc(Extracts to the output buffer the first file in the archive matching the given wildcard pattern.)pydoc"))
        .def("extract_items",
             &BitMemExtractor::extractItems,
             py::arg("in_archive"),
             py::arg("indices"),
             py::arg("out_dir") = std::string(),
             py::doc(R"pydoc(Extracts the specified items from the given archive to the chosen directory.)pydoc"))
        .def(
            "extract_matching_regex",
            static_cast<void (
                BitMemExtractor::*)(BitMemExtractorInput, const std::string &, const std::string &, bit7z::FilterPolicy)
                            const>(&BitMemExtractor::extractMatchingRegex),
            py::arg("in_archive"),
            py::arg("regex"),
            py::arg("out_dir"),
            py::arg("filter_policy"),
            py::doc(
                R"pydoc(Extracts the files in the archive that match the given regex pattern to the chosen directory.)pydoc"))
        .def(
            "extract_matching_regex",
            [](BitMemExtractor &self, py::bytes input, py::bytes regex, bit7z::FilterPolicy filter_policy)
                -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                std::string regex_str = py::cast<std::string>(regex);
                self.extractMatchingRegex(in_buffer, regex_str, out_buffer, filter_policy);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("in_archive"),
            py::arg("regex"),
            py::arg("filter_policy"),
            py::doc(
                R"pydoc(Extracts to the output buffer the first file in the archive matching the given regex pattern.)pydoc"))
        .def("test",
             &BitMemExtractor::test,
             py::arg("in_archive"),
             py::doc(R"pydoc(Tests the given archive without extracting its content.

If the archive is not valid, a BitException is thrown!

Args:
    in_archive: the input archive to be tested.)pydoc"));

    // BitCompressor class bindings
    using BitStringCompressInput = const std::string &;
    using BitStringCompressor = bit7z::BitCompressor<BitStringCompressInput>;
    py::class_<BitStringCompressor, bit7z::BitAbstractArchiveCreator>(m, "BitStringCompressor", py::is_final())
        .def(py::init([](const bit7z::BitInOutFormat &format) {
                 return new BitStringCompressor(_core::Bit7zipSingleton::getInstance(), format);
             }),
             py::arg("format"),
             py::doc(R"pydoc(Constructs a BitStringCompressor object, creating a new archive.)pydoc"))
        .def("compress_file",
             static_cast<void (BitStringCompressor::*)(BitStringCompressInput, const std::string &, const std::string &)
                             const>(&BitStringCompressor::compressFile),
             py::arg("in_file"),
             py::arg("out_file"),
             py::arg("input_name") = std::string(),
             py::doc(R"pydoc(Compresses the given file to the chosen archive.

Args:
    in_file: the input file to be compressed.
    out_file: the path (relative or absolute) to the output archive file.
    input_name: the name of the input file in the archive (optional).)pydoc"))
        .def(
            "compress_file",
            [](BitStringCompressor &self, const std::string &in_file, const std::string &input_name) -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                self.compressFile(in_file, out_buffer, input_name);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("in_file"),
            py::arg("input_name") = std::string(),
            py::doc(R"pydoc(Compresses the given file to a memory buffer.

Args:
    in_file: the input file to be compressed.
    input_name: the name of the input file in the archive (optional).)pydoc"));

    py::class_<bit7z::BitFileCompressor, BitStringCompressor>(m, "BitFileCompressor", py::is_final())
        .def(py::init([](const bit7z::BitInOutFormat &format) {
                 return new bit7z::BitFileCompressor(_core::Bit7zipSingleton::getInstance(), format);
             }),
             py::arg("format"),
             py::doc(R"pydoc(Constructs a BitFileCompressor object, creating a new archive.)pydoc"))
        .def("compress",
             static_cast<void (bit7z::BitFileCompressor::*)(const std::vector<std::string> &, const std::string &)
                             const>(&bit7z::BitFileCompressor::compress),
             py::arg("in_files"),
             py::arg("out_archive"),
             py::doc(R"pydoc(Compresses the given files or directories.

The items in the first argument must be the relative or absolute paths to files or directories existing on the filesystem.

Args:
    in_files: the input files to be compressed.
    out_archive: the path (relative or absolute) to the output archive file.)pydoc"))
        .def("compress",
             static_cast<void (bit7z::BitFileCompressor::*)(const std::map<std::string, std::string> &,
                                                            const std::string &) const>(
                 &bit7z::BitFileCompressor::compress),
             py::arg("in_files"),
             py::arg("out_archive"),
             py::doc(R"pydoc(Compresses the given files or directories using the specified aliases.

The items in the first argument must be the relative or absolute paths to files or directories existing on the filesystem. Each pair in the map must follow the following format: {"path to file in the filesystem", "alias path in the archive"}.


Args:
    in_files: a map of paths and corresponding aliases.
    out_archive: the path (relative or absolute) to the output archive file.)pydoc"))
        .def("compress_files",
             static_cast<void (bit7z::BitFileCompressor::*)(const std::vector<std::string> &, const std::string &)
                             const>(&bit7z::BitFileCompressor::compressFiles),
             py::arg("in_files"),
             py::arg("out_archive"),
             py::doc(R"pydoc(Compresses a group of files.

Args:
    in_files: the input files to be compressed.
    out_archive: the path (relative or absolute) to the output archive file.
Note:
    Any path to a directory or to a not-existing file will be ignored!)pydoc"))
        .def("compress_files",
             static_cast<void (
                 bit7z::BitFileCompressor::*)(const std::string &, const std::string &, bool, const std::string &)
                             const>(&bit7z::BitFileCompressor::compressFiles),
             py::arg("in_dir"),
             py::arg("out_archive"),
             py::arg("recursive") = true,
             py::arg("filter_pattern") = std::string("*"),
             py::doc(R"pydoc(Compresses all the files in the given directory.

Args:
    in_dir: the path (relative or absolute) to the input directory.
    out_archive: the path (relative or absolute) to the output archive file.
    recursive: (optional) if true, it searches files inside the sub-folders of in_dir.
    filter_pattern: the wildcard pattern to filter the files to be compressed (optional).)pydoc"))
        .def("compress_directory",
             &bit7z::BitFileCompressor::compressDirectory,
             py::arg("in_dir"),
             py::arg("out_archive"),
             py::doc(R"pydoc(Compresses an entire directory.

Args:
    in_dir: the path (relative or absolute) to the input directory.
    out_archive: the path (relative or absolute) to the output archive file.
Note:
    This method is equivalent to compress_files with filter set to "".)pydoc"))
        .def("compress_directory_contents",
             &bit7z::BitFileCompressor::compressDirectoryContents,
             py::arg("in_dir"),
             py::arg("out_archive"),
             py::arg("recursive") = true,
             py::arg("filter_pattern") = std::string("*"),
             py::doc(R"pydoc(Compresses the contents of a directory.

Args:
    in_dir: the path (relative or absolute) to the input directory.
    out_archive: the path (relative or absolute) to the output archive file.
    recursive: (optional) if true, it searches files inside the sub-folders of in_dir.
    filter_pattern: the wildcard pattern to filter the files to be compressed (optional).
Note:
    Unlike compress_files, this method includes also the metadata of the sub-folders.)pydoc"));

    // bit7z::BitMemCompressor class bindings
    using BitMemCompressorInput = const std::vector<bit7z::byte_t> &;
    using BitMemCompressor = bit7z::BitCompressor<BitMemCompressorInput>;
    py::class_<BitMemCompressor, bit7z::BitAbstractArchiveCreator>(m, "BitMemCompressor")
        .def(py::init([](const bit7z::BitInOutFormat &format) {
                 return new BitMemCompressor(_core::Bit7zipSingleton::getInstance(), format);
             }),
             py::arg("format"),
             py::doc(R"pydoc(Constructs a BitMemCompressor object, creating a new archive.)pydoc"))
        .def(
            "compress_file",
            [](BitMemCompressor &self, py::bytes input, const std::string &out_file, const std::string &input_name) {
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                self.compressFile(in_buffer, out_file, input_name);
            },
            py::arg("input"),
            py::arg("out_file"),
            py::arg("input_name") = std::string(),
            py::doc(R"pydoc(Compresses the given memory buffer to the chosen archive.

Args:
    input: the input memory buffer to be compressed.
    out_file: the path (relative or absolute) to the output archive file.
    input_name: (optional) the name to give to the compressed file inside the output archive.)pydoc"))
        .def(
            "compress_file",
            [](BitMemCompressor &self, py::bytes input, const std::string &input_name) -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                self.compressFile(in_buffer, out_buffer, input_name);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("input"),
            py::arg("input_name") = std::string(),
            py::doc(R"pydoc(Compresses the given memory buffer to a memory buffer.

Args:
    input: the input memory buffer to be compressed.
    input_name: (optional) the name to give to the compressed file inside the output archive.)pydoc"));

    // bit7z::BitArchiveEditor class bindings
    py::class_<bit7z::BitArchiveEditor, bit7z::BitArchiveWriter>(m, "BitArchiveEditor")
        .def(py::init(
                 [](const std::string &in_archive, const bit7z::BitInOutFormat &format, const std::string &password) {
                     return new bit7z::BitArchiveEditor(_core::Bit7zipSingleton::getInstance(),
                                                        in_archive,
                                                        format,
                                                        password);
                 }),
             py::arg("in_archive"),
             py::arg("format"),
             py::arg("password") = std::string(),
             py::doc(R"pydoc(Constructs a BitArchiveEditor object, reading the given archive file path.)pydoc"))
        .def("set_update_mode",
             &bit7z::BitArchiveEditor::setUpdateMode,
             py::arg("update_mode"),
             py::doc(R"pydoc(Sets how the editor performs the update of the items in the archive.

Args:
    mode: the desired update mode (either UpdateMode::Append or UpdateMode::Overwrite).

Note:
    BitArchiveEditor doesn't support UpdateMode::Nothing.)pydoc"))
        .def("rename_item",
             static_cast<void (bit7z::BitArchiveEditor::*)(uint32_t, const std::string &)>(
                 &bit7z::BitArchiveEditor::renameItem),
             py::arg("index"),
             py::arg("new_path"),
             py::doc(R"pydoc(Requests to change the path of the item at the specified index with the given one.

Args:
    index: the index of the item to be renamed.
    new_path: the new path of the item.)pydoc"))
        .def("rename_item",
             static_cast<void (bit7z::BitArchiveEditor::*)(const std::string &, const std::string &)>(
                 &bit7z::BitArchiveEditor::renameItem),
             py::arg("old_path"),
             py::arg("new_path"),
             py::doc(R"pydoc(Requests to change the path of the item from oldPath to the newPath.

Args:
    old_path: the current path of the item to be renamed.
    new_path: the new path of the item.)pydoc"))
        .def(
            "update_item",
            static_cast<void (bit7z::BitArchiveEditor::*)(uint32_t, const std::string &)>(
                &bit7z::BitArchiveEditor::updateItem),
            py::arg("index"),
            py::arg("in_file"),
            py::doc(
                R"pydoc(Requests to update the content of the item at the specified index with the data from the given file.

Args:
    index: the index of the item to be updated.
    in_file: the path of the file to be used for the update.)pydoc"))
        .def(
            "update_item",
            [](bit7z::BitArchiveEditor &self, uint32_t index, py::bytes input) {
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                self.updateItem(index, in_buffer);
            },
            py::arg("index"),
            py::arg("in_buffer"),
            py::doc(
                R"pydoc(Requests to update the content of the item at the specified index with the data from the given buffer.

Args:
    index: the index of the item to be updated.
    in_buffer: the buffer containing the new data for the item.)pydoc"))
        .def(
            "update_item",
            static_cast<void (bit7z::BitArchiveEditor::*)(const std::string &, const std::string &)>(
                &bit7z::BitArchiveEditor::updateItem),
            py::arg("item_path"),
            py::arg("in_file"),
            py::doc(
                R"pydoc(Requests to update the content of the item at the specified path with the data from the given file.

Args:
    item_path: the path of the item to be updated.
    in_file: the path of the file to be used for the update.)pydoc"))
        .def(
            "update_item",
            [](bit7z::BitArchiveEditor &self, const std::string &item_path, py::bytes input) {
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                self.updateItem(item_path, in_buffer);
            },
            py::arg("item_path"),
            py::arg("in_buffer"),
            py::doc(
                R"pydoc(Requests to update the content of the item at the specified path with the data from the given buffer.

Args:
    item_path: the path of the item to be updated.
    in_buffer: the buffer containing the new data for the item.)pydoc"))
        .def("delete_item",
             static_cast<void (bit7z::BitArchiveEditor::*)(uint32_t, bit7z::DeletePolicy)>(
                 &bit7z::BitArchiveEditor::deleteItem),
             py::arg("index"),
             py::arg("policy"),
             py::doc(R"pydoc(Marks as deleted the item at the given index.

Args:
    index: the index of the item to be deleted.
    policy: the policy to be used when deleting items.

Exceptions:
    BitException if the index is invalid.

Note:
    By default, if the item is a folder, only its metadata is deleted, not the files within it. If instead the policy is set to DeletePolicy::RecurseDirs, then the items within the folder will also be deleted.)pydoc"))
        .def("delete_item",
             static_cast<void (bit7z::BitArchiveEditor::*)(const std::string &, bit7z::DeletePolicy)>(
                 &bit7z::BitArchiveEditor::deleteItem),
             py::arg("item_path"),
             py::arg("policy"),
             py::doc(R"pydoc(Marks as deleted the archive's item(s) with the specified path.

Args:
    item_path: the path (in the archive) of the item to be deleted.
    policy: the policy to be used when deleting items.

Exceptions:
    BitException if the specified path is empty or invalid, or if no matching item could be found.

Note:
    By default, if the marked item is a folder, only its metadata will be deleted, not the files within it. To delete the folder contents as well, set the policy to DeletePolicy::RecurseDirs.
    The specified path must not begin with a path separator.
    A path with a trailing separator will _only_ be considered if the policy is DeletePolicy::RecurseDirs, and will only match folders; with DeletePolicy::ItemOnly, no item will match a path with a trailing separator.
    Generally, archives may contain multiple items with the same paths. If this is the case, all matching items will be marked as deleted according to the specified policy.)pydoc"))
        .def(
            "apply_changes",
            &bit7z::BitArchiveEditor::applyChanges,
            py::doc(
                R"pydoc(Applies the requested changes (i.e., rename/update/delete operations) to the input archive.)pydoc"));
}
