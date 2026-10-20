/*
 * bit7z - A C++ static library to interface with the 7-zip shared libraries.
 * Copyright (c) 2014-2023 Riccardo Ostani - All Rights Reserved.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

#ifndef BEXTERNALCODECS_HPP
#define BEXTERNALCODECS_HPP

#include "bitformat.hpp"
#include "bitformatinfo.hpp"
#include "bitsharedlibrary.hpp"
#include "bittypes.hpp"
#include "internal/com.hpp"
#include "internal/guids.hpp"
#include "internal/macros.hpp"

#include <7zip/Archive/IArchive.h>
#include <7zip/ICoder.h>

#include <cstdint>
#include <list>
#include <memory>
#include <string>
#include <vector>

namespace bit7z {

struct CExternalFormatInfo {
    GUID classID;
    std::string name;
    std::string extension;
    std::string addExtension;
    bool update = false;
    std::string signature;
    std::uint32_t signatureOffset = 0;
    std::uint32_t flags = 0;
    std::size_t dllIndex = 0;
};

class CExternalCodecsInfo final : public ICompressCodecsInfo, public CMyUnknownImp {
public:
    CExternalCodecsInfo() = default;
    ~CExternalCodecsInfo();

    CExternalCodecsInfo(const CExternalCodecsInfo&) = delete;
    CExternalCodecsInfo(CExternalCodecsInfo&&) = delete;
    auto operator=(const CExternalCodecsInfo&) -> CExternalCodecsInfo& = delete;
    auto operator=(CExternalCodecsInfo&&) -> CExternalCodecsInfo& = delete;

    // Follows the official 7-Zip LoadCodecs.cpp flow: for each supplied
    // folder the Codecs subfolder is scanned first, then the Formats
    // subfolder.  Every DLL is inspected for both codec exports
    // (GetNumberOfMethods / GetMethodProperty / CreateDecoder /
    // CreateEncoder) and format-handler exports (CreateObject /
    // GetNumberOfFormats / GetHandlerProperty2), so a single DLL can supply
    // both codecs and archive handlers.
    //
    // Multiple folders can be supplied; they are scanned in order and the
    // results are accumulated (append mode).
    bool loadPlugins(const std::vector<tstring>& pluginPaths);

    std::vector<std::string> getCodecPaths() const;
    std::vector<BitFormatInfo> getFormats() const;

    const CExternalFormatInfo* findFormat(const GUID& classID) const;
    const BitInFormat* findInFormat(const std::string& name) const;
    const BitInOutFormat* findInOutFormat(const std::string& name) const;
    HRESULT createInArchive(const GUID& classID, void** archive) const;
    HRESULT createOutArchive(const GUID& classID, void** archive) const;

    MY_UNKNOWN_IMP1(ICompressCodecsInfo)

    BIT7Z_STDMETHOD(GetNumMethods, UInt32* numMethods);
    BIT7Z_STDMETHOD(GetProperty, UInt32 index, PROPID propID, PROPVARIANT* value);
    BIT7Z_STDMETHOD(CreateDecoder, UInt32 index, const GUID* iid, void** coder);
    BIT7Z_STDMETHOD(CreateEncoder, UInt32 index, const GUID* iid, void** coder);

private:
    using CreateObjectFunc = HRESULT(WINAPI*)(const GUID* clsID, const GUID* iid, void** outObject);

    // A single loaded plugin DLL.  It may expose codec entry points,
    // format-handler entry points, or both (as the 7-Zip-zstd format
    // modules do).
    struct CPluginDll {
        std::unique_ptr<BitSharedLibrary> library;

        // Codec exports
        Func_GetNumberOfMethods getNumberOfMethods = nullptr;
        Func_GetMethodProperty getMethodProperty = nullptr;
        Func_CreateDecoder createDecoder = nullptr;
        Func_CreateEncoder createEncoder = nullptr;
        UInt32 numMethods = 0;
        UInt32 startIndex = 0;

        // Format-handler exports
        CreateObjectFunc createObject = nullptr;

        std::string path;
    };

    std::vector<CPluginDll> m_pluginDlls;
    UInt32 m_totalMethods = 0;

    std::vector<CExternalFormatInfo> m_formats;

    struct CInFormatEntry {
        std::string name;
        std::unique_ptr<BitInFormat> format;
    };
    struct CInOutFormatEntry {
        std::string name;
        tstring extension;
        std::unique_ptr<BitInOutFormat> format;
    };

    std::list<CInFormatEntry> m_inFormats;
    std::list<CInOutFormatEntry> m_inOutFormats;

    bool findCodec(UInt32 index, CPluginDll*& dll, UInt32& localIndex) const;
    bool loadDllsFromFolder(const std::string& folderPath);
};

} // namespace bit7z

#endif // BEXTERNALCODECS_HPP
