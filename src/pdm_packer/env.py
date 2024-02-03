from __future__ import annotations

import importlib.resources
import subprocess
import sys
from functools import cached_property
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from pdm.cli.actions import resolve_candidates_from_lockfile
from pdm.project import Project

try:
    from pdm.environments import PythonLocalEnvironment as BaseEnvironment
except ImportError:
    from pdm.models.environment import Environment as BaseEnvironment


def get_in_process_script():
    if sys.version_info >= (3, 9):
        script = importlib.resources.files("pdm_packer") / "_compile_source.py"
        return importlib.resources.as_file(script)
    else:
        return importlib.resources.path("pdm_packer", "_compile_source.py")


class PackEnvironment(BaseEnvironment):
    def __init__(self, project: Project) -> None:
        super().__init__(project)
        self._dir = TemporaryDirectory(prefix="pdm-pack-")

    @cached_property
    def packages_path(self) -> Path:
        return Path(self._dir.name)

    def __enter__(self) -> PackEnvironment:
        return self

    def __exit__(self, *args: Any) -> None:
        self._dir.cleanup()

    def _compile_to_pyc(self, dest: Path) -> None:
        with get_in_process_script() as scriptpath:
            args = [str(self.interpreter.path), str(scriptpath), str(dest)]
            subprocess.check_output(args, stderr=subprocess.STDOUT)

    def prepare_lib_for_pack(self, compile: bool = False) -> Path:
        """Get a lib path containing all dependencies for pack.
        Editable packages will be replaced by non-editable ones.
        """
        project = self.project
        this_paths = self.get_paths()
        requirements = project.get_dependencies().values()
        candidates = resolve_candidates_from_lockfile(project, requirements)
        synchronizer = project.core.synchronizer_class(
            candidates, self, install_self=bool(project.name), no_editable=True
        )
        synchronizer.synchronize()
        dest = Path(this_paths["purelib"])
        if compile:
            self._compile_to_pyc(dest)
        return dest
