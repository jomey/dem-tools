import argparse
from pathlib import Path

import pytest

from demtools.scripts import InputPath


@pytest.fixture(scope='module')
def tmp_test_file(tmp_input_path):
    file = Path(tmp_input_path.join('test_input_file.txt'))
    print(str(file))
    file.touch(mode=0o644, exist_ok=True)
    return file


@pytest.fixture(scope='module')
def tmp_test_path(tmp_test_file):
    return tmp_test_file.parent


@pytest.fixture(scope='module')
def subject():
    return InputPath()


class TestInputPaths(object):
    def test_path_exists(self, subject, tmp_test_path):
        assert subject(tmp_test_path) == tmp_test_path

    def test_path_does_not_exists(self, subject):
        with pytest.raises(argparse.ArgumentTypeError, match=r'Unable to find'):
            subject('/tmp/does_not_exist')

    def test_path_not_readable(self, subject, tmp_test_path):
        tmp_test_path.chmod(000)
        with pytest.raises(
                argparse.ArgumentTypeError, match=r'not readable'
        ):
            subject(tmp_test_path)
        tmp_test_path.chmod(0o755)

    def test_file_exists(self, subject, tmp_test_file):
        assert subject(tmp_test_file) == tmp_test_file

    def test_file_does_not_exists(self, subject):
        with pytest.raises(
                argparse.ArgumentTypeError, match=r'Unable to find'
        ):
            subject('/tmp/does_not_exist.txt')

    def test_file_not_readable(self, subject, tmp_test_file):
        tmp_test_file.chmod(000)
        with pytest.raises(
                argparse.ArgumentTypeError, match=r'not readable'
        ):
            subject(tmp_test_file)
        tmp_test_file.chmod(0o755)
