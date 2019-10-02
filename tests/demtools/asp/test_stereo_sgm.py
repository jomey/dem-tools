import pytest

from demtools.asp import StereoSGM


@pytest.mark.parametrize(
    'mock_run_command', [StereoSGM.RUN_COMMAND], indirect=True
)
@pytest.mark.usefixtures('mock_run_command')
class TestStereoSGM(object):
    def test_run(self):
        stereo_run_call = StereoSGM().run_call()
        assert stereo_run_call[0] == 'stereo'
        assert '--processes' not in stereo_run_call

    def test_algorithm_default(self):
        assert StereoSGM().algorithm == 1

    def test_run_in_parallel(self):
        stereo_run_call = StereoSGM(parallel=True, processes=4).run_call()
        assert stereo_run_call[0] == 'parallel_stereo'
        assert '--processes 4' in stereo_run_call

    def test_run_in_parallel_needs_processes(self):
        with pytest.raises(AttributeError, match=r'no number of processes'):
            assert StereoSGM(parallel=True)
