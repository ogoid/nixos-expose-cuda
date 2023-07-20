import json
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Tuple

parser = ArgumentParser("pre-build-hook")
parser.add_argument("derivation_path")
parser.add_argument("sandbox_path", nargs="?")


def symlink_parents(p: Path) -> List[Path]:
    out = []
    while p.is_symlink() and p not in out:
        p = p.readlink()
        out.append(p)
    return out


if __name__ == "__main__":
    args = parser.parse_args()
    drv_path = args.derivation_path
    proc = subprocess.run(
        [
            "nix",
            "show-derivation",
            drv_path,
        ],
        capture_output=True,
    )
    drv = json.loads(proc.stdout)
    assert drv_path in drv

    paths: List[Path] = []

    for p in Path("/run/opengl-driver/lib").glob("lib*"):
        if p.name.startswith("libcuda") or p.name.startswith("libnvidia"):
            paths.append(p)

    for p in Path("/dev").glob("video*"):
        paths.append(p)

    for p in Path("/dev").glob("nvidia*"):
        paths.append(p)

    for p in list(paths):
        paths.extend(symlink_parents(p))

    paths = sorted(set(paths))
    binds: List[Tuple[str, str]] = [
        (p.as_posix(), p.as_posix()) for p in paths
    ]

    features = drv[drv_path].get("env", {}).get("requiredSystemFeatures", [])
    if "expose-cuda" in features:
        print("extra-sandbox-paths")  # command
        for guest_path, host_path in binds:
            print(f"{guest_path}={host_path}")  # arguments, one per line
        print()  # terminated by an empty line
