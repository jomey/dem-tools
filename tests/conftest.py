import os
from pathlib import Path, PurePath

import pytest


@pytest.fixture(scope='session')
def fixture_path():
    return PurePath(__file__).with_name('fixtures')


@pytest.fixture(scope='module')
def tmp_input_path(tmpdir_factory):
    return tmpdir_factory.mktemp('test_input_path')


@pytest.fixture()
def mock_run_command(request, monkeypatch, tmpdir_factory):
    bin_dir = tmpdir_factory.mktemp('bin')
    commands = request.param
    if type(commands) is not list:
        commands = [commands]
    for command in commands:
        Path(bin_dir.join(command)).touch(mode=0o777)
    monkeypatch.setenv("PATH", str(bin_dir), prepend=os.pathsep)
