
from demtools.asp import Stereo


class StereoSGM(Stereo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.algorithm = kwargs.get('algorithm', 'SGM')
        self._parallel = kwargs.get('parallel', False)
        self.processes = kwargs.get('processes', None)

    @property
    def processes(self):
        return self._processes

    @processes.setter
    def processes(self, value):
        if self._parallel and value is None:
            raise AttributeError("Parallel processing requested, but no "
                                 "number of processes given in options")
        else:
            self._processes = value

    def parallel_run_options(self):
        return [f'--processes {self.processes}']

    def run_call(self, verbose=False):
        if self._parallel:
            self.run_command = f'parallel_{self.run_command}'

            self.run_options = self.parallel_run_options() + self.run_options

        return super().run_call(verbose=verbose)
