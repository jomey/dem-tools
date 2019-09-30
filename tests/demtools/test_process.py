import os
from subprocess import CalledProcessError

import pytest

from demtools import Process


class SampleProcess(Process):
    RUN_COMMAND = 'time'


@pytest.fixture(scope='module')
def run_options():
    return ['sleep', '0.03']


@pytest.fixture(scope='module')
def subject(run_options, tmp_input_path):
    return SampleProcess(run_options=run_options, log_directory=tmp_input_path)


class TestProject(object):
    def test_run_command(self, subject):
        assert subject.run_command == 'time'

    def test_invalid_run_command(self, subject):
        with pytest.raises(AttributeError, match=r'command in system PATH'):
            assert Process(run_command='foo')

    def test_command_constant_has_precedence(self, subject):
        assert SampleProcess(run_command='foo')

    def test_run_command_as_subclass(self, subject):
        assert subject.run_command == SampleProcess.RUN_COMMAND

    def test_run_options(self, subject, run_options):
        assert subject.run_options == run_options

    def test_invalid_run_options(self, subject, run_options):
        with pytest.raises(AttributeError, match=r'be a list'):
            SampleProcess(run_options='options')

    def test_run_call(self, subject, run_options):
        assert len(subject.run_call()) == \
               len([SampleProcess.RUN_COMMAND]) + len(run_options)

    def test_run_call_verbose(self, subject, capsys):
        subject.run_call(verbose=True)
        out, err = capsys.readouterr()
        assert len(out) > 0
        assert 'Executing: time' in out

    def test_log_file(self, subject, tmp_input_path):
        assert subject.log_file == \
               tmp_input_path.join(
                   SampleProcess.RUN_COMMAND + Process.LOG_FILE_SUFFIX
               )

    def test_log_directory(self, subject, tmp_input_path):
        assert subject.log_directory == tmp_input_path

    def test_logger_enabled(self, subject):
        with subject.logger() as log_file:
            assert log_file.name == str(subject.log_file)
            assert subject.log_file.exists()
            assert 10 == log_file.write('Test entry')

    def test_logger_disabled(self):
        subject = SampleProcess()
        with subject.logger() as log_file:
            assert log_file.name == os.devnull

    def test_run(self, subject):
        assert subject.run() == 0
        assert os.stat(subject.log_file).st_size > 0

    def test_run_verbose(self, subject, capsys):
        assert subject.run(verbose=True) == 0
        out, err = capsys.readouterr()
        assert len(out) > 0
        assert 'Executing: time' in out     # Verbose output of run_call()
        assert 'user' in out                # Verbose output of the call itself

    def test_failed_run(self, subject):
        subject.run_options = ['foo']

        with pytest.raises(CalledProcessError, match=r'.*time.*foo'):
            assert subject.run() != 0
