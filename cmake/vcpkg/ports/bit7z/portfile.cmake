vcpkg_check_linkage(ONLY_STATIC_LIBRARY)

vcpkg_from_github(
    OUT_SOURCE_PATH SOURCE_PATH
    REPO rikyoz/bit7z
    REF "v${VERSION}"
    SHA512 d240997e3b1f6eb8d0b19c89bf3b12044cbb10ba495b4ba535efc1cd04390157031a303025819b6fd9a6a51bdca7b59ad50df45055cbde9130ffd4c8279a0863
    HEAD_REF master
    PATCHES fix_dependencies.patch
)

# Copy external codecs support source files (internal)
file(COPY "${CMAKE_CURRENT_LIST_DIR}/bexternalcodecs.hpp" DESTINATION "${SOURCE_PATH}/src/internal")
file(COPY "${CMAKE_CURRENT_LIST_DIR}/bexternalcodecs.cpp" DESTINATION "${SOURCE_PATH}/src/internal")
# Copy the public header (BitFormatInfo / BitCodecInfo) to the public include directory
file(COPY "${CMAKE_CURRENT_LIST_DIR}/bitformatinfo.hpp" DESTINATION "${SOURCE_PATH}/include/bit7z")

# Register new source files in CMakeLists.txt
vcpkg_replace_string("${SOURCE_PATH}/CMakeLists.txt"
    "        src/internal/failuresourcecategory.cpp"
    "        src/internal/failuresourcecategory.cpp\n        src/internal/bexternalcodecs.cpp"
)

# Register the public header in PUBLIC_HEADERS list so it gets installed
vcpkg_replace_string("${SOURCE_PATH}/CMakeLists.txt"
    "        include/bit7z/bit7z.hpp"
    "        include/bit7z/bit7z.hpp\n        include/bit7z/bitformatinfo.hpp"
)
vcpkg_replace_string("${SOURCE_PATH}/CMakeLists.txt"
    "        src/internal/bufferutil.hpp"
    "        src/internal/bufferutil.hpp
        src/internal/bexternalcodecs.hpp"
)

# Add loadPlugins / getFormats / getCodecs / ... methods to Bit7zLibrary public API
vcpkg_replace_string("${SOURCE_PATH}/include/bit7z/bit7zlibrary.hpp"
    "    private:
        BitSharedLibrary mLibrary;"
    "        /**
         * @brief Loads external codec and format DLLs from the given folders and
         *        registers them with the 7-zip library.
         *
         * Follows the official 7-Zip LoadCodecs.cpp flow: the Codecs folder is
         * scanned first, then the Formats folder.  Every DLL is inspected for
         * both codec exports (GetNumberOfMethods / GetMethodProperty /
         * CreateDecoder / CreateEncoder) and format-handler exports
         * (CreateObject / GetNumberOfFormats / GetHandlerProperty2), so a
         * single DLL can supply both codecs and archive handlers.
         *
         * @param codecsPath   the path to the folder containing codec DLLs.
         * @param formatsPath  the path to the folder containing format handler DLLs.
         * @return true if at least one codec or format was successfully loaded.
         */
        bool loadPlugins( const tstring& codecsPath, const tstring& formatsPath );

        /**
         * @brief Enumerates all archive formats supported by the loaded 7-zip library.
         *
         * @return a vector of BitFormatInfo describing each supported format.
         */
        auto getFormats() const -> std::vector< struct BitFormatInfo >;

        /**
         * @brief Enumerates all compression codecs (methods) supported by the loaded 7-zip library.
         *
         * @return a vector of BitCodecInfo describing each supported codec.
         */
        auto getCodecs() const -> std::vector< struct BitCodecInfo >;

        /**
         * @brief Returns the paths of all external codec DLLs currently loaded.
         *
         * @return a vector of strings with the file paths of the loaded codec DLLs.
         */
        auto getCodecPaths() const -> std::vector< std::string >;

        /**
         * @brief Returns the read-only archive format (BitInFormat) for the given
         *        external format name, if it was loaded.
         *
         * @param name the name of the external format (as returned by getFormats).
         * @return a pointer to the BitInFormat, or nullptr if not found.
         */
        const class BitInFormat* getExternalInFormat( const std::string& name ) const;

        /**
         * @brief Returns the read-write archive format (BitInOutFormat) for the given
         *        external format name, if it was loaded.
         *
         * @param name the name of the external format (as returned by getFormats).
         * @return a pointer to the BitInOutFormat, or nullptr if not found.
         */
        const class BitInOutFormat* getExternalInOutFormat( const std::string& name ) const;

        ~Bit7zLibrary();
    private:
        BitSharedLibrary mLibrary;
        class CExternalCodecsInfo* mExternalCodecs = nullptr;
        void releaseExternalCodecs();"
)

