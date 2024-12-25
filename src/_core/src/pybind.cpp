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
        Python bindings for bit7z library
        -----------------------
        .. currentmodule:: _core
    )pbdoc";

    m.def("version", []() { return _core::ProjectVersion(); }, R"pbdoc(
        The _core plugin version.
    )pbdoc");

    m.def(
        "set_lib7zip_path",
        [](const std::string &path) { _core::default_library_path() = path; },
        py::arg("lib7zip_path"),
        py::doc(R"pbdoc(Configure the path to the 7zip library.)pbdoc"));

    m.def(
        "set_large_page_mode",
        []() { const_cast<bit7z::Bit7zLibrary &>(_core::Bit7zipSingleton::getInstance()).setLargePageMode(); },
        py::doc(R"pbdoc(Enable large page mode for 7zip library. This can improve performance on some systems.)pbdoc"));

    // Exception handling
    py::register_exception<bit7z::BitException>(m, "BitException");

    // CompressionLevel enum bindings
    py::enum_<bit7z::BitCompressionLevel>(m, "BitCompressionLevel")
        .value("None_", bit7z::BitCompressionLevel::None)
        .value("Fastest", bit7z::BitCompressionLevel::Fastest)
        .value("Fast", bit7z::BitCompressionLevel::Fast)
        .value("Normal", bit7z::BitCompressionLevel::Normal)
        .value("Max", bit7z::BitCompressionLevel::Max)
        .value("Ultra", bit7z::BitCompressionLevel::Ultra)
        .export_values();

    // CompressionMethod enum bindings
    py::enum_<bit7z::BitCompressionMethod>(m, "BitCompressionMethod")
        .value("Copy", bit7z::BitCompressionMethod::Copy)
        .value("Deflate", bit7z::BitCompressionMethod::Deflate)
        .value("Deflate64", bit7z::BitCompressionMethod::Deflate64)
        .value("BZip2", bit7z::BitCompressionMethod::BZip2)
        .value("Lzma", bit7z::BitCompressionMethod::Lzma)
        .value("Lzma2", bit7z::BitCompressionMethod::Lzma2)
        .value("Ppmd", bit7z::BitCompressionMethod::Ppmd)
        .export_values();

    // FormatFeatures enum bindings
    py::enum_<bit7z::FormatFeatures>(m, "FormatFeatures")
        .value("MultipleFiles", bit7z::FormatFeatures::MultipleFiles)
        .value("SolidArchive", bit7z::FormatFeatures::SolidArchive)
        .value("CompressionLevel", bit7z::FormatFeatures::CompressionLevel)
        .value("Encryption", bit7z::FormatFeatures::Encryption)
        .value("HeaderEncryption", bit7z::FormatFeatures::HeaderEncryption)
        .value("MultipleMethods", bit7z::FormatFeatures::MultipleMethods);

    // bit7z:: DeletePolicy enum bindings
    py::enum_<bit7z::DeletePolicy>(m, "DeletePolicy")
        .value("ItemOnly", bit7z::DeletePolicy::ItemOnly)
        .value("RecurseDirs", bit7z::DeletePolicy::RecurseDirs)
        .export_values();

    // bit7z::BitInFormat class bindings
    py::class_<bit7z::BitInFormat>(m, "BitInFormat")
        .def("value", &bit7z::BitInFormat::value)
        .def("__eq__", &bit7z::BitInFormat::operator==)
        .def("__ne__", &bit7z::BitInFormat::operator!=);

    // bit7z::BitInOutFormat class bindings
    py::class_<bit7z::BitInOutFormat, bit7z::BitInFormat>(m, "BitInOutFormat")
        .def("extension", &bit7z::BitInOutFormat::extension)
        .def("features", &bit7z::BitInOutFormat::features)
        .def("has_feature", &bit7z::BitInOutFormat::hasFeature)
        .def("default_method", &bit7z::BitInOutFormat::defaultMethod);

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
    py::enum_<bit7z::BitProperty>(m, "BitProperty")
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

    // bit7z::

    py::enum_<bit7z::BitPropVariantType>(m, "BitPropVariantType")
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

    py::class_<bit7z::BitPropVariant>(m, "BitPropVariant")
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
        .def("type", &bit7z::BitPropVariant::type)
        .def("clear", &bit7z::BitPropVariant::clear);

    // bit7z::BitGenericItem class bindings
    py::class_<bit7z::BitGenericItem>(m, "BitGenericItem")
        .def("is_dir", &bit7z::BitGenericItem::isDir)
        .def("size", &bit7z::BitGenericItem::size)
        .def("name", &bit7z::BitGenericItem::name)
        .def("path", &bit7z::BitGenericItem::path)
        .def("attributes", &bit7z::BitGenericItem::attributes);

    // bit7z::BitArchiveItem class bindings
    py::class_<bit7z::BitArchiveItem, bit7z::BitGenericItem>(m, "BitArchiveItem")
        .def("index", &bit7z::BitArchiveItem::index)
        .def("extension", &bit7z::BitArchiveItem::extension)
        .def("native_path", &bit7z::BitArchiveItem::nativePath)
        .def("creation_time", &bit7z::BitArchiveItem::creationTime)
        .def("last_access_time", &bit7z::BitArchiveItem::lastAccessTime)
        .def("last_write_time", &bit7z::BitArchiveItem::lastWriteTime)
        .def("attributes", &bit7z::BitArchiveItem::attributes)
        .def("pack_size", &bit7z::BitArchiveItem::packSize)
        .def("crc", &bit7z::BitArchiveItem::crc)
        .def("is_encrypted", &bit7z::BitArchiveItem::isEncrypted);

    // bit7z::BitArchiveItemOffset class bindings
    py::class_<bit7z::BitArchiveItemOffset, bit7z::BitArchiveItem>(m, "BitArchiveItemOffset")
        .def("__eq__", &bit7z::BitArchiveItemOffset::operator==)
        .def("__ne__", &bit7z::BitArchiveItemOffset::operator!=)
        .def("__iadd__", [](bit7z::BitArchiveItemOffset &self, int val) { return self.operator++(val); })
        .def("item_property", &bit7z::BitArchiveItemOffset::itemProperty);

    // bit7z::BitArchiveItemInfo class bindings
    py::class_<bit7z::BitArchiveItemInfo, bit7z::BitArchiveItem>(m, "BitArchiveItemInfo")
        .def("item_property", &bit7z::BitArchiveItemInfo::itemProperty)
        .def("item_properties", &bit7z::BitArchiveItemInfo::itemProperties);

    py::enum_<bit7z::OverwriteMode>(m, "OverwriteMode")
        .value("None_", bit7z::OverwriteMode::None)
        .value("Overwrite", bit7z::OverwriteMode::Overwrite)
        .value("Skip", bit7z::OverwriteMode::Skip)
        .export_values();

    // bit7z:: BitAbstractArchiveHandler class bindings
    py::class_<bit7z::BitAbstractArchiveHandler>(m, "BitAbstractArchiveHandler")
        .def("format", &bit7z::BitAbstractArchiveHandler::format)
        .def("password", &bit7z::BitAbstractArchiveHandler::password)
        .def("retainDirectories", &bit7z::BitAbstractArchiveHandler::retainDirectories)
        .def("is_password_defined", &bit7z::BitAbstractArchiveHandler::isPasswordDefined)
        .def("total_callback", &bit7z::BitAbstractArchiveHandler::totalCallback)
        .def("progress_callback", &bit7z::BitAbstractArchiveHandler::progressCallback)
        .def("ratio_callback", &bit7z::BitAbstractArchiveHandler::ratioCallback)
        .def("file_callback", &bit7z::BitAbstractArchiveHandler::fileCallback)
        .def("password_callback", &bit7z::BitAbstractArchiveHandler::passwordCallback)
        .def("overwrite_mode", &bit7z::BitAbstractArchiveHandler::overwriteMode)
        .def("set_password", &bit7z::BitAbstractArchiveHandler::setPassword, py::arg("password"))
        .def("clear_password", &bit7z::BitAbstractArchiveHandler::clearPassword)
        .def("set_retain_directories", &bit7z::BitAbstractArchiveHandler::setRetainDirectories)
        .def("set_total_callback", &bit7z::BitAbstractArchiveHandler::setTotalCallback)
        .def("set_progress_callback", &bit7z::BitAbstractArchiveHandler::setProgressCallback)
        .def("set_ratio_callback", &bit7z::BitAbstractArchiveHandler::setRatioCallback)
        .def("set_file_callback", &bit7z::BitAbstractArchiveHandler::setFileCallback)
        .def("set_password_callback", &bit7z::BitAbstractArchiveHandler::setPasswordCallback, py::arg("callback"))
        .def("set_overwrite_mode", &bit7z::BitAbstractArchiveHandler::setOverwriteMode, py::arg("mode"));

    // bit7z::BitAbstractArchiveOpener class bindings
    py::class_<bit7z::BitAbstractArchiveOpener, bit7z::BitAbstractArchiveHandler>(m, "BitAbstractArchiveOpener")
        .def("extraction_format", &bit7z::BitAbstractArchiveOpener::extractionFormat);

    // bit7z::UpdateMode enum bindings
    py::enum_<bit7z::UpdateMode>(m, "UpdateMode")
        .value("None_", bit7z::UpdateMode::None)
        .value("Append", bit7z::UpdateMode::Append)
        .value("Update", bit7z::UpdateMode::Update);

    // bit7z::BitAbstractArchiveCreator class bindings
    py::class_<bit7z::BitAbstractArchiveCreator, bit7z::BitAbstractArchiveHandler>(m, "BitAbstractArchiveCreator")
        .def("compression_format", &bit7z::BitAbstractArchiveCreator::compressionFormat)
        .def("crypt_headers", &bit7z::BitAbstractArchiveCreator::cryptHeaders)
        .def("compression_method", &bit7z::BitAbstractArchiveCreator::compressionMethod)
        .def("dictionary_size", &bit7z::BitAbstractArchiveCreator::dictionarySize)
        .def("word_size", &bit7z::BitAbstractArchiveCreator::wordSize)
        .def("solid_mode", &bit7z::BitAbstractArchiveCreator::solidMode)
        .def("update_mode", &bit7z::BitAbstractArchiveCreator::updateMode)
        .def("volume_size", &bit7z::BitAbstractArchiveCreator::volumeSize)
        .def("threads_count", &bit7z::BitAbstractArchiveCreator::threadsCount)
        .def("store_symbolic_links", &bit7z::BitAbstractArchiveCreator::storeSymbolicLinks)
        .def("set_password",
             static_cast<void (bit7z::BitAbstractArchiveCreator::*)(const std::string &)>(
                 &bit7z::BitAbstractArchiveCreator::setPassword),
             py::arg("password"))
        .def("set_password",
             static_cast<void (bit7z::BitAbstractArchiveCreator::*)(const std::string &, bool)>(
                 &bit7z::BitAbstractArchiveCreator::setPassword),
             py::arg("password"),
             py::arg("crypt_headers"))
        .def("set_compression_level", &bit7z::BitAbstractArchiveCreator::setCompressionLevel)
        .def("set_compression_method", &bit7z::BitAbstractArchiveCreator::setCompressionMethod)
        .def("set_dictionary_size", &bit7z::BitAbstractArchiveCreator::setDictionarySize)
        .def("set_word_size", &bit7z::BitAbstractArchiveCreator::setWordSize)
        .def("set_solid_mode", &bit7z::BitAbstractArchiveCreator::setSolidMode)
        .def("set_update_mode",
             static_cast<void (bit7z::BitAbstractArchiveCreator::*)(bit7z::UpdateMode)>(
                 &bit7z::BitAbstractArchiveCreator::setUpdateMode))
        .def("set_volume_size", &bit7z::BitAbstractArchiveCreator::setVolumeSize)
        .def("set_threads_count", &bit7z::BitAbstractArchiveCreator::setThreadsCount)
        .def("set_store_symbolic_links", &bit7z::BitAbstractArchiveCreator::setStoreSymbolicLinks);

    // bit7z::BitInputArchive
    py::class_<bit7z::BitInputArchive>(m, "BitInputArchive")
        .def("detected_format", &bit7z::BitInputArchive::detectedFormat)
        .def("archive_property", &bit7z::BitInputArchive::archiveProperty)
        .def("item_property", &bit7z::BitInputArchive::itemProperty)
        .def("items_count", &bit7z::BitInputArchive::itemsCount)
        .def("is_item_folder", &bit7z::BitInputArchive::isItemFolder)
        .def("is_item_encrypted", &bit7z::BitInputArchive::isItemEncrypted)
        .def("archive_path", &bit7z::BitInputArchive::archivePath)
        .def("extract_to",
             static_cast<void (bit7z::BitInputArchive::*)(const std::string &) const>(
                 &bit7z::BitInputArchive::extractTo))
        .def("extract_to",
             static_cast<void (bit7z::BitInputArchive::*)(const std::string &, const std::vector<uint32_t> &) const>(
                 &bit7z::BitInputArchive::extractTo),
             py::arg("path"),
             py::arg("indices"),
             py::doc(R"pydoc(Extracts the items at the specified indices to the specified path)pydoc"))
        .def(
            "extract_to",
            [](bit7z::BitInputArchive &self, uint32_t index) -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                self.extractTo(out_buffer, index);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("index"),
            py::doc(R"pydoc(Extracts the item at the specified index to a byte array)pydoc"))
        .def(
            "extract_to",
            [](bit7z::BitInputArchive &self) -> py::dict {
                std::map<std::string, std::vector<bit7z::byte_t>> out_buffer;
                self.extractTo(out_buffer);
                py::dict result;
                for (auto const &item : out_buffer) {
                    result[item.first.c_str()] =
                        py::bytes(reinterpret_cast<const char *>(item.second.data()), item.second.size());
                }
                return result;
            },
            py::doc(R"pydoc(Extracts all items to a dictionary of byte arrays)pydoc"))
        .def("test", &bit7z::BitInputArchive::test)
        .def("test_item", &bit7z::BitInputArchive::testItem, py::arg("index"))
        .def("contains", &bit7z::BitInputArchive::contains, py::arg("path"))
        .def("item_at", &bit7z::BitInputArchive::itemAt, py::arg("index"));

    // FilterPolicy enum bindings
    py::enum_<bit7z::FilterPolicy>(m, "FilterPolicy")
        .value("Include", bit7z::FilterPolicy::Include)
        .value("Exclude", bit7z::FilterPolicy::Exclude)
        .export_values();

    // bit7z::BitOutputArchive
    py::class_<bit7z::BitOutputArchive>(m, "BitOutputArchive")
        .def("add_items",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::vector<std::string> &)>(
                 &bit7z::BitOutputArchive::addItems))
        .def("add_items",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::map<std::string, std::string> &)>(
                 &bit7z::BitOutputArchive::addItems))
        .def("add_file",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::string &, const std::string &)>(
                 &bit7z::BitOutputArchive::addFile))
        .def("add_file",
             [](bit7z::BitOutputArchive &self, py::bytes input, const std::string &path) {
                 auto input_str = input.cast<std::string>();
                 std::vector<bit7z::byte_t> input_bytes(input_str.begin(), input_str.end());
                 self.addFile(input_bytes, path);
             })
        .def("add_files",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::vector<std::string> &)>(
                 &bit7z::BitOutputArchive::addFiles))
        .def("add_files",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::string &, const std::string &, bool)>(
                 &bit7z::BitOutputArchive::addFiles))
        .def("add_files",
             static_cast<void (
                 bit7z::BitOutputArchive::*)(const std::string &, const std::string &, bit7z::FilterPolicy, bool)>(
                 &bit7z::BitOutputArchive::addFiles))
        .def("add_directory", &bit7z::BitOutputArchive::addDirectory)
        .def("add_directory_contents",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::string &, const std::string &, bool)>(
                 &bit7z::BitOutputArchive::addDirectoryContents))
        .def("add_directory_contents",
             static_cast<void (
                 bit7z::BitOutputArchive::*)(const std::string &, const std::string &, bit7z::FilterPolicy, bool)>(
                 &bit7z::BitOutputArchive::addDirectoryContents))
        .def("compress_to",
             static_cast<void (bit7z::BitOutputArchive::*)(const std::string &)>(&bit7z::BitOutputArchive::compressTo))
        .def("compress_to",
             [](bit7z::BitOutputArchive &self) -> py::bytes {
                 std::vector<bit7z::byte_t> out_buffer;
                 self.compressTo(out_buffer);
                 return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
             })
        .def("items_count", &bit7z::BitOutputArchive::itemsCount);

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
             py::arg("password") = std::string())
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
            py::arg("password") = std::string())
        .def("items", &bit7z::BitArchiveReader::items)
        .def("archive_properties", &bit7z::BitArchiveReader::archiveProperties)
        .def("folders_count", &bit7z::BitArchiveReader::foldersCount)
        .def("files_count", &bit7z::BitArchiveReader::filesCount)
        .def("size", &bit7z::BitArchiveReader::size)
        .def("pack_size", &bit7z::BitArchiveReader::packSize)
        .def("has_encrypted_items", &bit7z::BitArchiveReader::hasEncryptedItems)
        .def("is_encrypted",
             static_cast<bool (bit7z::BitArchiveReader::*)() const>(&bit7z::BitArchiveReader::isEncrypted))
        .def("volumes_count", &bit7z::BitArchiveReader::volumesCount)
        .def("is_multi_volume", &bit7z::BitArchiveReader::isMultiVolume)
        .def("is_solid", &bit7z::BitArchiveReader::isSolid)
        .def_static(
            "is_header_encrypted",
            [](const std::string &in_archive, const bit7z::BitInFormat &format) -> bool {
                return bit7z::BitArchiveReader::isHeaderEncrypted(_core::Bit7zipSingleton::getInstance(),
                                                                  in_archive,
                                                                  format);
            },
            py::arg("in_archive"),
            py::arg("format"))
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
            py::arg("format"));

    // bit7z::BitArchiveWriter class bindings
    py::class_<bit7z::BitArchiveWriter, bit7z::BitAbstractArchiveCreator, bit7z::BitOutputArchive>(m,
                                                                                                   "BitArchiveWriter")
        .def(py::init([](const bit7z::BitInOutFormat &format) {
                 return new bit7z::BitArchiveWriter(_core::Bit7zipSingleton::getInstance(), format);
             }),
             py::arg("format"))
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
             py::arg("password") = std::string())
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
            py::arg("password") = std::string());

    // BitExtractor class bindings
    using BitStringExtractInput = const std::string &;
    using BitStringExtractor = bit7z::BitExtractor<BitStringExtractInput>;
    py::class_<BitStringExtractor, bit7z::BitAbstractArchiveOpener> bitStringExtractor(m, "BitStringExtractor");
    bitStringExtractor
        .def(py::init([](const bit7z::BitInFormat &format) {
                 return new BitStringExtractor(_core::Bit7zipSingleton::getInstance(), format);
             }),
             py::arg("format"))
        .def("extract",
             static_cast<void (BitStringExtractor::*)(BitStringExtractInput, const std::string &) const>(
                 &BitStringExtractor::extract),
             py::arg("in_archive"),
             py::arg("out_dir"))
        .def(
            "extract",
            [](BitStringExtractor &self, const std::string &input, uint32_t index) -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                self.extract(input, out_buffer, index);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("in_archive"),
            py::arg("index"))
        .def(
            "extract",
            [](BitStringExtractor &self, const std::string &input) -> py::dict {
                std::map<std::string, std::vector<bit7z::byte_t>> out_buffer;
                self.extract(input, out_buffer);
                py::dict result;
                for (const auto &item : out_buffer) {
                    result[item.first.c_str()] =
                        py::bytes(reinterpret_cast<const char *>(item.second.data()), item.second.size());
                }
                return result;
            },
            py::arg("in_archive"))
        .def("extract_matching",
             static_cast<void (BitStringExtractor::*)(BitStringExtractInput,
                                                      const std::string &,
                                                      const std::string &,
                                                      bit7z::FilterPolicy) const>(&BitStringExtractor::extractMatching),
             py::arg("in_archive"),
             py::arg("pattern"),
             py::arg("out_dir"),
             py::arg("filter_policy"))
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
            py::arg("filter_policy"))
        .def("extract_items",
             &BitStringExtractor::extractItems,
             py::arg("in_archive"),
             py::arg("indices"),
             py::arg("out_dir") = std::string())
        .def("extract_matching_regex",
             static_cast<void (BitStringExtractor::*)(BitStringExtractInput,
                                                      const std::string &,
                                                      const std::string &,
                                                      bit7z::FilterPolicy) const>(
                 &BitStringExtractor::extractMatchingRegex),
             py::arg("in_archive"),
             py::arg("regex"),
             py::arg("out_dir"),
             py::arg("filter_policy"))
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
            py::arg("filter_policy"))
        .def("test", &BitStringExtractor::test);

    m.attr("BitFileExtractor") = bitStringExtractor;

    // bit7z::BitMemExtractor class bindings
    using BitMemExtractorInput = const std::vector<bit7z::byte_t> &;
    using BitMemExtractor = bit7z::BitExtractor<const std::vector<bit7z::byte_t> &>;
    py::class_<BitMemExtractor, bit7z::BitAbstractArchiveOpener>(m, "BitMemExtractor")
        .def(py::init([](const bit7z::BitInFormat &format) {
                 return new BitMemExtractor(_core::Bit7zipSingleton::getInstance(), format);
             }),
             py::arg("format"))
        .def("extract",
             static_cast<void (BitMemExtractor::*)(BitMemExtractorInput, const std::string &) const>(
                 &BitMemExtractor::extract),
             py::arg("in_archive"),
             py::arg("out_dir") = std::string())
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
            py::arg("index"))
        .def(
            "extract",
            [](BitMemExtractor &self, py::bytes input) -> py::dict {
                std::map<std::string, std::vector<bit7z::byte_t>> out_buffer;
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                self.extract(in_buffer, out_buffer);
                py::dict result;
                for (const auto &item : out_buffer) {
                    result[item.first.c_str()] =
                        py::bytes(reinterpret_cast<const char *>(item.second.data()), item.second.size());
                }
                return result;
            },
            py::arg("in_archive"))
        .def(
            "extract_matching",
            static_cast<void (
                BitMemExtractor::*)(BitMemExtractorInput, const std::string &, const std::string &, bit7z::FilterPolicy)
                            const>(&BitMemExtractor::extractMatching),
            py::arg("in_archive"),
            py::arg("pattern"),
            py::arg("out_dir"),
            py::arg("filter_policy"))
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
            py::arg("filter_policy"))
        .def("extract_items",
             &BitMemExtractor::extractItems,
             py::arg("in_archive"),
             py::arg("indices"),
             py::arg("out_dir") = std::string())
        .def(
            "extract_matching_regex",
            static_cast<void (
                BitMemExtractor::*)(BitMemExtractorInput, const std::string &, const std::string &, bit7z::FilterPolicy)
                            const>(&BitMemExtractor::extractMatchingRegex),
            py::arg("in_archive"),
            py::arg("regex"),
            py::arg("out_dir"),
            py::arg("filter_policy"))
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
            py::arg("filter_policy"))
        .def("test", &BitMemExtractor::test);

    // BitCompressor class bindings
    using BitStringCompressInput = const std::string &;
    using BitStringCompressor = bit7z::BitCompressor<BitStringCompressInput>;
    py::class_<BitStringCompressor, bit7z::BitAbstractArchiveCreator>(m, "BitStringCompressor", py::is_final())
        .def(py::init([](const bit7z::BitInOutFormat &format) {
                 return new BitStringCompressor(_core::Bit7zipSingleton::getInstance(), format);
             }),
             py::arg("format"))
        .def("compress_file",
             static_cast<void (BitStringCompressor::*)(BitStringCompressInput, const std::string &, const std::string &)
                             const>(&BitStringCompressor::compressFile),
             py::arg("in_file"),
             py::arg("out_file"),
             py::arg("input_name") = std::string())
        .def(
            "compress_file",
            [](BitStringCompressor &self, const std::string &in_file, const std::string &input_name) -> py::bytes {
                std::vector<bit7z::byte_t> out_buffer;
                self.compressFile(in_file, out_buffer, input_name);
                return py::bytes(reinterpret_cast<const char *>(out_buffer.data()), out_buffer.size());
            },
            py::arg("in_file"),
            py::arg("input_name") = std::string());

    py::class_<bit7z::BitFileCompressor, BitStringCompressor>(m, "BitFileCompressor", py::is_final())
        .def(py::init([](const bit7z::BitInOutFormat &format) {
                 return new bit7z::BitFileCompressor(_core::Bit7zipSingleton::getInstance(), format);
             }),
             py::arg("format"))
        .def("compress",
             static_cast<void (bit7z::BitFileCompressor::*)(const std::vector<std::string> &, const std::string &)
                             const>(&bit7z::BitFileCompressor::compress),
             py::arg("in_files"),
             py::arg("out_archive"))
        .def("compress",
             static_cast<void (bit7z::BitFileCompressor::*)(const std::map<std::string, std::string> &,
                                                            const std::string &) const>(
                 &bit7z::BitFileCompressor::compress),
             py::arg("in_files"),
             py::arg("out_archive"))
        .def("compress_files",
             static_cast<void (bit7z::BitFileCompressor::*)(const std::vector<std::string> &, const std::string &)
                             const>(&bit7z::BitFileCompressor::compressFiles),
             py::arg("in_files"),
             py::arg("out_archive"))
        .def("compress_files",
             static_cast<void (
                 bit7z::BitFileCompressor::*)(const std::string &, const std::string &, bool, const std::string &)
                             const>(&bit7z::BitFileCompressor::compressFiles),
             py::arg("in_dir"),
             py::arg("out_archive"),
             py::arg("recursive") = true,
             py::arg("filter_pattern") = std::string("*"))
        .def("compress_directory",
             &bit7z::BitFileCompressor::compressDirectory,
             py::arg("in_dir"),
             py::arg("out_archive"))
        .def("compress_directory_contents",
             &bit7z::BitFileCompressor::compressDirectoryContents,
             py::arg("in_dir"),
             py::arg("out_archive"),
             py::arg("recursive") = true,
             py::arg("filter_pattern") = std::string("*"));

    // bit7z::BitMemCompressor class bindings
    using BitMemCompressorInput = const std::vector<bit7z::byte_t> &;
    using BitMemCompressor = bit7z::BitCompressor<BitMemCompressorInput>;
    py::class_<BitMemCompressor, bit7z::BitAbstractArchiveCreator>(m, "BitMemCompressor")
        .def(py::init([](const bit7z::BitInOutFormat &format) {
                 return new BitMemCompressor(_core::Bit7zipSingleton::getInstance(), format);
             }),
             py::arg("format"))
        .def(
            "compress_file",
            [](BitMemCompressor &self, py::bytes input, const std::string &out_file, const std::string &input_name) {
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                self.compressFile(in_buffer, out_file, input_name);
            },
            py::arg("input"),
            py::arg("out_file"),
            py::arg("input_name") = std::string())
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
            py::arg("input_name") = std::string());

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
             py::arg("password") = std::string())
        .def("set_update_mode", &bit7z::BitArchiveEditor::setUpdateMode, py::arg("update_mode"))
        .def("rename_item",
             static_cast<void (bit7z::BitArchiveEditor::*)(uint32_t, const std::string &)>(
                 &bit7z::BitArchiveEditor::renameItem),
             py::arg("index"),
             py::arg("new_path"))
        .def("rename_item",
             static_cast<void (bit7z::BitArchiveEditor::*)(const std::string &, const std::string &)>(
                 &bit7z::BitArchiveEditor::renameItem),
             py::arg("old_path"),
             py::arg("new_path"))
        .def("update_item",
             static_cast<void (bit7z::BitArchiveEditor::*)(uint32_t, const std::string &)>(
                 &bit7z::BitArchiveEditor::updateItem),
             py::arg("index"),
             py::arg("in_file"))
        .def(
            "update_item",
            [](bit7z::BitArchiveEditor &self, uint32_t index, py::bytes input) {
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                self.updateItem(index, in_buffer);
            },
            py::arg("index"),
            py::arg("in_buffer"))
        // .def("update_item",
        //      static_cast<void (bit7z::BitArchiveEditor::*)(uint32_t, std::istream&)>(
        //          &bit7z::BitArchiveEditor::updateItem),
        //      py::arg("index"),
        //      py::arg("new_data"))
        .def("update_item",
             static_cast<void (bit7z::BitArchiveEditor::*)(const std::string &, const std::string &)>(
                 &bit7z::BitArchiveEditor::updateItem),
             py::arg("item_path"),
             py::arg("in_file"))
        .def(
            "update_item",
            [](bit7z::BitArchiveEditor &self, const std::string &item_path, py::bytes input) {
                std::string input_str = py::cast<std::string>(input);
                std::vector<bit7z::byte_t> in_buffer(input_str.begin(), input_str.end());
                self.updateItem(item_path, in_buffer);
            },
            py::arg("item_path"),
            py::arg("in_buffer"))
        // .def("update_item",
        //      static_cast<void (bit7z::BitArchiveEditor::*)(const std::string&, std::istream&)>(
        //          &bit7z::BitArchiveEditor::updateItem),
        //      py::arg("item_path"),
        //      py::arg("new_data"))
        .def("delete_item",
             static_cast<void (bit7z::BitArchiveEditor::*)(uint32_t, bit7z::DeletePolicy)>(
                 &bit7z::BitArchiveEditor::deleteItem),
             py::arg("index"),
             py::arg("policy"))
        .def("delete_item",
             static_cast<void (bit7z::BitArchiveEditor::*)(const std::string &, bit7z::DeletePolicy)>(
                 &bit7z::BitArchiveEditor::deleteItem),
             py::arg("item_path"),
             py::arg("policy"))
        .def("apply_changes", &bit7z::BitArchiveEditor::applyChanges);
}
