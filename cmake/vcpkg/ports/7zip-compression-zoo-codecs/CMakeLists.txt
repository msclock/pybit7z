cmake_minimum_required(VERSION 3.19)

project(7zip-compression-zoo-codecs LANGUAGES C CXX)

set(ZOO_SDK "${CMAKE_CURRENT_SOURCE_DIR}/plugins/sdk")

set(CODEC_COMMON_SOURCES
    ${ZOO_SDK}/CPP/7zip/Compress/DllExportsCompress.cpp
    ${ZOO_SDK}/CPP/7zip/Compress/CodecExports.cpp
    ${ZOO_SDK}/CPP/7zip/Common/MethodId.cpp
    ${ZOO_SDK}/CPP/Common/MyVector.cpp
    ${ZOO_SDK}/CPP/Common/MyString.cpp
    ${ZOO_SDK}/CPP/Common/IntToString.cpp
    ${ZOO_SDK}/CPP/Common/NewHandler.cpp
    ${ZOO_SDK}/CPP/Common/StringConvert.cpp
    ${ZOO_SDK}/CPP/Common/UTFConvert.cpp
    ${ZOO_SDK}/CPP/Windows/PropVariant.cpp
)

set(CODEC_COMMON_INCLUDE_DIRS
    ${ZOO_SDK}
    ${ZOO_SDK}/CPP
)

set(CODEC_COMMON_DEFS Z7_EXTERNAL_CODECS)
if(WIN32)
    list(APPEND CODEC_COMMON_DEFS UNICODE _UNICODE)
endif()

if(WIN32)
    set(CODEC_DEF_FILE "${CMAKE_CURRENT_BINARY_DIR}/Codec.def")
    file(WRITE "${CODEC_DEF_FILE}"
"EXPORTS
  CreateObject PRIVATE
  GetNumberOfMethods PRIVATE
  GetMethodProperty PRIVATE
  CreateDecoder PRIVATE
  CreateEncoder PRIVATE
  CreateCoder PRIVATE
  GetModuleProp PRIVATE
")
else()
    set(CODEC_DEF_FILE "")
endif()

function(add_codec_dll name codec_sources extra_defs extra_includes)
    add_library(${name} SHARED
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

    set_target_properties(${name} PROPERTIES
        OUTPUT_NAME ${name}
        PREFIX ""
    )

    if(NOT MSVC)
        target_compile_options(${name} PRIVATE -fvisibility=hidden)
    endif()

    if(WIN32)
        target_link_libraries(${name} PRIVATE oleaut32 uuid)
    endif()
endfunction()

# ---------------------------------------------------------------------------
# bsc.dll
# ---------------------------------------------------------------------------
set(BSC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/plugins/bsc")
set(BSC_UPSTREAM "${BSC_DIR}/upstream/libbsc")
add_codec_dll(bsc
    "${BSC_DIR}/src/BscCoder.cpp;${BSC_DIR}/src/Register.cpp;${BSC_UPSTREAM}/adler32/adler32.cpp;${BSC_UPSTREAM}/bwt/bwt.cpp;${BSC_UPSTREAM}/coder/coder.cpp;${BSC_UPSTREAM}/coder/qlfc/qlfc.cpp;${BSC_UPSTREAM}/coder/qlfc/qlfc_model.cpp;${BSC_UPSTREAM}/filters/detectors.cpp;${BSC_UPSTREAM}/filters/preprocessing.cpp;${BSC_UPSTREAM}/libbsc/libbsc.cpp;${BSC_UPSTREAM}/lzp/lzp.cpp;${BSC_UPSTREAM}/platform/platform.cpp;${BSC_UPSTREAM}/st/st.cpp;${BSC_UPSTREAM}/bwt/libsais/libsais.c"
    "LIBBSC_SORT_TRANSFORM_SUPPORT;LIBBSC_ALLOW_UNALIGNED_ACCESS;LIBBSC_PLATFORM_HEADERS=1"
    "${BSC_DIR}/upstream;${BSC_UPSTREAM}"
)

# ---------------------------------------------------------------------------
# zpaq.dll
# ---------------------------------------------------------------------------
set(ZPAQ_DIR "${CMAKE_CURRENT_SOURCE_DIR}/plugins/zpaq")
add_codec_dll(zpaq
    "${ZPAQ_DIR}/src/ZpaqCoder.cpp;${ZPAQ_DIR}/src/Register.cpp;${ZPAQ_DIR}/upstream/libzpaq.cpp"
    ""
    "${ZPAQ_DIR}/upstream"
)
if(MSVC)
    target_compile_options(zpaq PRIVATE /wd4305 /wd4244 /wd4267 /wd4996)
endif()

# ---------------------------------------------------------------------------
# Install all codec binaries into bin/codecs
# ---------------------------------------------------------------------------
set(CODEC_TARGETS bsc zpaq)

install(
    TARGETS ${CODEC_TARGETS}
    RUNTIME DESTINATION bin/codecs
    LIBRARY DESTINATION bin/codecs
)

include(CMakePackageConfigHelpers)
configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/7zip-compression-zoo-codecs-config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/7zip-compression-zoo-codecs-config.cmake"
    @ONLY
)
install(
    FILES "${CMAKE_CURRENT_BINARY_DIR}/7zip-compression-zoo-codecs-config.cmake"
    DESTINATION "share/7zip-compression-zoo-codecs"
)
