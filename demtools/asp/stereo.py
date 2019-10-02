import re

from demtools import Process


class Stereo(Process):
    ALGORITHMS = {
        'Local': 0,     # Local Search Window
        'SGM': 1,       # Semi-Global Matching
        'SSGM': 2,      # Smooth Semi-Global Matching
        'MGM': 3,       # More Global Matching
    }

    NO_DATA_VALUE = "--nodata-value -32768"
    MAP_PROJECT_OPTIONS = ['-t dgmaprpc', '--alignment-method None']
    STEREO_ALGORITHM_OPTION = "--stereo-algorithm {0}"

    RUN_OPTIONS_FILTER = re.compile(r"(?:-{1,2})([\w-]+)\s+(-?[\w\s]*)")
    RUN_OPTION_BLACKLIST = [
        't', 'alignment-method', 'stereo-algorithm'
    ]

    RUN_COMMAND = 'stereo'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.algorithm = kwargs.get('algorithm', 'Local')
        self.map_projected = kwargs.get('map_projected', False)

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        if value in self.ALGORITHMS.keys():
            self._algorithm = self.ALGORITHMS[value]
        elif int(value) in self.ALGORITHMS.values():
            self._algorithm = int(value)
        else:
            raise AttributeError("Invalid value given for algorithm.")

    @property
    def map_projected(self):
        return self._map_projected

    @map_projected.setter
    def map_projected(self, value):
        self._map_projected = value

    def in_option_blacklist(self, option):
        match = self.RUN_OPTIONS_FILTER.match(option)
        return match[1] in self.RUN_OPTION_BLACKLIST

    def filter_run_options(self):
        self.run_options = [
            option for option in self._run_options
            if not self.in_option_blacklist(option)
        ]

    def stereo_run_options(self):
        run_options = [
            self.STEREO_ALGORITHM_OPTION.format(self.algorithm),
            self.NO_DATA_VALUE,
        ]

        if self.map_projected:
            run_options.extend(self.MAP_PROJECT_OPTIONS)

        return run_options

    def run_call(self, verbose=False):
        self.filter_run_options()
        self.run_options = self.stereo_run_options() + self.run_options

        return super().run_call(verbose)
