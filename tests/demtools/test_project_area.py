import pytest

from demtools import ProjectArea


@pytest.fixture(scope='module')
def project_name_prefix():
    return 'test_area_001'


@pytest.fixture(scope='module')
def subject(tmp_input_path, project_name_prefix):
    return ProjectArea(tmp_input_path, name_prefix=project_name_prefix)


class TestProjectArea(object):
    def test_path_exists(self, subject, tmp_input_path):
        assert subject.root_dir == tmp_input_path

    def test_project_prefix_name(self, subject, project_name_prefix):
        assert subject.name_prefix == project_name_prefix

    def test_add_folder(self, subject):
        new_folder = subject.add_folder('new_folder')
        assert new_folder.exists()
