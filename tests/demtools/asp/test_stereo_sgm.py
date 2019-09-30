import pytest

from demtools.asp import StereoSGM


@pytest.mark.parametrize(
    'mock_run_command', [StereoSGM.RUN_COMMAND], indirect=True
)
@pytest.mark.usefixtures('mock_run_command')
class TestStereoSGM(object):
    def test_run(self):
        assert StereoSGM().run_command == 'parallel_stereo'

    def test_algorithm_default(self):
        assert StereoSGM().algorithm == 1
