import pytest


@pytest.fixture(scope='module')
def tmp_input_path(tmpdir_factory):
    return tmpdir_factory.mktemp('test_input_path')
