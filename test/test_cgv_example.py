import re
import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_SOURCE = REPOSITORY_ROOT / "example"


def test_example_configures_and_builds_out_of_source(tmp_path):
    build_dir = tmp_path / "build"
    configure = subprocess.run(
        ["cmake", "-S", str(EXAMPLE_SOURCE), "-B", str(build_dir)],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    output = f"{configure.stdout}\n{configure.stderr}"

    assert re.search(r"CgvFindVersionDemo version: \S+", output)
    assert re.search(r"CgvFindVersionDemo version string: \S+", output)

    subprocess.run(
        ["cmake", "--build", str(build_dir)],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert list(tmp_path.rglob("CMakeCache.txt")) == [build_dir / "CMakeCache.txt"]
