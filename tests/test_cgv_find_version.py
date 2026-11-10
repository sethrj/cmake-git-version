import re
import subprocess
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "CgvFindVersion.cmake"


def run_git(directory, *arguments):
    return subprocess.run(
        ["git", *arguments],
        cwd=directory,
        check=True,
        capture_output=True,
        text=True,
    )


def create_repository(directory):
    directory.mkdir()
    run_git(directory.parent, "init", str(directory))
    run_git(directory, "checkout", "-b", "main")
    run_git(directory, "config", "user.name", "CgvFindVersion Tests")
    run_git(directory, "config", "user.email", "cgv-tests@example.invalid")
    commit(directory, "initial")
    return directory


def commit(directory, message):
    revision_file = directory / "revision.txt"
    previous_revision = int(revision_file.read_text()) if revision_file.exists() else 0
    revision_file.write_text(f"{previous_revision + 1}\n")
    run_git(directory, "add", "revision.txt")
    run_git(directory, "commit", "--quiet", "-m", message)


def clone_repository(source, destination, shallow=False):
    arguments = ["clone", "--quiet"]
    if shallow:
        arguments.extend(["--depth=1"])
    arguments.extend([source.resolve().as_uri(), str(destination)])
    run_git(source.parent, *arguments)
    return destination


def add_tag(directory, tag, annotated=False):
    if annotated:
        run_git(directory, "tag", "--annotate", tag, "--message", tag)
    else:
        run_git(directory, "tag", tag)


def run_cmake_version(directory, *definitions):
    result = subprocess.run(
        ["cmake", *definitions, "-DSOURCE_DIR=.", "-P", str(SCRIPT_PATH)],
        cwd=directory,
        check=True,
        capture_output=True,
        text=True,
    )
    output = f"{result.stdout}\n{result.stderr}"
    version = re.search(r'^VERSION="([^"]*)"$', output, re.MULTILINE)
    version_string = re.search(r'^VERSION_STRING="([^"]*)"$', output, re.MULTILINE)
    assert version, output
    assert version_string, output
    return version.group(1), version_string.group(1)


def assert_shallow_clone(directory):
    result = run_git(directory, "rev-parse", "--is-shallow-repository")
    assert result.stdout.strip() == "true"


@pytest.mark.parametrize("annotated", [False, True], ids=["lightweight", "annotated"])
def test_deep_clone_at_tag_has_release_version(tmp_path, annotated):
    source = create_repository(tmp_path / "source")
    add_tag(source, "v1.2.3", annotated=annotated)
    clone = clone_repository(source, tmp_path / "clone")

    assert run_git(clone, "rev-parse", "--is-shallow-repository").stdout.strip() == "false"
    assert run_cmake_version(clone) == ("1.2.3", "1.2.3")


def test_deep_clone_after_tag_includes_distance_branch_and_hash(tmp_path):
    source = create_repository(tmp_path / "source")
    add_tag(source, "v1.2.3")
    commit(source, "change one")
    commit(source, "change two")
    clone = clone_repository(source, tmp_path / "clone")

    version, version_string = run_cmake_version(clone)
    assert version == "1.2.3"
    assert re.fullmatch(r"1\.2\.3-2\+main\.[0-9a-f]+", version_string)


@pytest.mark.parametrize(
    ("fallback", "expected_version"),
    [(None, "0.0.0"), ("4.5.6", "4.5.6")],
    ids=["default-version", "fallback-version"],
)
def test_deep_clone_without_tags_uses_hash_and_fallback(
    tmp_path, fallback, expected_version
):
    source = create_repository(tmp_path / "source")
    commit(source, "another commit")
    clone = clone_repository(source, tmp_path / "clone")
    definitions = [f"-DLOCAL_VERSION={fallback}"] if fallback else []

    version, version_string = run_cmake_version(clone, *definitions)
    assert version == expected_version
    assert re.fullmatch(rf"{re.escape(expected_version)}\+[0-9a-f]+", version_string)


def test_shallow_clone_with_tag_at_head_has_release_version(tmp_path):
    source = create_repository(tmp_path / "source")
    add_tag(source, "v2.3.4")
    clone = clone_repository(source, tmp_path / "clone", shallow=True)

    assert_shallow_clone(clone)
    assert run_cmake_version(clone) == ("2.3.4", "2.3.4")


def test_shallow_clone_without_tags_uses_fallback_and_hash(tmp_path):
    source = create_repository(tmp_path / "source")
    commit(source, "another commit")
    clone = clone_repository(source, tmp_path / "clone", shallow=True)

    assert_shallow_clone(clone)
    version, version_string = run_cmake_version(clone, "-DLOCAL_VERSION=5.6.7")
    assert version == "5.6.7"
    assert re.fullmatch(r"5\.6\.7\+[0-9a-f]+", version_string)


def test_shallow_clone_ignores_tag_beyond_shallow_boundary(tmp_path):
    source = create_repository(tmp_path / "source")
    add_tag(source, "v1.0.0")
    commit(source, "untagged head")
    clone = clone_repository(source, tmp_path / "clone", shallow=True)

    assert_shallow_clone(clone)
    assert run_git(clone, "tag", "--list").stdout.strip() == ""
    version, version_string = run_cmake_version(clone, "-DLOCAL_VERSION=6.7.8")
    assert version == "6.7.8"
    assert re.fullmatch(r"6\.7\.8\+[0-9a-f]+", version_string)
