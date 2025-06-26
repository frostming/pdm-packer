import argparse
import json
import os
import subprocess
from pathlib import Path

import nox

PROJECT_DIR = Path(__file__).parent
os.environ["PDM_IGNORE_SAVED_PYTHON"] = "1"


@nox.session(python=("3.8", "3.9", "3.10", "3.11", "3.12"))
def test(session):
    session.run("pdm", "install", "-Gtest", external=True)
    session.run("pytest", "tests/")


def _get_current_version():
    cmd = ["git", "describe", "--tags", "--abbrev=0"]
    return subprocess.check_output(cmd).decode("utf-8").strip()


@nox.session
def release(session: nox.Session):
    session.run("pdm", "install", "-Gdev", external=True)

    args = _parse_args(session.posargs)
    bump_version_input = {
        "version": _get_current_version(),
        "pre": args.pre,
        "major": args.major,
        "minor": args.minor,
        "patch": args.patch,
    }
    new_version = session.run(
        "python", "tasks/bump_version.py", json.dumps(bump_version_input), silent=True
    ).strip()
    print(f"Bump version to: {new_version}")
    if args.dry_run:
        subprocess.check_call(
            ["towncrier", "build", "--version", new_version, "--draft"]
        )
    else:
        subprocess.check_call(["towncrier", "build", "--yes", "--version", new_version])
        subprocess.check_call(["git", "add", "."])
        if args.commit:
            subprocess.check_call(["git", "commit", "-m", f"Release {new_version}"])
            subprocess.check_call(
                ["git", "tag", "-a", new_version, "-m", f"v{new_version}"]
            )
            subprocess.check_call(["git", "push", "--follow-tags"])


def _parse_args(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument(
        "--no-commit",
        action="store_false",
        dest="commit",
        default=True,
        help="Do not commit to Git",
    )
    group = parser.add_argument_group(title="version part")
    group.add_argument("--pre", help="Pre tag")
    group.add_argument("--major", action="store_true", help="Bump major version")
    group.add_argument("--minor", action="store_true", help="Bump minor version")
    group.add_argument("--patch", action="store_true", help="Bump patch version")

    return parser.parse_args(argv)
