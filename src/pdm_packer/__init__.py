"""
    pdm-packer

    A PDM plugin that packs your packages into a zipapp
    :author: Frost Ming <mianghong@gmail.com>
    :license: MIT
"""

from pdm.core import Core

from .command import PackCommand


def plugin(core: Core) -> None:
    core.register_command(PackCommand)
