# Changelog

<!-- insertion marker -->
[v0.2.1](https://github.com/frostming/pdm-packer/releases/tag/0.2.1) (2021-07-16)
---------------------------------------------------------------------------------

### Features & Improvements

- Introduce `--no-py` to exclude py files in the result zipapp. [#9](https://github.com/frostming/pdm-packer/issues/9)


[v0.2.0](https://github.com/frostming/pdm-packer/releases/tag/0.2.0) (2021-07-15)
---------------------------------------------------------------------------------

### Features & Improvements

- Add `--pyc/--compile` to compile source files into pyc. Compiled files are placed next to the source files to be loaded by `zipimport` for speedup.  [#7](https://github.com/frostming/pdm-packer/issues/7)


[v0.1.1](https://github.com/frostming/pdm-packer/releases/tag/0.1.1) (2021-06-07)
---------------------------------------------------------------------------------

### Features & Improvements

- File content are written into the file object instead of memory. [#4](https://github.com/frostming/pdm-packer/issues/4)
