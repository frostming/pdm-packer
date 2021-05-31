# pdm-packer

[![Tests](https://github.com/frostming/pdm-packer/workflows/Tests/badge.svg)](https://github.com/frostming/pdm-packer/actions?query=workflow%3Aci)
[![pypi version](https://img.shields.io/pypi/v/pdm-packer.svg)](https://pypi.org/project/pdm-packer/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A PDM plugin that packs your packages into a zipapp

## Requirements

pdm-packer requires Python >=3.7

## Installation

If you have installed PDM with the recommended tool `pipx`, add this plugin by:

```bash
$ pipx inject pdm pdm-packer
```

Or if you have installed PDM with `pip install --user pdm`, install with `pip` to the user site:

```bash
$ python -m pip install --user pdm-packer
```

Otherwise, install `pdm-packer` to the same place where PDM is located.

## Changlog

See [CHANGELOG.md](https://github.com/frostming/pdm-packer/blob/main/CHANGELOG.md)
