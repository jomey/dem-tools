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
    Path(bin_dir.join(request.param)).touch(mode=0o777)
    # TODO - Needed for StereoSGM test case.
    # Can't quite figure out, why mark.parametrize is not working
    # This should be improved in future revisions.
    Path(bin_dir.join(f'parallel_{request.param}')).touch(mode=0o777)
    monkeypatch.setenv("PATH", str(bin_dir), prepend=os.pathsep)
