cmake_minimum_required(VERSION 3.25)
message(STATUS "CMAKE VERSION:${CMAKE_VERSION}")

project(
  pybit7z
  LANGUAGES C CXX
  HOMEPAGE_URL "https://github.com/msclock/pybit7z"
  DESCRIPTION "A wrapper based on bit7z.")

# Project default module
find_package(cmake-modules REQUIRED)
include(cmake-modules/ProjectDefault)
include(ConfigureVersion)

add_subdirectory(src)
