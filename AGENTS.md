# Repository Guidance

## Project Structure

- `CgvFindVersion.cmake` is the project module and can be included by downstream CMake projects or run in script mode with `cmake -P`.
- `install.sh <project-cmake-dir>` copies the module to a consuming project's CMake directory and adds the `export-subst` rule needed for Git-archive metadata.
- `example/CMakeLists.txt` directly includes the root module and demonstrates metadata from this checkout.
- `test/` contains pytest coverage for script mode and the example project. `test/requirements.txt` lists the Python test dependency.

## CMake Interface

- Include the module and call `cgv_find_version(<ProjectName>)` before `project()` when the discovered version should initialize `project(VERSION ...)`.
- The function sets `<ProjectName>_VERSION` and `<ProjectName>_VERSION_STRING` in the caller's scope.
- Git discovery defaults to the directory containing `CgvFindVersion.cmake`. In script mode, use `-DSOURCE_DIR=<repo>` to inspect another checkout; for test running in a clone, set the process working directory to that clone and pass `-DSOURCE_DIR=.`.
- The default tag pattern accepts `v`-prefixed numeric versions and supported prerelease suffixes. Set `CGV_TAG_REGEX` before calling the function to use another tag format.
- A reachable exact tag gives a release version. Commits after a tag add commit distance and hash metadata. If no tag is available, a provided `<ProjectName>_VERSION` is used as the fallback base; otherwise the numeric version defaults to `0.0.0`.

## Testing

- Python 3, CMake, and Git must be available on `PATH`.
- From the repository root, create a virtual environment and install test requirements with either `uv` or `python3 -m venv`; detailed commands are in `test/README.md`.
- Run the full suite with `uv run --python .venv/bin/python -m pytest -q test` or `python -m pytest -q test` inside the activated environment.
- The script-mode test create temporary source repositories and clones. Shallow-clone test use `file://` clone URLs so `git clone --depth=1` is genuinely shallow. Keep generated repositories and build trees in pytest temporary directories rather than the checkout.
- Configure the example out of source with `cmake -S example -B build/cgv-example`. The example integration test also runs `cmake --build` in a temporary build directory and checks that CMake's cache is kept out of the source tree.
