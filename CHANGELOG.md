# Changelog

<!-- insertion marker -->
[v0.8.2](https://github.com/frostming/pdm-packer/releases/tag/0.8.2) (2025-06-26)

### Features & Improvements

- Drop support of Python 3.8 and update dependencies. [#48](https://github.com/frostming/pdm-packer/issues/48)

### Bug Fixes

- Create output parent directories if they don't exist. [#47](https://github.com/frostming/pdm-packer/issues/47)

### Dependencies

- Update PDM version and pre-commit hooks. [#50](https://github.com/frostming/pdm-packer/issues/50)

### Removals and Deprecations

- Remove backward-compatibility code for PDM 2.19 and earlier. [#51](https://github.com/frostming/pdm-packer/issues/51)

### Miscellany

- Refactor the release script. [#52](https://github.com/frostming/pdm-packer/issues/52)
## [v0.8.1](https://github.com/frostming/pdm-packer/releases/tag/0.8.1) (2024-09-06)

### Bug Fixes

- Fix the wrong method used to get synchronizer for PDM 2.19+ [#44](https://github.com/frostming/pdm-packer/issues/44)

## [v0.8.0](https://github.com/frostming/pdm-packer/releases/tag/0.8.0) (2024-09-05)

### Features & Improvements

- Update to support PDM 2.19. [#0](https://github.com/frostming/pdm-packer/issues/0)

## [v0.6.1](https://github.com/frostming/pdm-packer/releases/tag/0.6.1) (2023-07-13)

### Bug Fixes

- Include dist-info files in the zipapp. [#35](https://github.com/frostming/pdm-packer/issues/35)

## [v0.6.0](https://github.com/frostming/pdm-packer/releases/tag/0.6.0) (2023-03-29)

### Features & Improvements

- Add compatible import statement for the next PDM release. [#31](https://github.com/frostming/pdm-packer/issues/31)

## [v0.5.0](https://github.com/frostming/pdm-packer/releases/tag/0.5.0) (2022-12-12)

### Bug Fixes

- Update the import paths according to the deprecation. [#20](https://github.com/frostming/pdm-packer/issues/20)
- Fix the code compatibility with `pdm 2.3.0+`. [#24](https://github.com/frostming/pdm-packer/issues/24)

## [v0.3.2](https://github.com/frostming/pdm-packer/releases/tag/0.3.2) (2022-05-13)

### Bug Fixes

- Fix a bug that the default interpreter is not a string due to API change in PDM. [#15](https://github.com/frostming/pdm-packer/issues/15)

## [v0.3.1](https://github.com/frostming/pdm-packer/releases/tag/0.3.1) (2022-04-25)

### Bug Fixes

- Fix the compatibility issue about the `get_architecture()` function. [#14](https://github.com/frostming/pdm-packer/issues/14)

## [v0.3.0](https://github.com/frostming/pdm-packer/releases/tag/0.3.0) (2022-02-15)

### Features & Improvements

- Reinstall all **default** depenencies when packing the application. [#12](https://github.com/frostming/pdm-packer/issues/12)

### Bug Fixes

- Fix the compatibility issue with the latest PDM version. [#12](https://github.com/frostming/pdm-packer/issues/12)

## [v0.2.1](https://github.com/frostming/pdm-packer/releases/tag/0.2.1) (2021-07-16)

### Features & Improvements

- Introduce `--no-py` to exclude py files in the result zipapp. [#9](https://github.com/frostming/pdm-packer/issues/9)

## [v0.2.0](https://github.com/frostming/pdm-packer/releases/tag/0.2.0) (2021-07-15)

### Features & Improvements

- Add `--pyc/--compile` to compile source files into pyc. Compiled files are placed next to the source files to be loaded by `zipimport` for speedup. [#7](https://github.com/frostming/pdm-packer/issues/7)

## [v0.1.1](https://github.com/frostming/pdm-packer/releases/tag/0.1.1) (2021-06-07)

### Features & Improvements

- File content are written into the file object instead of memory. [#4](https://github.com/frostming/pdm-packer/issues/4)
