import os
import shutil

from contextlib import contextmanager
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT, CalledProcessError


class Process(object):
    """
    Base class that can be inherited from for a specific sub command.

    Each process consists of a mandatory `run_command` that is either given
    with the initializer or set in child class as a constant.
    Examples:
        * Standalone usage:
        ::
            Process(run_command='command')

        * Class inheritance:
        ::
            class ChildProcess(Process):
                RUN_COMMAND = 'command'

    Other possible arguments:
    *run_options*: List of additional arguments given to the command
    *lod_directory*: Directory to log the output of the command to
    """
    LOG_FILE_SUFFIX = '.log'

    def __init__(self, **kwargs):
        self.run_command = \
            getattr(self, 'RUN_COMMAND', None) or kwargs.get('run_command')
        self.run_options = kwargs.get('run_options', [])
        self.log_directory = kwargs.get('log_directory', None)

    @property
    def run_command(self):
        return self._run_command

    @run_command.setter
    def run_command(self, value):
        """
        Set the command to be executed.

        Will raise an AttributeError if the command can not be found in the
        system PATH.

        :param value: command to execute
        """
        bin_path = shutil.which(value)
        if bin_path is None:
            raise AttributeError("Can't find given command in system PATH")
        else:
            self._run_command = value

    @property
    def run_options(self):
        return self._run_options

    @run_options.setter
    def run_options(self, value):
        """
        Set the options that are passed with the run command.
        Must be given as a list, e.g. ['--option1', '--option2 value']

        :param value: List of command arguments.
        """
        if type(value) is not list:
            raise AttributeError("run options must be a list")
        else:
            self._run_options = value

    @property
    def log_file(self):
        """
        Log file the output of the command will be saved to.
        Naming pattern is the run command with a '.log' suffix.

        :return: Path object with log file
        """
        return self.log_directory.joinpath(
            self.run_command + self.LOG_FILE_SUFFIX
        )

    @property
    def log_directory(self):
        return self._log_directory

    @log_directory.setter
    def log_directory(self, value):
        """
        The log directory. Setting this to None will disable logging.

        :param value: Absolute path to directory
        """
        if value is not None:
            self._log_directory = Path(value)
        else:
            self._log_directory = None

    @contextmanager
    def logger(self):
        if self.log_directory is not None:
            if not self.log_directory.exists():
                self.log_directory.mkdir()
            log_file = self.log_file
        else:
            log_file = os.devnull

        with open(log_file, "w") as log_file:
            yield log_file

    def run_call(self, verbose=False):
        """
        Get the run command with options.

        :param verbose: Print the command to stdout

        :return: List with the run command as first entry
        """
        run_call = [self.run_command] + self.run_options

        if verbose:
            print(f"Executing: {str(' '.join(run_call))}")

        return run_call

    def run(self, verbose=False, shell=False):
        """
        Execute the command with set options.
        Will raise a CalledProcessError if the return code is other than 0.

        :param verbose: Print the log to STDOUT as well
        :param shell: Execute the command as a full shell. *Use with caution*.
        :return: Return code of the command
        """
        with Popen(self.run_call(verbose),
                   stdout=PIPE, stderr=STDOUT,
                   shell=shell, bufsize=1, universal_newlines=True) as pipe:

            with self.logger() as logger:
                for line in pipe.stdout:
                    if verbose:
                        print(line)

                    logger.write(line)

            pipe.wait()  # Get the return code

            if pipe.returncode != 0:
                raise CalledProcessError(pipe.returncode, pipe.args)
            else:
                return pipe.returncode
