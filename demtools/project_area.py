from pathlib import Path


class ProjectArea(object):
    INPUT_DIR_NAME = 'input_data'
    OUTPUT_DIR_NAME = 'output_data'

    def __init__(self, root_dir, name_prefix):
        self._root_dir = Path(root_dir)
        self.name_prefix = name_prefix
        self.__setup_project_structure()

    @property
    def root_dir(self):
        return self._root_dir

    @property
    def input_dir(self):
        return self.root_dir.joinpath(self.INPUT_DIR_NAME)

    @property
    def output_dir(self):
        return self.root_dir.joinpath(self.OUTPUT_DIR_NAME)

    def __setup_project_structure(self):
        for directory in [self.input_dir, self.output_dir]:
            directory = Path(directory)
            if not directory.exists():
                directory.mkdir()
            del directory
