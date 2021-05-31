from __future__ import annotations

import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from pdm import Project
from pdm.models.candidates import Candidate
from pdm.models.environment import Environment
from pdm.utils import cached_property
from pip._vendor.pkg_resources import Distribution, EggInfoDistribution


def is_dist_editable(dist: Distribution) -> bool:
    return isinstance(dist, EggInfoDistribution) or getattr(dist, "editable", False)


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

    def prepare_lib_for_pack(self) -> Path:
        """Get a lib path containing all dependencies for pack.
        Editable packages will be replaced by non-editable ones.
        """
        project = self.project
        project_paths = project.environment.get_paths()
        this_paths = self.get_paths()
        for path in {project_paths["platlib"], project_paths["purelib"]}:
            shutil.copytree(path, this_paths["purelib"])

        locked_repository = project.locked_repository
        candidates: dict[str, Candidate] = {}
        install_self = False
        for k, dist in project.environment.get_working_set().items():
            if is_dist_editable(dist):
                if project.meta.name and k == project.meta.project_name:
                    install_self = True
                else:
                    candidates[k] = locked_repository.all_candidates[k]

        synchronizer = project.core.synchronizer_class(
            candidates, self, install_self=install_self, no_editable=True
        )
        synchronizer.synchronize()
        return Path(this_paths["purelib"])
