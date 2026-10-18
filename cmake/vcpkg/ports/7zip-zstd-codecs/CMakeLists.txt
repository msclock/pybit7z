cmake_minimum_required(VERSION 3.19)

project(7zip-zstd-codecs LANGUAGES C CXX)

find_package(7zip CONFIG REQUIRED)

function(add_codec_dll name codec_sources extra_defs extra_includes)
    add_library(${name} SHARED
        CPP/7zip/Bundles/Codec_${name}/StdAfx.cpp
        ${codec_sources}
    )

    if(WIN32)
        target_sources(${name} PRIVATE "${VCPKG_INSTALLED_DIR}/${VCPKG_TARGET_TRIPLET}/include/7zip/CPP/7zip/Compress/Codec.def")
    endif()

    target_link_libraries(${name} PRIVATE 7zip::7zip-codec-common)

    target_include_directories(${name} PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/CPP
        ${CMAKE_CURRENT_SOURCE_DIR}/C
        ${extra_includes}
    )

    target_compile_definitions(${name} PRIVATE ${extra_defs})

    set_target_properties(${name} PROPERTIES
        OUTPUT_NAME ${name}
        PREFIX ""
    )

    if(NOT MSVC)
        target_compile_options(${name} PRIVATE -fvisibility=hidden)
    endif()
endfunction()

function(add_format_dll name handler_source codec_sources extra_defs extra_includes)
    add_library(fmt_${name} SHARED
        ${handler_source}
        ${codec_sources}
    )

    if(WIN32)
        target_sources(fmt_${name} PRIVATE "${VCPKG_INSTALLED_DIR}/${VCPKG_TARGET_TRIPLET}/include/7zip/CPP/7zip/Archive/Archive2.def")
    endif()

    target_link_libraries(fmt_${name} PRIVATE 7zip::7zip-format-common)

    target_include_directories(fmt_${name} PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/CPP
        ${CMAKE_CURRENT_SOURCE_DIR}/C
        ${extra_includes}
    )

    target_compile_definitions(fmt_${name} PRIVATE ${extra_defs})

    set_target_properties(fmt_${name} PROPERTIES
        OUTPUT_NAME ${name}
        PREFIX ""
    )

    if(NOT MSVC)
        target_compile_options(fmt_${name} PRIVATE -fvisibility=hidden)
    endif()
endfunction()

