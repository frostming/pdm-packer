"""Configuration for the pytest test suite."""
import pytest
from click.testing import CliRunner
from pdm import Core


@pytest.fixture(scope="session")
def main():
    return Core()


@pytest.fixture(scope="session")
def invoke(main):
    runner = CliRunner(mix_stderr=False)

    def caller(args, *, raising=True, **extras):
        result = runner.invoke(main, args, prog_name="pdm", **extras)
        if raising and result.exit_code != 0:
            raise RuntimeError(f"Call command {args} failed: {result.output}")
        return result

    return caller
