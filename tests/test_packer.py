import os
import shutil
import stat
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest
from pdm.models.pip_shims import global_tempdir_manager
from pdm.utils import cd

from pdm_packer.env import PackEnvironment, is_dist_editable


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
    invoke(
        ["init"],
        input="\ny\ntest-app\n0.1.0\n\n\n\n>=3.6\n",
        obj=project,
    )
    invoke(["add", "requests"], obj=project)

    return project


def test_pack_env_all_non_editable(example_project):
    with global_tempdir_manager():
        with PackEnvironment(example_project) as env:
            env.prepare_lib_for_pack()
            for _, v in env.get_working_set().items():
                assert not is_dist_editable(v)


def test_create_without_main_error(example_project, invoke):
    with pytest.raises(RuntimeError):
        invoke(["pack"], obj=example_project)


def test_create_normal_pyz(example_project, invoke, tmp_path):
    with cd(tmp_path):
        invoke(["pack", "-m", "app:main"], obj=example_project)
    output = tmp_path / "test_app.pyz"
    assert output.exists()
    assert f"#!{example_project.python.executable}".encode() in output.read_bytes()

    with zipfile.ZipFile(output) as zf:
        namelist = zf.namelist()
        assert "requests/__init__.py" in namelist
        assert "chardet/__init__.py" in namelist
        assert not any(name.endswith(".pyc") for name in namelist)
        assert not any(".dist-info" in name for name in namelist)

        main = [
            line.decode().rstrip()
            for line in zf.open("__main__.py")
            if not line.startswith(b"#")
        ]
        assert main == ["import app", "app.main()"]

    subprocess.check_call([sys.executable, str(output)])


def test_pack_respect_console_script(example_project, invoke, tmp_path):
    example_project.meta["scripts"] = {"app": "app:main"}
    example_project.write_pyproject()
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