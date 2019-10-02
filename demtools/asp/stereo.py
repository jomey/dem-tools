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
    MAP_PROJECT_OPTIONS = ["-t {0.map_projected}", '--alignment-method None']
    MAP_PROJECTED_SESSION_TYPES = ['dgmaprpc', 'rpcmaprpc', 'astermaprpc']
    STEREO_ALGORITHM_OPTION = "--stereo-algorithm {0}"

    RUN_OPTIONS_FILTER = re.compile(r"(?:-{1,2})([\w-]+)\s+(-?[\w\s]*)")
    STEREO_ALGORITHM_BLACKLIST = ['stereo-algorithm']
    MAP_PROJECTED_BLACKLIST = ['t', 'alignment-method']

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
        self.filter_run_options(self.STEREO_ALGORITHM_BLACKLIST)

    @property
    def map_projected(self):
        return self._map_projected

    @map_projected.setter
    def map_projected(self, value):
        if value in self.MAP_PROJECTED_SESSION_TYPES:
            self._map_projected = value
            self.filter_run_options(self.MAP_PROJECTED_BLACKLIST)
        else:
            self._map_projected = None

    def in_option_blacklist(self, option, blacklist):
        match = self.RUN_OPTIONS_FILTER.match(option)
        return match[1] in blacklist

    def filter_run_options(self, blacklist):
        self.run_options = [
            option for option in self._run_options
            if not self.in_option_blacklist(option, blacklist)
        ]

    def stereo_run_options(self):
        run_options = [
            self.STEREO_ALGORITHM_OPTION.format(self.algorithm),
            self.NO_DATA_VALUE,
        ]

        if self.map_projected:
            map_options = self.MAP_PROJECT_OPTIONS.copy()
            map_options[0] = map_options[0].format(self)
            run_options.extend(map_options)

        return run_options

    def run_call(self, verbose=False):
        self.run_options = self.stereo_run_options() + self.run_options

        return super().run_call(verbose)
