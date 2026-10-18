cmake_minimum_required(VERSION 3.19)

project(7zip-zstd-codecs LANGUAGES C CXX)

option(USE_NO_ASM "Disable ASM")

# All codec DLLs share these common source files.
set(CODEC_COMMON_SOURCES
    CPP/7zip/Compress/CodecExports.cpp
    CPP/7zip/Compress/DllExportsCompress.cpp
    C/Alloc.c
    C/Threads.c
    CPP/7zip/Common/StreamUtils.cpp
    CPP/Windows/System.cpp
)

set(CODEC_COMMON_INCLUDE_DIRS
    ${CMAKE_CURRENT_SOURCE_DIR}/CPP
    ${CMAKE_CURRENT_SOURCE_DIR}/C
)

if(WIN32)
    set(CODEC_DEF_FILE CPP/7zip/Compress/Codec.def)
else()
    set(CODEC_DEF_FILE "")
endif()

# Common compile definitions for every codec DLL.
set(CODEC_COMMON_DEFS Z7_EXTERNAL_CODECS)
if(WIN32)
    list(APPEND CODEC_COMMON_DEFS UNICODE _UNICODE)
endif()

# Helper: creates one codec shared library target.
#   name        -> target name and output file base name (e.g. zstd)
#   codec_sources -> extra C/C++ sources for this codec
#   extra_defs  -> extra compile definitions
#   extra_includes -> extra include directories
function(add_codec_dll name codec_sources extra_defs extra_includes)
    add_library(${name} SHARED
        CPP/7zip/Bundles/Codec_${name}/StdAfx.cpp
        ${CODEC_COMMON_SOURCES}
        ${codec_sources}
    )

    if(CODEC_DEF_FILE)
        target_sources(${name} PRIVATE ${CODEC_DEF_FILE})
    endif()

    target_include_directories(${name} PRIVATE
        ${CODEC_COMMON_INCLUDE_DIRS}
        ${extra_includes}
    )

    target_compile_definitions(${name} PRIVATE ${CODEC_COMMON_DEFS} ${extra_defs})

    if(WIN32)
        set_target_properties(${name} PROPERTIES
            OUTPUT_NAME ${name}
            PREFIX ""
        )
    else()
        set_target_properties(${name} PROPERTIES
            OUTPUT_NAME ${name}
            PREFIX ""
        )
    endif()

    if(NOT MSVC)
        target_compile_options(${name} PRIVATE -fvisibility=hidden)
    endif()
endfunction()

