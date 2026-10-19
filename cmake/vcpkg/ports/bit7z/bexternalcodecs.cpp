/*
 * bit7z - A C++ static library to interface with the 7-zip shared libraries.
 * Copyright (c) 2014-2023 Riccardo Ostani - All Rights Reserved.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

#include "bexternalcodecs.hpp"

#include "bit7zlibrary.hpp"
#include "bitexception.hpp"
#include "bitpropvariant.hpp"
#include "internal/fs.hpp"
#include "internal/stringutil.hpp"

#include <7zip/Archive/IArchive.h>
#include <7zip/ICoder.h>

#include <cstring>

extern "C" const GUID IID_ICompressCodecsInfo = {0x23170F69,
                                                 0x40C1,
                                                 0x278A,
                                                 {0x00, 0x00, 0x00, 0x04, 0x00, 0x60, 0x00, 0x00}};

namespace bit7z {

CExternalCodecsInfo::~CExternalCodecsInfo() = default;

bool CExternalCodecsInfo::loadPlugins(const tstring& codecsPath, const tstring& formatsPath) {
    m_pluginDlls.clear();
    m_formats.clear();
    m_inFormats.clear();
    m_inOutFormats.clear();
    m_totalMethods = 0;

    // Follow the official 7-Zip LoadCodecs.cpp order: Codecs first, Formats second.
    loadDllsFromFolder(codecsPath);
    loadDllsFromFolder(formatsPath);

    return m_totalMethods > 0 || !m_formats.empty();
}

bool CExternalCodecsInfo::loadDllsFromFolder(const tstring& folderPath) {
    fs::path dir(folderPath);
    if (!fs::exists(dir) || !fs::is_directory(dir)) {
        return false;
    }

    for (const auto& entry : fs::directory_iterator(dir)) {
        if (!entry.is_regular_file()) {
            continue;
        }
        const auto& ext = entry.path().extension();
        if (ext != ".dll" && ext != ".dylib" && ext != ".so") {
            continue;
        }

        CPluginDll plugin;
        try {
            plugin.library = std::make_unique<BitSharedLibrary>(entry.path().string());
        }
        catch (const BitException&) {
            continue;
        }

        // --- Codec exports ---
        try {
            plugin.getNumberOfMethods = plugin.library->getFunction<Func_GetNumberOfMethods>("GetNumberOfMethods");
            plugin.getMethodProperty = plugin.library->getFunction<Func_GetMethodProperty>("GetMethodProperty");
            plugin.createDecoder = plugin.library->getFunction<Func_CreateDecoder>("CreateDecoder");
            plugin.createEncoder = plugin.library->getFunction<Func_CreateEncoder>("CreateEncoder");
        }
        catch (const BitException&) {
            // Not a codec DLL; the codec pointers stay null.
        }

        UInt32 numMethods = 0;
        if (plugin.getNumberOfMethods != nullptr && plugin.getNumberOfMethods(&numMethods) == S_OK && numMethods > 0) {
            plugin.numMethods = numMethods;
            plugin.startIndex = m_totalMethods;
            m_totalMethods += numMethods;
        }

        // --- Format-handler exports ---
        try {
            plugin.createObject = plugin.library->getFunction<CreateObjectFunc>("CreateObject");
        }
        catch (const BitException&) {
            // Not a format-handler DLL.
        }

        // Skip DLLs that expose neither codecs nor formats.
        if (plugin.numMethods == 0 && plugin.createObject == nullptr) {
            continue;
        }

        plugin.path = entry.path().string();
        const std::size_t dllIndex = m_pluginDlls.size();
        m_pluginDlls.push_back(std::move(plugin));

        // --- Enumerate formats (if the DLL is a format handler) ---
        if (m_pluginDlls.back().createObject != nullptr) {
            Func_GetNumberOfFormats getNumFormats = nullptr;
            Func_GetHandlerProperty2 getHandlerProp = nullptr;
            try {
                getNumFormats = m_pluginDlls.back().library->getFunction<Func_GetNumberOfFormats>("GetNumberOfFormats");
                getHandlerProp =
                    m_pluginDlls.back().library->getFunction<Func_GetHandlerProperty2>("GetHandlerProperty2");
            }
            catch (const BitException&) {
                getNumFormats = nullptr;
                getHandlerProp = nullptr;
            }

            UInt32 numFormats = 0;
            if (getNumFormats != nullptr && getNumFormats(&numFormats) == S_OK && numFormats > 0) {
                for (UInt32 i = 0; i < numFormats; ++i) {
                    CExternalFormatInfo info;
                    info.dllIndex = dllIndex;

                    BitPropVariant prop;
                    if (getHandlerProp(i, NArchive::NHandlerPropID::kClassID, &prop) == S_OK && prop.vt == VT_BSTR
                        && prop.bstrVal != nullptr) {
                        if (::SysStringByteLen(prop.bstrVal) == sizeof(GUID)) {
                            std::memcpy(&info.classID, prop.bstrVal, sizeof(GUID));
                        }
                    }
                    prop = BitPropVariant{};
                    if (getHandlerProp(i, NArchive::NHandlerPropID::kName, &prop) == S_OK && prop.vt == VT_BSTR) {
                        info.name = prop.getString();
                    }
                    prop = BitPropVariant{};
                    if (getHandlerProp(i, NArchive::NHandlerPropID::kExtension, &prop) == S_OK && prop.vt == VT_BSTR) {
                        info.extension = prop.getString();
                    }
                    prop = BitPropVariant{};
                    if (getHandlerProp(i, NArchive::NHandlerPropID::kAddExtension, &prop) == S_OK
                        && prop.vt == VT_BSTR) {
                        info.addExtension = prop.getString();
                    }
                    prop = BitPropVariant{};
                    if (getHandlerProp(i, NArchive::NHandlerPropID::kUpdate, &prop) == S_OK && prop.vt == VT_BOOL) {
                        info.update = prop.getBool();
                    }
                    prop = BitPropVariant{};
                    if (getHandlerProp(i, NArchive::NHandlerPropID::kSignature, &prop) == S_OK && prop.vt == VT_BSTR
                        && prop.bstrVal != nullptr) {
                        const auto byteLen = ::SysStringByteLen(prop.bstrVal);
                        if (byteLen > 0) {
                            info.signature.assign(reinterpret_cast<const char*>(prop.bstrVal), byteLen);
                        }
                    }
                    prop = BitPropVariant{};
                    if (getHandlerProp(i, NArchive::NHandlerPropID::kSignatureOffset, &prop) == S_OK
                        && prop.vt == VT_UI4) {
                        info.signatureOffset = prop.getUInt32();
                    }
                    prop = BitPropVariant{};
                    if (getHandlerProp(i, NArchive::NHandlerPropID::kFlags, &prop) == S_OK && prop.vt == VT_UI4) {
                        info.flags = prop.getUInt32();
                    }

                    m_formats.push_back(std::move(info));

                    const auto& added = m_formats.back();
                    const unsigned char fmtValue = added.classID.Data4[5];
                    if (added.update) {
                        std::string ext = added.extension;
                        const auto space = ext.find_first_of(" \t");
                        if (space != std::string::npos) {
                            ext = ext.substr(0, space);
                        }
                        if (!ext.empty() && ext.front() != '.') {
                            ext = "." + ext;
                        }

                        auto& entry = m_inOutFormats.emplace_back();
                        entry.name = added.name;
                        entry.extension = tstring(ext.begin(), ext.end());
                        entry.format = std::make_unique<BitInOutFormat>(fmtValue,
                                                                        entry.extension.c_str(),
                                                                        BitCompressionMethod::Copy,
                                                                        FormatFeatures::CompressionLevel);
                    }
                    else {
                        auto& entry = m_inFormats.emplace_back();
                        entry.name = added.name;
                        entry.format = std::make_unique<BitInFormat>(fmtValue);
                    }
                }
            }
        }
    }

    return true;
}

std::vector<std::string> CExternalCodecsInfo::getCodecPaths() const {
    std::vector<std::string> paths;
    paths.reserve(m_pluginDlls.size());
    for (const auto& dll : m_pluginDlls) {
        paths.push_back(dll.path);
    }
    return paths;
}

std::vector<BitFormatInfo> CExternalCodecsInfo::getFormats() const {
    std::vector<BitFormatInfo> result;
    result.reserve(m_formats.size());
    for (const auto& fmt : m_formats) {
        BitFormatInfo info;
        info.name = fmt.name;
        info.extension = fmt.extension;
        info.addExtension = fmt.addExtension;
        info.update = fmt.update;
        info.signature = fmt.signature;
        info.signatureOffset = fmt.signatureOffset;
        info.flags = fmt.flags;
        result.push_back(std::move(info));
    }
    return result;
}

const CExternalFormatInfo* CExternalCodecsInfo::findFormat(const GUID& classID) const {
    for (const auto& fmt : m_formats) {
        if (std::memcmp(&fmt.classID, &classID, sizeof(GUID)) == 0) {
            return &fmt;
        }
    }
    return nullptr;
}

const BitInFormat* CExternalCodecsInfo::findInFormat(const std::string& name) const {
    for (const auto& entry : m_inOutFormats) {
        if (entry.name == name) {
            return entry.format.get();
        }
    }
    for (const auto& entry : m_inFormats) {
        if (entry.name == name) {
            return entry.format.get();
        }
    }
    return nullptr;
}

const BitInOutFormat* CExternalCodecsInfo::findInOutFormat(const std::string& name) const {
    for (const auto& entry : m_inOutFormats) {
        if (entry.name == name) {
            return entry.format.get();
        }
    }
    return nullptr;
}

HRESULT CExternalCodecsInfo::createInArchive(const GUID& classID, void** archive) const {
    const auto* fmt = findFormat(classID);
    if (fmt == nullptr) {
        return E_NOINTERFACE;
    }
    const auto& dll = m_pluginDlls[fmt->dllIndex];
    return dll.createObject(&classID, &IID_IInArchive, archive);
}

HRESULT CExternalCodecsInfo::createOutArchive(const GUID& classID, void** archive) const {
    const auto* fmt = findFormat(classID);
    if (fmt == nullptr) {
        return E_NOINTERFACE;
    }
    const auto& dll = m_pluginDlls[fmt->dllIndex];
    return dll.createObject(&classID, &IID_IOutArchive, archive);
}

bool CExternalCodecsInfo::findCodec(UInt32 index, CPluginDll*& dll, UInt32& localIndex) const {
    for (const auto& plugin : m_pluginDlls) {
        if (index >= plugin.startIndex && index < plugin.startIndex + plugin.numMethods) {
            dll = const_cast<CPluginDll*>(&plugin);
            localIndex = index - plugin.startIndex;
            return true;
        }
    }
    return false;
}

COM_DECLSPEC_NOTHROW
STDMETHODIMP CExternalCodecsInfo::GetNumMethods(UInt32* numMethods) noexcept {
    if (numMethods == nullptr) {
        return E_INVALIDARG;
    }
    *numMethods = m_totalMethods;
    return S_OK;
}

COM_DECLSPEC_NOTHROW
STDMETHODIMP CExternalCodecsInfo::GetProperty(UInt32 index, PROPID propID, PROPVARIANT* value) noexcept {
    CPluginDll* dll = nullptr;
    UInt32 localIndex = 0;
    if (!findCodec(index, dll, localIndex)) {
        return E_INVALIDARG;
    }
    return dll->getMethodProperty(localIndex, propID, value);
}

COM_DECLSPEC_NOTHROW
STDMETHODIMP CExternalCodecsInfo::CreateDecoder(UInt32 index, const GUID* iid, void** coder) noexcept {
    CPluginDll* dll = nullptr;
    UInt32 localIndex = 0;
    if (!findCodec(index, dll, localIndex)) {
        return E_INVALIDARG;
    }
    return dll->createDecoder(localIndex, iid, coder);
}

COM_DECLSPEC_NOTHROW
STDMETHODIMP CExternalCodecsInfo::CreateEncoder(UInt32 index, const GUID* iid, void** coder) noexcept {
    CPluginDll* dll = nullptr;
    UInt32 localIndex = 0;
    if (!findCodec(index, dll, localIndex)) {
        return E_INVALIDARG;
    }
    return dll->createEncoder(localIndex, iid, coder);
}

auto Bit7zLibrary::getFormats() const -> std::vector<BitFormatInfo> {
    std::vector<BitFormatInfo> result;
    try {
        const auto getNumFormats = mLibrary.getFunction<Func_GetNumberOfFormats>("GetNumberOfFormats");
        const auto getHandlerProp = mLibrary.getFunction<Func_GetHandlerProperty2>("GetHandlerProperty2");

        UInt32 numFormats = 0;
        if (getNumFormats(&numFormats) == S_OK && numFormats > 0) {
            result.reserve(numFormats);
            for (UInt32 i = 0; i < numFormats; ++i) {
                BitFormatInfo info;

                BitPropVariant prop;
                if (getHandlerProp(i, NArchive::NHandlerPropID::kName, &prop) == S_OK && prop.vt == VT_BSTR) {
                    info.name = prop.getString();
                }
                prop = BitPropVariant{};
                if (getHandlerProp(i, NArchive::NHandlerPropID::kExtension, &prop) == S_OK && prop.vt == VT_BSTR) {
                    info.extension = prop.getString();
                }
                prop = BitPropVariant{};
                if (getHandlerProp(i, NArchive::NHandlerPropID::kAddExtension, &prop) == S_OK && prop.vt == VT_BSTR) {
                    info.addExtension = prop.getString();
                }
                prop = BitPropVariant{};
                if (getHandlerProp(i, NArchive::NHandlerPropID::kUpdate, &prop) == S_OK && prop.vt == VT_BOOL) {
                    info.update = prop.getBool();
                }
                prop = BitPropVariant{};
                if (getHandlerProp(i, NArchive::NHandlerPropID::kSignature, &prop) == S_OK && prop.vt == VT_BSTR
                    && prop.bstrVal != nullptr) {
                    const auto byteLen = ::SysStringByteLen(prop.bstrVal);
                    if (byteLen > 0) {
                        info.signature.assign(reinterpret_cast<const char*>(prop.bstrVal), byteLen);
                    }
                }
                prop = BitPropVariant{};
                if (getHandlerProp(i, NArchive::NHandlerPropID::kSignatureOffset, &prop) == S_OK && prop.vt == VT_UI4) {
                    info.signatureOffset = prop.getUInt32();
                }
                prop = BitPropVariant{};
                if (getHandlerProp(i, NArchive::NHandlerPropID::kFlags, &prop) == S_OK && prop.vt == VT_UI4) {
                    info.flags = prop.getUInt32();
                }

                result.push_back(std::move(info));
            }
        }

        if (mExternalCodecs != nullptr) {
            auto extFormats = const_cast<CExternalCodecsInfo*>(mExternalCodecs)->getFormats();
            result.reserve(result.size() + extFormats.size());
            for (auto& fmt : extFormats) {
                result.push_back(std::move(fmt));
            }
        }
    }
    catch (const BitException&) {
    }
    return result;
}

auto Bit7zLibrary::getCodecs() const -> std::vector<BitCodecInfo> {
    std::vector<BitCodecInfo> result;
    try {
        const auto getNumMethods = mLibrary.getFunction<Func_GetNumberOfMethods>("GetNumberOfMethods");
        const auto getMethodProp = mLibrary.getFunction<Func_GetMethodProperty>("GetMethodProperty");

        UInt32 numMethods = 0;
        if (getNumMethods(&numMethods) == S_OK && numMethods > 0) {
            result.reserve(numMethods);
            for (UInt32 i = 0; i < numMethods; ++i) {
                BitCodecInfo info;

                BitPropVariant prop;
                if (getMethodProp(i, ::NMethodPropID::kID, &prop) == S_OK && prop.vt == VT_UI8) {
                    info.id = prop.getUInt64();
                }
                prop = BitPropVariant{};
                if (getMethodProp(i, ::NMethodPropID::kName, &prop) == S_OK && prop.vt == VT_BSTR) {
                    info.name = prop.getString();
                }
                prop = BitPropVariant{};
                if (getMethodProp(i, ::NMethodPropID::kDecoder, &prop) == S_OK && prop.vt == VT_BSTR) {
                    info.decoder = ::SysStringByteLen(prop.bstrVal) == sizeof(GUID);
                }
                prop = BitPropVariant{};
                if (getMethodProp(i, ::NMethodPropID::kEncoder, &prop) == S_OK && prop.vt == VT_BSTR) {
                    info.encoder = ::SysStringByteLen(prop.bstrVal) == sizeof(GUID);
                }
                prop = BitPropVariant{};
                if (getMethodProp(i, ::NMethodPropID::kPackStreams, &prop) == S_OK && prop.vt == VT_UI4) {
                    info.packStreams = prop.getUInt32();
                }
                prop = BitPropVariant{};
                if (getMethodProp(i, ::NMethodPropID::kUnpackStreams, &prop) == S_OK && prop.vt == VT_UI4) {
                    info.unpackStreams = prop.getUInt32();
                }
                prop = BitPropVariant{};
                if (getMethodProp(i, ::NMethodPropID::kDescription, &prop) == S_OK && prop.vt == VT_BSTR) {
                    info.description = prop.getString();
                }
                prop = BitPropVariant{};
                if (getMethodProp(i, ::NMethodPropID::kIsFilter, &prop) == S_OK && prop.vt == VT_BOOL) {
                    info.isFilter = prop.getBool();
                }

                result.push_back(std::move(info));
            }
        }

        if (mExternalCodecs != nullptr) {
            auto* extCodecs = const_cast<CExternalCodecsInfo*>(mExternalCodecs);
            UInt32 extNumMethods = 0;
            if (extCodecs->GetNumMethods(&extNumMethods) == S_OK && extNumMethods > 0) {
                result.reserve(result.size() + extNumMethods);
                for (UInt32 i = 0; i < extNumMethods; ++i) {
                    BitCodecInfo info;
                    info.isExternal = true;

                    BitPropVariant prop;
                    if (extCodecs->GetProperty(i, ::NMethodPropID::kID, &prop) == S_OK && prop.vt == VT_UI8) {
                        info.id = prop.getUInt64();
                    }
                    prop = BitPropVariant{};
                    if (extCodecs->GetProperty(i, ::NMethodPropID::kName, &prop) == S_OK && prop.vt == VT_BSTR) {
                        info.name = prop.getString();
                    }
                    prop = BitPropVariant{};
                    if (extCodecs->GetProperty(i, ::NMethodPropID::kDecoder, &prop) == S_OK && prop.vt == VT_BSTR) {
                        info.decoder = ::SysStringByteLen(prop.bstrVal) == sizeof(GUID);
                    }
                    prop = BitPropVariant{};
                    if (extCodecs->GetProperty(i, ::NMethodPropID::kEncoder, &prop) == S_OK && prop.vt == VT_BSTR) {
                        info.encoder = ::SysStringByteLen(prop.bstrVal) == sizeof(GUID);
                    }
                    prop = BitPropVariant{};
                    if (extCodecs->GetProperty(i, ::NMethodPropID::kPackStreams, &prop) == S_OK && prop.vt == VT_UI4) {
                        info.packStreams = prop.getUInt32();
                    }
                    prop = BitPropVariant{};
                    if (extCodecs->GetProperty(i, ::NMethodPropID::kUnpackStreams, &prop) == S_OK
                        && prop.vt == VT_UI4) {
                        info.unpackStreams = prop.getUInt32();
                    }
                    prop = BitPropVariant{};
                    if (extCodecs->GetProperty(i, ::NMethodPropID::kDescription, &prop) == S_OK && prop.vt == VT_BSTR) {
                        info.description = prop.getString();
                    }
                    prop = BitPropVariant{};
                    if (extCodecs->GetProperty(i, ::NMethodPropID::kIsFilter, &prop) == S_OK && prop.vt == VT_BOOL) {
                        info.isFilter = prop.getBool();
                    }

                    result.push_back(std::move(info));
                }
            }
        }
    }
    catch (const BitException&) {
    }
    return result;
}

std::vector<std::string> Bit7zLibrary::getCodecPaths() const {
    std::vector<std::string> result;
    if (mExternalCodecs == nullptr) {
        return result;
    }
    return const_cast<CExternalCodecsInfo*>(mExternalCodecs)->getCodecPaths();
}

} // namespace bit7z
