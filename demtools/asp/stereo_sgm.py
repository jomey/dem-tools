
from demtools.asp import Stereo


class StereoSGM(Stereo):
    RUN_COMMAND = 'parallel_stereo'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.algorithm = kwargs.get('algorithm', 'SGM')