# ---------------------------------------------------------------------------
# Codecs that have no corresponding archive handler (format) are built as
# standalone codec DLLs and placed in bin/codecs.
#
# Codecs that DO have an archive handler (zstd, brotli, lz4, lz5, lizard)
# are built only as format DLLs (see below).  The format DLL already exports
# the codec entry points (GetNumberOfMethods / GetMethodProperty /
# CreateDecoder / CreateEncoder) together with the format handler entry
# points (CreateObject / GetNumberOfFormats / GetHandlerProperty2), so a
# single DLL serves both purposes -- exactly how 7-Zip-zstd ships them.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# flzma2.dll (Fast LZMA2) -- codec only, no archive handler
# ---------------------------------------------------------------------------
file(GLOB FLZMA2_C_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/C/fast-lzma2/*.c")
add_codec_dll(flzma2
    "CPP/7zip/Compress/Lzma2Decoder.cpp;CPP/7zip/Compress/Lzma2Encoder.cpp;CPP/7zip/Compress/LzmaDecoder.cpp;CPP/7zip/Compress/LzmaEncoder.cpp;CPP/7zip/Compress/FastLzma2Register.cpp;C/7zStream.c;C/CpuArch.c;C/LzFind.c;C/LzFindMt.c;C/LzFindOpt.c;C/Lzma2Dec.c;C/Lzma2DecMt.c;C/Lzma2Enc.c;C/LzmaDec.c;C/LzmaEnc.c;C/MtCoder.c;C/MtDec.c;CPP/7zip/Common/CWrappers.cpp;${FLZMA2_C_SOURCES}"
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
# These DLLs combine the codec implementation with the archive handler in a
# single module.  Each exports both the codec entry points
# (GetNumberOfMethods / GetMethodProperty / CreateDecoder / CreateEncoder)
# and the format handler entry points (CreateObject / GetNumberOfFormats /
# GetHandlerProperty2), so one DLL serves both roles.

# Source globs shared with the (now removed) standalone codec targets.
file(GLOB ZSTD_C_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/C/zstd/*.c")
file(GLOB BROTLI_C_SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/C/brotli/*.c")

set(FORMAT_COMMON_SOURCES
    # Archive exports / entry points
    CPP/7zip/Archive/ArchiveExports.cpp
    CPP/7zip/Archive/DllExports2.cpp
    CPP/7zip/Compress/CodecExports.cpp
    CPP/7zip/Compress/CopyCoder.cpp

    # 7zip common
    CPP/7zip/Common/CreateCoder.cpp
    CPP/7zip/Common/CWrappers.cpp
    CPP/7zip/Common/InBuffer.cpp
    CPP/7zip/Common/InOutTempBuffer.cpp
    CPP/7zip/Common/FilterCoder.cpp
    CPP/7zip/Common/LimitedStreams.cpp
    CPP/7zip/Common/LockedStream.cpp
    CPP/7zip/Common/MemBlocks.cpp
    CPP/7zip/Common/MethodId.cpp
    CPP/7zip/Common/MethodProps.cpp
    CPP/7zip/Common/OffsetStream.cpp
    CPP/7zip/Common/OutBuffer.cpp
    CPP/7zip/Common/OutMemStream.cpp
    CPP/7zip/Common/ProgressMt.cpp
    CPP/7zip/Common/ProgressUtils.cpp
    CPP/7zip/Common/PropId.cpp
    CPP/7zip/Common/StreamBinder.cpp
    CPP/7zip/Common/StreamObjects.cpp
    CPP/7zip/Common/StreamUtils.cpp
    CPP/7zip/Common/UniqBlocks.cpp
    CPP/7zip/Common/VirtThread.cpp

    # Archive common
    CPP/7zip/Archive/Common/CoderMixer2.cpp
    CPP/7zip/Archive/Common/DummyOutStream.cpp
    CPP/7zip/Archive/Common/FindSignature.cpp
    CPP/7zip/Archive/Common/HandlerOut.cpp
    CPP/7zip/Archive/Common/InStreamWithCRC.cpp
    CPP/7zip/Archive/Common/ItemNameUtils.cpp
    CPP/7zip/Archive/Common/MultiStream.cpp
    CPP/7zip/Archive/Common/OutStreamWithCRC.cpp
    CPP/7zip/Archive/Common/OutStreamWithSha1.cpp
    CPP/7zip/Archive/Common/ParseProperties.cpp

    # CPP common
    CPP/Common/CRC.cpp
    CPP/Common/CrcReg.cpp
    CPP/Common/DynLimBuf.cpp
    CPP/Common/IntToString.cpp
    CPP/Common/LzFindPrepare.cpp
    CPP/Common/MyMap.cpp
    CPP/Common/MyString.cpp
    CPP/Common/MyVector.cpp
    CPP/Common/MyXml.cpp
    CPP/Common/NewHandler.cpp
    CPP/Common/Sha1Reg.cpp
    CPP/Common/Sha256Reg.cpp
    CPP/Common/Sha3Reg.cpp
    CPP/Common/Sha512Reg.cpp
    CPP/Common/Sha512Prepare.cpp
    CPP/Common/StringConvert.cpp
    CPP/Common/StringToInt.cpp
    CPP/Common/UTFConvert.cpp
    CPP/Common/Wildcard.cpp
    CPP/Common/XzCrc64Init.cpp
    CPP/Common/XzCrc64Reg.cpp

    # Windows
    CPP/Common/MyWindows.cpp
    CPP/Windows/FileDir.cpp
    CPP/Windows/FileFind.cpp
    CPP/Windows/FileIO.cpp
    CPP/Windows/FileName.cpp
    CPP/Windows/PropVariant.cpp
    CPP/Windows/PropVariantConv.cpp
    CPP/Windows/PropVariantUtils.cpp
    CPP/Windows/Synchronization.cpp
    CPP/Windows/System.cpp
    CPP/Windows/TimeUtils.cpp

    # C sources
    C/7zBuf2.c
    C/7zCrc.c
    C/7zCrcOpt.c
    C/7zStream.c
    C/Alloc.c
    C/CpuArch.c
    C/LzFind.c
    C/Md5.c
    C/Sha1.c
    C/Sha1Opt.c
    C/Sha256.c
    C/Sha256Opt.c
    C/Sha3.c
    C/Sha512.c
    C/Sha512Opt.c
    C/Threads.c
    C/XzCrc64.c
    C/XzCrc64Opt.c
)

set(FORMAT_COMMON_INCLUDE_DIRS
    ${CMAKE_CURRENT_SOURCE_DIR}/CPP
    ${CMAKE_CURRENT_SOURCE_DIR}/C
)

if(WIN32)
    set(FORMAT_DEF_FILE CPP/7zip/Archive/Archive2.def)
else()
    set(FORMAT_DEF_FILE "")
endif()

set(FORMAT_COMMON_DEFS Z7_EXTERNAL_CODECS)
if(WIN32)
    list(APPEND FORMAT_COMMON_DEFS UNICODE _UNICODE)
endif()

# Helper: creates one external archive handler (format) shared library target.
#   name           -> target name (output file is ${name}.dll)
#   handler_source -> the *Handler.cpp file that registers the format
#   codec_sources  -> codec C/C++ sources bundled into the format DLL
#   extra_defs     -> extra compile definitions
#   extra_includes -> extra include directories
function(add_format_dll name handler_source codec_sources extra_defs extra_includes)
    add_library(fmt_${name} SHARED
        ${FORMAT_COMMON_SOURCES}
        ${handler_source}
        ${codec_sources}
    )

    if(FORMAT_DEF_FILE)
        target_sources(fmt_${name} PRIVATE ${FORMAT_DEF_FILE})
    endif()

    target_include_directories(fmt_${name} PRIVATE
        ${FORMAT_COMMON_INCLUDE_DIRS}
        ${extra_includes}
    )

    target_compile_definitions(fmt_${name} PRIVATE ${FORMAT_COMMON_DEFS} ${extra_defs})

    set_target_properties(fmt_${name} PROPERTIES
        OUTPUT_NAME ${name}
        PREFIX ""
    )

    if(NOT MSVC)
        target_compile_options(fmt_${name} PRIVATE -fvisibility=hidden)
    endif()
endfunction()

# ---------------------------------------------------------------------------
# zstd format DLL  (zst / zstd / tzst / tzstd)
# ---------------------------------------------------------------------------
add_format_dll(zstd
    "CPP/7zip/Archive/ZstdHandler.cpp"
    "CPP/7zip/Compress/ZstdDecoder.cpp;CPP/7zip/Compress/ZstdEncoder.cpp;CPP/7zip/Compress/ZstdRegister.cpp;${ZSTD_C_SOURCES};C/hashes/xxhash.c;C/zstdmt/zstd-mt_threading.c"
    "ZSTD_LEGACY_SUPPORT;ZSTD_MULTITHREAD"
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
    ""
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

# Provide a config file so consumers can locate the codec directory.
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
