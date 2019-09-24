import os
from subprocess import CalledProcessError

import pytest

from demtools import Process


class TestProcess(Process):
    COMMAND = 'time'

    @property
    def run_command(self):
        return self.COMMAND


@pytest.fixture(scope='module')
def run_options():
    return ['sleep', '0.03']


@pytest.fixture(scope='module')
def subject(run_options, tmp_input_path):
    return TestProcess(run_options=run_options, log_directory=tmp_input_path)


class TestProject(object):
    def test_requires_implemented_run_command(self):
        with pytest.raises(NotImplementedError, match=r'inherited class'):
            Process().run_command

    def test_run_command_as_option(self):
        command = 'test'
        subject = Process(run_command=command)
        assert subject.run_command == command

    def test_run_command_as_subclass(self, subject):
        assert subject.run_command == TestProcess.COMMAND

    def test_run_options(self, subject, run_options):
        assert subject.run_options == run_options

    def test_invalid_run_options(self, subject, run_options):
        with pytest.raises(AttributeError, match=r'be a list'):
            TestProcess(run_options='options')

    def test_run_call(self, subject, run_options):
        assert len(subject.run_call) == \
               len([TestProcess.COMMAND]) + len(run_options)

    def test_log_file(self, subject, tmp_input_path):
        assert subject.log_file == \
               tmp_input_path.join(
                   TestProcess.COMMAND + Process.LOG_FILE_SUFFIX
               )

    def test_log_directory(self, subject, tmp_input_path):
        assert subject.log_directory == tmp_input_path

    def test_logger_enabled(self, subject):
        subject.verbose = True
        with subject.logger() as log_file:
            assert subject.log_file.exists()
            assert 10 == log_file.write('Test entry')

    def test_run(self, subject):
        subject.verbose = True

        assert subject.run() == 0
        assert os.stat(subject.log_file).st_size > 0

    def test_failed_run(self, subject):
        subject.run_options = ['foo']

        with pytest.raises(CalledProcessError, match=r'.*time.*foo'):
            assert subject.run() != 0