# Change default destructor to custom one (must be done after adding the declaration above)
vcpkg_replace_string("${SOURCE_PATH}/include/bit7z/bit7zlibrary.hpp"
    "        ~Bit7zLibrary() = default;"
    ""
)

# Add include and implementation in bit7zlibrary.cpp
vcpkg_replace_string("${SOURCE_PATH}/src/bit7zlibrary.cpp"
    "#include \"bit7zlibrary.hpp\""
    "#include \"bit7zlibrary.hpp\"
#include \"internal/bexternalcodecs.hpp\""
)
vcpkg_replace_string("${SOURCE_PATH}/src/bit7zlibrary.cpp"
    "using CreateObjectFunc = HRESULT (WINAPI*)( const GUID* clsID"
    "void Bit7zLibrary::releaseExternalCodecs() {
    if ( mExternalCodecs == nullptr ) {
        return;
    }
    using SetCodecsFunc = HRESULT ( WINAPI* )( ICompressCodecsInfo* );
    try {
        SetCodecsFunc pSetCodecs = mLibrary.getFunction< SetCodecsFunc >( \"SetCodecs\" );
        // SetCodecs( nullptr ) invokes g_ExternalCodecs.ClearAndRelease(), which
        // releases the ICompressCodecsInfo held by g_ExternalCodecs.GetCodecs.
        // Since that CMyComPtr owns the single strong reference to our
        // CExternalCodecsInfo (refcount drops to 0), the object is deleted
        // inside this call.  We must NOT call mExternalCodecs->Release()
        // afterwards, or it would be a use-after-free.
        pSetCodecs( nullptr );
        mExternalCodecs = nullptr;
        return;
    } catch ( const BitException& ) {
    }
    // SetCodecs is unavailable (e.g. 7z.so built without external-codec
    // support): release the object directly.
    mExternalCodecs->Release();
    mExternalCodecs = nullptr;
}

Bit7zLibrary::~Bit7zLibrary() {
    releaseExternalCodecs();
}

bool Bit7zLibrary::loadPlugins( const tstring& codecsPath, const tstring& formatsPath ) {
    using SetCodecsFunc = HRESULT ( WINAPI* )( ICompressCodecsInfo* );
    SetCodecsFunc pSetCodecs = nullptr;
    try {
        pSetCodecs = mLibrary.getFunction< SetCodecsFunc >( \"SetCodecs\" );
    } catch ( const BitException& ) {
        return false;
    }

    if ( mExternalCodecs == nullptr ) {
        mExternalCodecs = new CExternalCodecsInfo();
    }

    if ( !mExternalCodecs->loadPlugins( codecsPath, formatsPath ) ) {
        return false;
    }

    const HRESULT res = pSetCodecs( mExternalCodecs );
    if ( res != S_OK ) {
        return false;
    }

    return true;
}

const BitInFormat* Bit7zLibrary::getExternalInFormat( const std::string& name ) const {
    if ( mExternalCodecs == nullptr ) {
        return nullptr;
    }
    return const_cast< CExternalCodecsInfo* >( mExternalCodecs )->findInFormat( name );
}

const BitInOutFormat* Bit7zLibrary::getExternalInOutFormat( const std::string& name ) const {
    if ( mExternalCodecs == nullptr ) {
        return nullptr;
    }
    return const_cast< CExternalCodecsInfo* >( mExternalCodecs )->findInOutFormat( name );
}

using CreateObjectFunc = HRESULT (WINAPI*)( const GUID* clsID"
)

# Route external archive formats to their owning format DLL's CreateObject.
vcpkg_replace_string("${SOURCE_PATH}/src/bit7zlibrary.cpp"
    "BIT7Z_NODISCARD
auto Bit7zLibrary::initInArchive( const BitInFormat& format ) const -> CMyComPtr< IInArchive > {
    CMyComPtr< IInArchive > inArchive{};
    const HRESULT res = createArchiveObject( mCreateObjectFunc, format, &inArchive );
    if ( res != S_OK || inArchive == nullptr ) {
        throw BitException( \"Failed to initialize the input archive object\", make_hresult_code( res ) );
    }
    return inArchive;
}"
    "BIT7Z_NODISCARD
auto Bit7zLibrary::initInArchive( const BitInFormat& format ) const -> CMyComPtr< IInArchive > {
    CMyComPtr< IInArchive > inArchive{};
    const auto formatID = formatGuid( format );
    HRESULT res = E_FAIL;
    if ( mExternalCodecs != nullptr &&
         const_cast< CExternalCodecsInfo* >( mExternalCodecs )->findFormat( formatID ) != nullptr ) {
        res = const_cast< CExternalCodecsInfo* >( mExternalCodecs )
                  ->createInArchive( formatID, reinterpret_cast< void** >( &inArchive ) );
    } else {
        res = createArchiveObject( mCreateObjectFunc, format, &inArchive );
    }
    if ( res != S_OK || inArchive == nullptr ) {
        throw BitException( \"Failed to initialize the input archive object\", make_hresult_code( res ) );
    }
    return inArchive;
}"
)

vcpkg_replace_string("${SOURCE_PATH}/src/bit7zlibrary.cpp"
    "BIT7Z_NODISCARD
auto Bit7zLibrary::initOutArchive( const BitInOutFormat& format ) const -> CMyComPtr< IOutArchive > {
    CMyComPtr< IOutArchive > outArchive{};
    const HRESULT res = createArchiveObject( mCreateObjectFunc, format, &outArchive );
    if ( res != S_OK || outArchive == nullptr ) {
        throw BitException( \"Failed to initialize the output archive object\", make_hresult_code( res ) );
    }
    return outArchive;
}"
    "BIT7Z_NODISCARD
auto Bit7zLibrary::initOutArchive( const BitInOutFormat& format ) const -> CMyComPtr< IOutArchive > {
    CMyComPtr< IOutArchive > outArchive{};
    const auto formatID = formatGuid( format );
    HRESULT res = E_FAIL;
    if ( mExternalCodecs != nullptr &&
         const_cast< CExternalCodecsInfo* >( mExternalCodecs )->findFormat( formatID ) != nullptr ) {
        res = const_cast< CExternalCodecsInfo* >( mExternalCodecs )
                  ->createOutArchive( formatID, reinterpret_cast< void** >( &outArchive ) );
    } else {
        res = createArchiveObject( mCreateObjectFunc, format, &outArchive );
    }
    if ( res != S_OK || outArchive == nullptr ) {
        throw BitException( \"Failed to initialize the output archive object\", make_hresult_code( res ) );
    }
    return outArchive;
}"
)

vcpkg_replace_string("${SOURCE_PATH}/include/bit7z/bitabstractarchivecreator.hpp"
    [[protected:]]
    [[
    void setFormatProperty( const std::wstring& name, const BitPropVariant& value ) noexcept { mExtraProperties[ name ] = value; }
    protected:]]
)

# Add RTLD_LOCAL | RTLD_NODELETE to dlopen so codec .so symbols don't
# enter the global namespace (prevents ELF interpose). RTLD_NODELETE makes
# dlclose a no-op so codec .so are never unmapped at runtime — the glibc
# cleanup ordering during Python process shutdown otherwise triggers
# use-after-free / heap corruption in dlclose.
vcpkg_replace_string("${SOURCE_PATH}/src/bitsharedlibrary.cpp"
    "dlopen( (lib_name), RTLD_LAZY )"
    "dlopen( (lib_name), RTLD_LAZY | RTLD_LOCAL | RTLD_NODELETE )"
)
vcpkg_check_features(
    OUT_FEATURE_OPTIONS FEATURE_OPTIONS
    FEATURES
        regex-matching                  BIT7Z_REGEX_MATCHING
)

vcpkg_cmake_configure(
    SOURCE_PATH "${SOURCE_PATH}"
    OPTIONS
        -DCMAKE_POSITION_INDEPENDENT_CODE=ON
        -DBIT7Z_USE_SYSTEM_DEPENDENCIES=ON
        -DBIT7Z_AUTO_FORMAT=ON
        -DBIT7Z_AUTO_PREFIX_LONG_PATHS=ON
        -DBIT7Z_DISABLE_ZIP_ASCII_PWD_CHECK=OFF
        -DBIT7Z_PATH_SANITIZATION=ON
        -DBIT7Z_DISABLE_USE_STD_FILESYSTEM=OFF
        -DBIT7Z_USE_STD_BYTE=OFF
        -DBIT7Z_USE_NATIVE_STRING=OFF
        -DBIT7Z_USE_SYSTEM_CODEPAGE=OFF
        -DBIT7Z_BUILD_TESTS=OFF
        -DBIT7Z_BUILD_DOCS=OFF
        -DBIT7Z_WARNINGS_AS_ERRORS=OFF
        ${FEATURE_OPTIONS}
)

vcpkg_cmake_install()
vcpkg_copy_pdbs()

vcpkg_cmake_config_fixup(PACKAGE_NAME bit7z CONFIG_PATH lib/cmake/bit7z)

vcpkg_install_copyright(FILE_LIST "${SOURCE_PATH}/LICENSE")

file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include" "${CURRENT_PACKAGES_DIR}/debug/share")
