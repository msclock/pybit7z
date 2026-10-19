set(PYBIND11_FINDPYTHON ON)

find_package(7zip CONFIG REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
find_package(bit7z CONFIG REQUIRED)
find_package(7zip-zstd-codecs CONFIG REQUIRED)
find_package(7zip-compression-zoo-codecs CONFIG REQUIRED)

# The internal target will not be installed and only act as requirements for
# main and tests internally
set(target_name_internal _core_internal)
set(target_name _core)

file(GLOB_RECURSE internal_srcs "src/*.cpp")
file(GLOB_RECURSE internal_hdrs "include/*.hpp")

list(FILTER internal_srcs EXCLUDE REGEX "pybind.cpp")

add_library(${target_name_internal} OBJECT)
warn_target(${target_name_internal})
harden_target(${target_name_internal})
sanitize_target(${target_name_internal})

generate_git_header(VERSION_NAMESPACE_PREFIX _core)

target_sources(${target_name_internal} PRIVATE ${internal_srcs}
                                               ${internal_hdrs})

target_include_interface_directories(
  ${target_name_internal} ${CMAKE_CURRENT_SOURCE_DIR}/include
  ${CMAKE_CURRENT_BINARY_DIR}/git_version)

get_property(
  imported_targets
  DIRECTORY
  PROPERTY IMPORTED_TARGETS)
list(FILTER imported_targets INCLUDE REGEX [[bit7z::]])

target_link_libraries(${target_name_internal} PUBLIC 7zip::7zip
                                                     ${imported_targets})

# The main target only contains main logits. Here it is recommended to put the
# parts that need to be verified and tested in the target target_name_internal
set(target_name _core)

pybind11_add_module(${target_name} MODULE src/pybind.cpp)
warn_target(${target_name})
harden_target(${target_name})
sanitize_target(${target_name})

target_link_libraries(${target_name} PRIVATE ${target_name_internal})

if(NOT WIN32)
  target_compile_options(${target_name} PRIVATE -fvisibility=hidden)
  if(NOT APPLE)
    set(PYBIND_VERSION_SCRIPT "${CMAKE_CURRENT_BINARY_DIR}/pybind.version")
    file(WRITE "${PYBIND_VERSION_SCRIPT}" "{ global: PyInit_*; local: *; };")
    target_link_options(${target_name} PRIVATE
                        "-Wl,--version-script=${PYBIND_VERSION_SCRIPT}")
  endif()
endif()

add_custom_command(
  TARGET ${target_name}
  POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_FILE:7zip::7zip>
          $<TARGET_FILE_DIR:${target_name}>
  COMMAND ${CMAKE_COMMAND} -E copy_directory "${7ZIP_ZSTD_CODECS_DIR}"
          "$<TARGET_FILE_DIR:${target_name}>/Codecs"
  COMMAND
    ${CMAKE_COMMAND} -E copy_directory "${7ZIP_COMPRESSION_ZOO_CODECS_DIR}"
    "$<TARGET_FILE_DIR:${target_name}>/Codecs"
  COMMAND ${CMAKE_COMMAND} -E copy_directory "${7ZIP_ZSTD_FORMATS_DIR}"
          "$<TARGET_FILE_DIR:${target_name}>/Formats"
  COMMENT
    "Sync 7zip runtime library external codecs and format handlers to build path."
)

install(
  IMPORTED_RUNTIME_ARTIFACTS
  7zip::7zip
  RUNTIME_DEPENDENCY_SET
  plugins_runtime
  DESTINATION
  ${CMAKE_PROJECT_NAME}
  COMPONENT
  Runtime)

install(TARGETS ${target_name} DESTINATION ${CMAKE_PROJECT_NAME})

install(
  DIRECTORY "${7ZIP_ZSTD_CODECS_DIR}/"
  DESTINATION ${CMAKE_PROJECT_NAME}/Codecs
  COMPONENT Runtime)

install(
  DIRECTORY "${7ZIP_COMPRESSION_ZOO_CODECS_DIR}/"
  DESTINATION ${CMAKE_PROJECT_NAME}/Codecs
  COMPONENT Runtime)

install(
  DIRECTORY "${7ZIP_ZSTD_FORMATS_DIR}/"
  DESTINATION ${CMAKE_PROJECT_NAME}/Formats
  COMPONENT Runtime)

install_dependency(TARGETS ${target_name} DEPENDS_DESTINATION
                   ${CMAKE_PROJECT_NAME})

if(BUILD_TESTING)
  add_test_subdirectory(tests)
endif()
