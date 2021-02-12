# CMake Git Version

Seamlessly integrate git version tags into your CMake project. Inspired by
[Versioneer for Python projects]
(https://github.com/python-versioneer/python-versioneer).

This small CMake script ensures that your project's internal
version metadata is always up-to-date with Git version data, whether your
repository is cloned or exported as a source tarball via the GitHub release
mechanism.

## Installation

A tiny installation script copies the files in the `cmake` directory to your
project's CMake directory and configures the gitattributes file.

```console
$ ./install.sh /path/to/myproject/cmake
-- Copied script to /path/to/myproject/cmake/CgvFindVersion.cmake
-- Updated /path/to/myproject/cmake/.gitattributes
```

## Usage

Typically you will want to use the exported version metadata from CGV to inform
CMake of your project's version:

```cmake
include("${CMAKE_CURRENT_LIST_DIR}/cmake/CgvFindVersion.cmake")
cgv_find_version(MyProject)

project(MyProject VERSION "${MyProject_VERSION}" LANGUAGES CXX)
```

CMake will parse the supplied version number into major/minor/patch versions
that can be used by a `config.h.in` file:
```c++
static const char myproject_version[] = "@MyProject_VERSION_STRING@";
static const int myproject_version_major = @PROJECT_VERSION_MAJOR@;
static const int myproject_version_minor = @PROJECT_VERSION_MINOR@;
static const int myproject_version_patch = @PROJECT_VERSION_PATCH@;
```
which will let CMake generate a header file:
```cmake
configure_file("config.h.in" "MyProject_config.h" @ONLY)
```

You can test the version information by running CMake from the command line:
```console
cmake -P cmake/CgvFindVersion.cmake
```
