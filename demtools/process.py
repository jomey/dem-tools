import os
from contextlib import contextmanager
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT, CalledProcessError


class Process(object):
    LOG_FILE_SUFFIX = '.log'

    def __init__(self, **kwargs):
        self._run_command = kwargs.get('run_command')
        self.run_options = kwargs.get('run_options', [])
        self.log_directory = kwargs.get('log_directory', None)

    @property
    def run_command(self):
        if self._run_command is None:
            raise NotImplementedError(
                'Need to specify the run command or define in inherited class'
            )
        else:
            return self._run_command

    @property
    def run_options(self):
        return self._run_options

    @run_options.setter
    def run_options(self, value):
        if type(value) is not list:
            raise AttributeError("run options must be a list")
        else:
            self._run_options = value

    @property
    def run_call(self, verbose=False):
        run_call = [self.run_command] + self.run_options

        if verbose:
            print("Executing: " + str(' '.join(run_call)))

        return run_call

    @property
    def log_file(self):
        return self.log_directory.joinpath(
            self.run_command + self.LOG_FILE_SUFFIX
        )

    @property
    def log_directory(self):
        return self._log_directory

    @log_directory.setter
    def log_directory(self, value):
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

    def run(self, verbose=False, shell=False):
        with Popen(self.run_call,
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
