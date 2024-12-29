set(PYBIND11_FINDPYTHON ON)

find_package(7zip CONFIG REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
find_package(unofficial-bit7z CONFIG REQUIRED)

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

if(NOT VCPKG_TARGET_ARCHITECTURE MATCHES [[86]])
  set(bit7z_suffix 64)
endif()

target_link_libraries(${target_name_internal}
                      PUBLIC 7zip::7zip unofficial::bit7z::bit7z${bit7z_suffix})

# The main target only contains main logits. Here it is recommended to put the
# parts that need to be verified and tested in the target target_name_internal
set(target_name _core)

pybind11_add_module(${target_name} MODULE src/pybind.cpp)
warn_target(${target_name})
harden_target(${target_name})
sanitize_target(${target_name})

target_link_libraries(${target_name} PRIVATE ${target_name_internal})

add_custom_command(
  TARGET ${target_name}
  POST_BUILD
  COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_FILE:7zip::7zip>
          $<TARGET_FILE_DIR:${target_name}>
  COMMENT "Sync 7zip runtime library to build path.")

install(
  IMPORTED_RUNTIME_ARTIFACTS
  7zip::7zip
  RUNTIME_DEPENDENCY_SET
  plugins_runtime
  DESTINATION
  ${SKBUILD_PROJECT_NAME}
  COMPONENT
  Runtime)

install(TARGETS ${target_name} DESTINATION ${SKBUILD_PROJECT_NAME})

install_dependency(TARGETS ${target_name} DEPENDS_DESTINATION
                   ${SKBUILD_PROJECT_NAME})

if(BUILD_TESTING)
  add_test_subdirectory(tests)
endif()
