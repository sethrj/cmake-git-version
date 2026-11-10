# Tests

The test require Python 3.12 or newer, CMake, and Git on `PATH`. They create
temporary Git repositories and clones; the working checkout is not modified.

## With uv

From the repository root:

```console
uv venv --python 3.12
uv pip install --python .venv/bin/python -r test/requirements.txt
uv run --python .venv/bin/python -m pytest -q test
```

## With Python's venv

From the repository root:

```console
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r test/requirements.txt
python -m pytest -q test
```

## Example CMake project

Configure the example from the repository root:

```console
cmake -S example -B build/cgv-example
```

The example includes the root `CgvFindVersion.cmake` directly, so it reports
version metadata for this repository checkout.
