import os
import shutil
import stat
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest
from pdm.utils import cd, is_editable

from pdm_packer.env import PackEnvironment


@pytest.fixture(scope="module")
def example_project(invoke, main):
    tmp_path = Path(__file__).parent / ".testing"
    if tmp_path.exists():
        shutil.rmtree(tmp_path)
    tmp_path.mkdir()
    tmp_path.joinpath("app.py").write_text(
        "import requests\ndef main():\n    print(requests.__version__)\n"
    )
    project = main.create_project(tmp_path)
    project.pyproject.set_data(
        {
            "project": {
                "name": "test_app",
                "version": "0.1.0",
                "requires-python": ">=3.7",
                "dependencies": ["requests==2.31.0"],
            },
            "build-system": {
                "requires": ["pdm-backend"],
                "build-backend": "pdm.backend",
            },
        }
    )
    project.pyproject.write()
    invoke(["lock"], obj=project)

    return project


def test_pack_env_all_non_editable(example_project):
    with PackEnvironment(example_project) as env:
        env.prepare_lib_for_pack()
        for _, v in env.get_working_set().items():
            assert not is_editable(v)


def test_create_without_main_error(example_project, invoke):
    result = invoke(["pack"], raising=False, obj=example_project)
    assert result.exit_code != 0


def test_no_py_not_with_compile(example_project, invoke):
    result = invoke(["pack", "--no-py"], raising=False, obj=example_project)
    assert result.exit_code != 0


def test_create_normal_pyz(example_project, invoke, tmp_path):
    with cd(tmp_path):
        invoke(["pack", "-m", "app:main"], obj=example_project)
    output = tmp_path / "test_app.pyz"
    assert output.exists()
    assert f"#!{example_project.python.executable}".encode() in output.read_bytes()

    with zipfile.ZipFile(output) as zf:
        namelist = zf.namelist()
        assert "requests/__init__.py" in namelist
        assert "urllib3/__init__.py" in namelist
        assert "requests-2.31.0.dist-info/METADATA" in namelist
        assert "app.py" in namelist
        assert not any(name.endswith(".pyc") for name in namelist)

        main = [
            line.decode().rstrip()
            for line in zf.open("__main__.py")
            if not line.startswith(b"#")
        ]
        assert main == ["import app", "app.main()"]

    subprocess.check_call([sys.executable, str(output)])


def test_create_pyz_with_pyc(example_project, invoke, tmp_path):
    with cd(tmp_path):
        invoke(["pack", "-v", "-m", "app:main", "--compile"], obj=example_project)
    output = tmp_path / "test_app.pyz"
    assert output.exists()

    with zipfile.ZipFile(output) as zf:
        namelist = zf.namelist()
        assert "app.pyc" in namelist
        assert "requests/__init__.pyc" in namelist
        assert "requests/__init__.py" in namelist
        assert "urllib3/__init__.pyc" in namelist


def test_create_pyz_without_py(example_project, invoke, tmp_path):
    with cd(tmp_path):
        invoke(
            ["pack", "-v", "-m", "app:main", "--compile", "--no-py"],
            obj=example_project,
        )
    output = tmp_path / "test_app.pyz"
    assert output.exists()

    with zipfile.ZipFile(output) as zf:
        namelist = zf.namelist()
        assert "app.pyc" in namelist
        assert "requests/__init__.pyc" in namelist
        assert "requests/__init__.py" not in namelist
        assert "urllib3/__init__.pyc" in namelist


def test_pack_respect_console_script(example_project, invoke, tmp_path):
    example_project.pyproject.metadata["scripts"] = {"app": "app:main"}
    example_project.pyproject.write()
    with cd(tmp_path):
        invoke(["pack"], obj=example_project)
    output = tmp_path / "test_app.pyz"
    assert output.exists()

    with zipfile.ZipFile(output) as zf:
        main = [
            line.decode().rstrip()
            for line in zf.open("__main__.py")
            if not line.startswith(b"#")
        ]
        assert main == ["import app", "app.main()"]

    subprocess.check_call([sys.executable, str(output)])


def test_pack_change_output_file(example_project, invoke, tmp_path):
    output = tmp_path / "foo.pyz"
    invoke(["pack", "-m", "app:main", "-o", str(output)], obj=example_project)

    assert output.exists()
    subprocess.check_call([sys.executable, str(output)])


def test_pack_create_exe_file(example_project, invoke, tmp_path):
    with cd(tmp_path):
        invoke(["pack", "-m", "app:main", "--exe"], obj=example_project)
    output = tmp_path / ("test_app.exe" if os.name == "nt" else "test_app")
    assert output.exists()
    assert output.stat().st_mode & stat.S_IEXEC

    subprocess.check_call([str(output)])
