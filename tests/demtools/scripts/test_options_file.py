import argparse

import pytest

from demtools.scripts import OptionsFile


@pytest.fixture(scope='module')
def command_options_file(fixture_path):
    return str(fixture_path.joinpath('command.opts'))


@pytest.fixture(scope='module')
def subject():
    return OptionsFile()


class TestOptionsFile(object):
    def test_path_does_not_exists(self, subject):
        with pytest.raises(
                argparse.ArgumentTypeError, match=r'Unable to find'
        ):
            subject('/tmp/does_not_exist')

    def test_returns_list(self, subject, command_options_file):
        options = subject(command_options_file)
        assert type(options) == list
        assert len(options) == 5
        assert '--first 1' in options
        assert '--third 3 3' in options
