import pytest

from demtools import ProjectArea


@pytest.fixture(scope='module')
def project_name_prefix():
    return 'test_area_001'


@pytest.fixture(scope='module')
def subject(tmp_input_path, project_name_prefix):
    return ProjectArea(tmp_input_path, project_name_prefix)


class TestProjectArea(object):
    def test_path_exists(self, subject, tmp_input_path):
        assert subject.root_dir == tmp_input_path

    def test_project_prefix_name(self, subject, project_name_prefix):
        assert subject.name_prefix == project_name_prefix

    def test_dg_output_dir(self, subject):
        assert subject.input_dir.name == ProjectArea.INPUT_DIR_NAME
        assert subject.input_dir.exists()

    def test_asp_output_dir(self, subject):
        assert subject.output_dir.name == ProjectArea.OUTPUT_DIR_NAME
        assert subject.output_dir.exists()
