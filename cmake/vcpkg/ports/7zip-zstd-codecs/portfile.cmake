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

vcpkg_cmake_configure(
    SOURCE_PATH "${SOURCE_PATH}"
)

vcpkg_cmake_install()
vcpkg_copy_pdbs()

file(INSTALL "${SOURCE_PATH}/DOC/License.txt" DESTINATION "${CURRENT_PACKAGES_DIR}/share/${PORT}" RENAME copyright)

file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/share")
