import argparse
import importlib.resources
import io
import os
import stat
import zipapp
from pathlib import Path

from pdm.cli.commands.base import BaseCommand
from pdm.exceptions import PdmUsageError
from pdm.project import Project

from .env import PackEnvironment


class PackCommand(BaseCommand):
    """Pack the packages into a zipapp"""

    name = "pack"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-m", "--main", help="Specify the console script entry point for the zipapp"
        )
        parser.add_argument(
            "-o",
            "--output",
            help="Specify the output filename, default: the project name",
            type=Path,
        )
        parser.add_argument(
            "-c",
            "--compress",
            action="store_true",
            help="Compress files with the deflate method, no compress by default",
        )
        parser.add_argument(
            "--pyc",
            "--compile",
            dest="compile",
            action="store_true",
            help="Compile source into pyc files",
        )
        parser.add_argument(
            "--no-py",
            action="store_true",
            help="Remove the .py files in favor of .pyc files",
        )
        parser.add_argument(
            "-i",
            "--interpreter",
            help="The Python interpreter path, default: the project interpreter",
        )
        parser.add_argument(
            "--exe",
            action="store_true",
            help="Create an executable file. If the output file isn't given, "
            "the file name will end with .exe(Windows) or no suffix(Posix)",
        )

    @staticmethod
    def _write_zipapp(
        stream: io.BytesIO, project: Project, options: argparse.Namespace
    ) -> Path:
        bytes = stream.getvalue()
        if options.exe and (
            os.name == "nt" or (os.name == "java" and os._name == "nt")
        ):
            interpreter = options.interpreter or project.python.executable
            bits = "32" if project.python.is_32bit else "64"
            kind = "w" if "pythonw" in Path(interpreter).name else "t"
            launcher = importlib.resources.read_binary("distlib", f"{kind}{bits}.exe")
            bytes = launcher + bytes

        if options.output:
            output = options.output
        else:
            name = project.name or project.root.name
            name = name.replace("-", "_")
            suffix = ".pyz" if not options.exe else ".exe" if os.name == "nt" else ""
            output = Path(name + suffix)

        output.write_bytes(bytes)
        if options.exe:
            output.chmod(output.stat().st_mode | stat.S_IEXEC)
        return output

    def handle(self, project: Project, options: argparse.Namespace) -> None:
        def file_filter(name: str) -> bool:
            path = Path(name)
            last = path.name
            return not (
                "__pycache__" in path.parts
                or options.no_py
                and last.endswith(".py")
                or not options.compile
                and last.endswith(".pyc")
            )

        main = None
        if options.no_py and not options.compile:
            raise PdmUsageError("--no-py must be used with --pyc/--compile")
        if options.main:
            main = options.main
        else:
            scripts = project.pyproject.metadata.get("scripts", {})
            if scripts:
                main = str(scripts[next(iter(scripts))])

        target_stream = io.BytesIO()

        with PackEnvironment(project) as pack_env:
            project.core.ui.echo("Packing packages...")
            lib = pack_env.prepare_lib_for_pack(compile=options.compile)
            project.core.ui.echo(f"Packages are prepared at {lib}")
            project.core.ui.echo("Creating zipapp...")
            zipapp.create_archive(
                lib,
                target_stream,
                interpreter=options.interpreter or str(project.python.executable),
                main=main,
                compressed=options.compress,
                filter=file_filter,
            )
            output = self._write_zipapp(target_stream, project, options)
            project.core.ui.echo(f"Zipapp is generated at [green]{output}[/]")
