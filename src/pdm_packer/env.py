from __future__ import annotations

import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from pdm.cli.actions import resolve_candidates_from_lockfile
from pdm.compat import cached_property
from pdm.models.environment import Environment
from pdm.project import Project

IN_PROCESS_SCRIPT = Path(__file__).with_name("_compile_source.py")


class PackEnvironment(Environment):
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
        args = [str(self.interpreter.path), str(IN_PROCESS_SCRIPT), str(dest)]
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
