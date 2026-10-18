vcpkg_check_linkage(ONLY_DYNAMIC_LIBRARY)

vcpkg_from_github(
    OUT_SOURCE_PATH SOURCE_PATH
    REPO mcmilk/7-Zip-zstd
    REF "v26.02-v1.5.7-R2"
    SHA512 07856251d14c9fcffe0635037adbc80be9988ee5b1bd2b55a3f4cdf126eb7cb1431fa6cf7f99854e214d7d2f20c48a2680b76da9642d2a5045d93feda36bcaf3
    HEAD_REF master
)

file(COPY "${CMAKE_CURRENT_LIST_DIR}/CMakeLists.txt" DESTINATION "${SOURCE_PATH}")
file(COPY "${CMAKE_CURRENT_LIST_DIR}/7zip-zstd-codecs-config.cmake.in" DESTINATION "${SOURCE_PATH}")

vcpkg_replace_string(
    "${SOURCE_PATH}/CPP/7zip/Compress/LizardEncoder.cpp"
    "          _props._level = mylevel;"
    "          _props._level = mylevel;
        if (_props._level < LIZARDMT_LEVEL_MIN)
          _props._level = LIZARDMT_LEVEL_MIN;"
)

vcpkg_replace_string(
    "${SOURCE_PATH}/CPP/7zip/Compress/Lz4Encoder.cpp"
    "        if (_props._level > mylevel)
          _props._level = mylevel;"
    "        if (_props._level > mylevel)
          _props._level = mylevel;
        if (_props._level < LZ4MT_LEVEL_MIN)
          _props._level = LZ4MT_LEVEL_MIN;"
)

vcpkg_replace_string(
    "${SOURCE_PATH}/CPP/7zip/Compress/Lz5Encoder.cpp"
    "        if (_props._level > mylevel)
          _props._level = mylevel;"
    "        if (_props._level > mylevel)
          _props._level = mylevel;
        if (_props._level < LZ5MT_LEVEL_MIN)
          _props._level = LZ5MT_LEVEL_MIN;"
)

# Fix use-after-free in Extract(): outStream.Release() deletes the
# CDummyOutStream object owned by outStreamSpec, but later code calls
# outStreamSpec->GetSize() on the freed pointer.  Capture the size into a
# local variable before Release() and use it afterwards.
foreach(_handler BrotliHandler LizardHandler Lz4Handler Lz5Handler ZstdHandler)
    set(_handler_file "${SOURCE_PATH}/CPP/7zip/Archive/${_handler}.cpp")
    if(EXISTS "${_handler_file}")
        vcpkg_replace_string(
            "${_handler_file}"
            "  decoderSpec->ReleaseInStream();
  outStream.Release();"
            "  decoderSpec->ReleaseInStream();
  const UInt64 _outStreamSize = outStreamSpec->GetSize();
  outStream.Release();"
        )
        vcpkg_replace_string(
            "${_handler_file}"
            "    _unpackSize = outStreamSpec->GetSize();"
            "    _unpackSize = _outStreamSize;"
        )
    endif()
endforeach()

# musl libc defaults thread stacks to ~128 KB (vs ~8 MB on glibc),
# which is too small for the lizard/zstdmt compression worker threads
# and causes stack overflow / SIGSEGV on musllinux. Set an explicit
# 1 MB stack size for every zstdmt worker thread.
# The replacement is applied on all platforms, but the actual stack
# override is guarded by `#if defined(__musl__)` so only musl libc
# builds take it. On glibc / Windows the original NULL attr is kept
# (Windows threading.h shim does not provide pthread_attr_t anyway).
foreach(_codec brotli lz4 lz5 lizard)
    set(_file "${SOURCE_PATH}/C/zstdmt/${_codec}-mt_compress.c")
    if(EXISTS "${_file}")
        vcpkg_replace_string(
            "${_file}"
            [[pthread_create(&w->pthread, NULL, pt_compress, w);]]
            [[
#if defined(__MUSL__)
    { 
        pthread_attr_t _mt_attr;
        pthread_attr_init(&_mt_attr);
        pthread_attr_setstacksize(&_mt_attr, 1 << 20);
        pthread_create(&w->pthread, &_mt_attr, pt_compress, w);
        pthread_attr_destroy(&_mt_attr);
    }
#else
    pthread_create(&w->pthread, NULL, pt_compress, w);
#endif]]
        )
    endif()
    set(_file "${SOURCE_PATH}/C/zstdmt/${_codec}-mt_decompress.c")
    if(EXISTS "${_file}")
        vcpkg_replace_string(
            "${_file}"
            [[pthread_create(&wt->pthread, NULL, pt_decompress, wt);]]
            [[
#if defined(__MUSL__)
    { 
        pthread_attr_t _mt_attr;
        pthread_attr_init(&_mt_attr);
        pthread_attr_setstacksize(&_mt_attr, 1 << 20);
        pthread_create(&wt->pthread, &_mt_attr, pt_decompress, wt);
        pthread_attr_destroy(&_mt_attr);
    }
#else
    pthread_create(&wt->pthread, NULL, pt_decompress, wt);
#endif]]
        )
    endif()
endforeach()

vcpkg_cmake_configure(
    SOURCE_PATH "${SOURCE_PATH}"
)

vcpkg_cmake_install()
vcpkg_copy_pdbs()

file(INSTALL "${SOURCE_PATH}/DOC/License.txt" DESTINATION "${CURRENT_PACKAGES_DIR}/share/${PORT}" RENAME copyright)

file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/share")