from pdm import Core

from .command import PackCommand


def entrypoint(core: Core) -> None:
    core.register_command(PackCommand)
