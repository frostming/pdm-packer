from __future__ import annotations

import importlib.resources
import itertools
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from pdm.cli.actions import resolve_candidates_from_lockfile
from pdm.environments import PythonEnvironment
from pdm.project import Project


def get_in_process_script():
    if sys.version_info >= (3, 9):
        script = importlib.resources.files("pdm_packer") / "_compile_source.py"
        return importlib.resources.as_file(script)
    else:
        return importlib.resources.path("pdm_packer", "_compile_source.py")


IN_PROCESS_SCRIPT = Path(__file__).with_name("_compile_source.py")
PDM_VERSION = tuple(
    map(
        int,
        itertools.takewhile(str.isdigit, importlib.metadata.version("pdm").split(".")),
    )
)


class PackEnvironment(PythonEnvironment):
    def __init__(self, project: Project) -> None:
        self._dir = TemporaryDirectory(prefix="pdm-pack-")
        super().__init__(project, prefix=self._dir.name)

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
        if PDM_VERSION >= (2, 19):
            from pdm.cli.actions import resolve_from_lockfile

            packages = resolve_from_lockfile(project, requirements, groups=["default"])
            synchronizer = project.core.get_synchronizer()(
                self,
                install_self=bool(project.name),
                no_editable=True,
                packages=packages,
            )
        else:
            candidates = resolve_candidates_from_lockfile(
                project, requirements, groups=["default"]
            )
            synchronizer = project.core.synchronizer_class(
                candidates, self, install_self=bool(project.name), no_editable=True
            )
        synchronizer.synchronize()
        dest = Path(this_paths["purelib"])
        if compile:
            self._compile_to_pyc(dest)
        return dest
