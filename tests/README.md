# Tests

The tests require Python 3, CMake, and Git on `PATH`. They create temporary Git
repositories and clones; the working checkout is not modified.

## With uv

From the repository root:

```console
uv venv
uv pip install --python .venv/bin/python -r tests/requirements.txt
uv run --python .venv/bin/python -m pytest -q tests
```

## With Python's venv

From the repository root:

```console
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r tests/requirements.txt
python -m pytest -q tests
```

## Example CMake project

Configure the example from the repository root:

```console
cmake -S example -B build/cgv-example
```

The example includes the root `CgvFindVersion.cmake` directly, so it reports
version metadata for this repository checkout.
