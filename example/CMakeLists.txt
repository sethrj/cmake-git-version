cmake_minimum_required(VERSION 3.8)

include("${CMAKE_CURRENT_LIST_DIR}/../CgvFindVersion.cmake")
cgv_find_version(CgvFindVersionDemo)

project(CgvFindVersionDemo VERSION "${CgvFindVersionDemo_VERSION}" LANGUAGES NONE)

message(STATUS "CgvFindVersionDemo version: ${CgvFindVersionDemo_VERSION}")
message(STATUS "CgvFindVersionDemo version string: ${CgvFindVersionDemo_VERSION_STRING}")
