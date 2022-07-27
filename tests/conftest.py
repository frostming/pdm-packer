"""Configuration for the pytest test suite."""
import pytest
from click.testing import CliRunner
from pdm.core import Core


@pytest.fixture(scope="session")
def main() -> Core:
    return Core()


@pytest.fixture(scope="session")
def invoke(main: Core):
    runner = CliRunner(mix_stderr=False)

    def caller(args, *, raising=True, **extras):
        result = runner.invoke(
            main, args, prog_name="pdm", catch_exceptions=not raising, **extras
        )
        if result.exit_code != 0 and raising:
            raise RuntimeError(
                f"Calling command {args} failed with exit code: {result.exit_code}\n"
                f"{result.stderr}"
            )
        return result

    return caller