# ---------------------------------------------------------------------------
# flzma2.dll (Fast LZMA2) -- codec only, no archive handler
# ---------------------------------------------------------------------------
file(GLOB FLZMA2_C_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/C/fast-lzma2/*.c")
add_codec_dll(flzma2
    "CPP/7zip/Compress/Lzma2Decoder.cpp;CPP/7zip/Compress/Lzma2Encoder.cpp;CPP/7zip/Compress/LzmaDecoder.cpp;CPP/7zip/Compress/LzmaEncoder.cpp;CPP/7zip/Compress/FastLzma2Register.cpp;C/LzFindMt.c;C/LzFindOpt.c;C/Lzma2Dec.c;C/Lzma2DecMt.c;C/Lzma2Enc.c;C/LzmaDec.c;C/LzmaEnc.c;C/MtCoder.c;C/MtDec.c;${FLZMA2_C_SOURCES}"
    "NO_XXHASH;FL2_7ZIP_BUILD"
    "${CMAKE_CURRENT_SOURCE_DIR}/C/fast-lzma2"
)

# ---------------------------------------------------------------------------
# Install codec-only binaries into bin/codecs
# ---------------------------------------------------------------------------
set(CODEC_TARGETS flzma2)

install(
    TARGETS ${CODEC_TARGETS}
    RUNTIME DESTINATION bin/codecs
    LIBRARY DESTINATION bin/codecs
)

# ===========================================================================
# External archive handler (format) DLLs
# ===========================================================================

file(GLOB ZSTD_C_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/C/zstd/*.c")
file(GLOB BROTLI_C_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/C/brotli/*.c")

# ---------------------------------------------------------------------------
# zstd format DLL  (zst / zstd / tzst / tzstd)
# ---------------------------------------------------------------------------
add_format_dll(zstd
    "CPP/7zip/Archive/ZstdHandler.cpp"
    "CPP/7zip/Compress/ZstdDecoder.cpp;CPP/7zip/Compress/ZstdEncoder.cpp;CPP/7zip/Compress/ZstdRegister.cpp;${ZSTD_C_SOURCES};C/hashes/xxhash.c;C/zstdmt/zstd-mt_threading.c"
    "ZSTD_LEGACY_SUPPORT;ZSTD_MULTITHREAD;ZSTD_DISABLE_ASM"
    "${CMAKE_CURRENT_SOURCE_DIR}/C/zstd;${CMAKE_CURRENT_SOURCE_DIR}/C/zstdmt;${CMAKE_CURRENT_SOURCE_DIR}/C/hashes"
)

# ---------------------------------------------------------------------------
# brotli format DLL  (br / brotli / tbr)
# ---------------------------------------------------------------------------
add_format_dll(brotli
    "CPP/7zip/Archive/BrotliHandler.cpp"
    "CPP/7zip/Compress/BrotliDecoder.cpp;CPP/7zip/Compress/BrotliEncoder.cpp;CPP/7zip/Compress/BrotliRegister.cpp;${BROTLI_C_SOURCES};C/zstdmt/brotli-mt_common.c;C/zstdmt/brotli-mt_compress.c;C/zstdmt/brotli-mt_decompress.c;C/zstdmt/zstd-mt_threading.c"
    ""
    "${CMAKE_CURRENT_SOURCE_DIR}/C/brotli;${CMAKE_CURRENT_SOURCE_DIR}/C/zstd;${CMAKE_CURRENT_SOURCE_DIR}/C/zstdmt"
)

# ---------------------------------------------------------------------------
# lz4 format DLL  (lz4 / tlz4)
# ---------------------------------------------------------------------------
add_format_dll(lz4
    "CPP/7zip/Archive/Lz4Handler.cpp"
    "CPP/7zip/Compress/Lz4Decoder.cpp;CPP/7zip/Compress/Lz4Encoder.cpp;CPP/7zip/Compress/Lz4Register.cpp;C/lz4/lz4.c;C/lz4/lz4frame.c;C/lz4/lz4hc.c;C/hashes/xxhash.c;C/zstdmt/lz4-mt_common.c;C/zstdmt/lz4-mt_compress.c;C/zstdmt/lz4-mt_decompress.c;C/zstdmt/zstd-mt_threading.c"
    ""
    "${CMAKE_CURRENT_SOURCE_DIR}/C/lz4;${CMAKE_CURRENT_SOURCE_DIR}/C/zstd;${CMAKE_CURRENT_SOURCE_DIR}/C/zstdmt"
)

# ---------------------------------------------------------------------------
# lz5 format DLL  (lz5 / tlz5)
# ---------------------------------------------------------------------------
add_format_dll(lz5
    "CPP/7zip/Archive/Lz5Handler.cpp"
    "CPP/7zip/Compress/Lz5Decoder.cpp;CPP/7zip/Compress/Lz5Encoder.cpp;CPP/7zip/Compress/Lz5Register.cpp;C/lz5/lz5.c;C/lz5/lz5frame.c;C/lz5/lz5hc.c;C/hashes/xxhash.c;C/zstdmt/lz5-mt_common.c;C/zstdmt/lz5-mt_compress.c;C/zstdmt/lz5-mt_decompress.c;C/zstdmt/zstd-mt_threading.c"
    ""
    "${CMAKE_CURRENT_SOURCE_DIR}/C/lz5;${CMAKE_CURRENT_SOURCE_DIR}/C/zstd;${CMAKE_CURRENT_SOURCE_DIR}/C/zstdmt"
)

# ---------------------------------------------------------------------------
# lizard format DLL  (liz / tliz)
# ---------------------------------------------------------------------------
add_format_dll(lizard
    "CPP/7zip/Archive/LizardHandler.cpp"
    "CPP/7zip/Compress/LizardDecoder.cpp;CPP/7zip/Compress/LizardEncoder.cpp;CPP/7zip/Compress/LizardRegister.cpp;C/lizard/lizard_compress.c;C/lizard/lizard_decompress.c;C/lizard/lizard_frame.c;C/lizard/liz_entropy_common.c;C/lizard/liz_fse_compress.c;C/lizard/liz_fse_decompress.c;C/lizard/liz_huf_compress.c;C/lizard/liz_huf_decompress.c;C/zstd/debug.c;C/zstd/entropy_common.c;C/zstd/error_private.c;C/zstd/fse_compress.c;C/zstd/fse_decompress.c;C/zstd/hist.c;C/zstd/huf_compress.c;C/zstd/huf_decompress.c;C/hashes/xxhash.c;C/zstdmt/lizard-mt_common.c;C/zstdmt/lizard-mt_compress.c;C/zstdmt/lizard-mt_decompress.c;C/zstdmt/zstd-mt_threading.c"
    "ZSTD_DISABLE_ASM"
    "${CMAKE_CURRENT_SOURCE_DIR}/C/lizard;${CMAKE_CURRENT_SOURCE_DIR}/C/zstd;${CMAKE_CURRENT_SOURCE_DIR}/C/zstdmt"
)

# ---------------------------------------------------------------------------
# Install all format binaries into bin/Formats
# ---------------------------------------------------------------------------
set(FORMAT_TARGETS fmt_zstd fmt_brotli fmt_lz4 fmt_lz5 fmt_lizard)

install(
    TARGETS ${FORMAT_TARGETS}
    RUNTIME DESTINATION bin/Formats
    LIBRARY DESTINATION bin/Formats
)

include(CMakePackageConfigHelpers)
configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/7zip-zstd-codecs-config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/7zip-zstd-codecs-config.cmake"
    @ONLY
)
install(
    FILES "${CMAKE_CURRENT_BINARY_DIR}/7zip-zstd-codecs-config.cmake"
    DESTINATION "share/7zip-zstd-codecs"
)
