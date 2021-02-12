# CMake Git Version

Seamlessly integrate git version tags into your CMake project. Inspired by
[Versioneer for Python projects]
(https://github.com/python-versioneer/python-versioneer).

This small CMake script ensures that your project's internal
version metadata is always up-to-date with Git version data, whether your
repository is cloned or exported as a source tarball.

## Installation

A tiny installation script copies the files in the `cmake` directory to your
project's CMake directory.

```console
$ ./install.sh /path/to/myproject/cmake
```

