vcpkg_check_linkage(ONLY_DYNAMIC_LIBRARY)

set(VCPKG_POLICY_EMPTY_INCLUDE_FOLDER enabled)
set(VCPKG_POLICY_DLLS_WITHOUT_LIBS enabled)

vcpkg_from_github(
    OUT_SOURCE_PATH SOURCE_PATH
    REPO AlexMelanFromRingo/compression-zoo
    REF "a4edb687ce6f661577fc499305bdedcf36fced6e"
    SHA512 a97961f7abdbaaac0f2bd323f361b7b66a87bb2cb1d905b8f162f063a67a07e2baaff373a5fe644a62c6ecc816389ba0cc00d4d54157eed7fbc3acf8ce562c3f
    HEAD_REF main
)

file(COPY "${CMAKE_CURRENT_LIST_DIR}/CMakeLists.txt" DESTINATION "${SOURCE_PATH}")
file(COPY "${CMAKE_CURRENT_LIST_DIR}/7zip-compression-zoo-codecs-config.cmake.in" DESTINATION "${SOURCE_PATH}")

file(REMOVE_RECURSE
    "${SOURCE_PATH}/plugins/bsc/upstream/version"
    "${SOURCE_PATH}/plugins/bsc/upstream/VERSION"
)

# Redirect zoo codec source includes from bundled SDK to standard 7zip port headers.
# Before: #include "../../sdk/CPP/Common/ComTry.h"
# After:  #include "Common/ComTry.h"   (resolves via 7zip::7zip-codec-common INTERFACE include)
file(GLOB_RECURSE ZOO_CODEC_FILES
    "${SOURCE_PATH}/plugins/*/*.cpp"
    "${SOURCE_PATH}/plugins/*/*.h"
)
foreach(src ${ZOO_CODEC_FILES})
    file(READ "${src}" CONTENTS)
    if(CONTENTS MATCHES "#include \"../../sdk/CPP/.*\"")
        vcpkg_replace_string("${src}" "../../sdk/CPP/" "")
    endif()
endforeach()

vcpkg_cmake_configure(
    SOURCE_PATH "${SOURCE_PATH}"
)

vcpkg_cmake_install()
vcpkg_copy_pdbs()

file(INSTALL "${SOURCE_PATH}/LICENSE" DESTINATION "${CURRENT_PACKAGES_DIR}/share/${PORT}" RENAME copyright)

file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")
file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/share")
