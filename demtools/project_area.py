from pathlib import Path


class ProjectArea(object):
    DG_INPUT_DIR_NAME = 'dg_input'
    ASP_OUTPUT_DIR_NAME = 'asp_output'

    def __init__(self, root_dir, name_prefix):
        self._root_dir = Path(root_dir)
        self.name_prefix = name_prefix
        self.__setup_project_structure()

    @property
    def root_dir(self):
        return self._root_dir

    @property
    def dg_input_dir(self):
        return self.root_dir.joinpath(self.DG_INPUT_DIR_NAME)

    @property
    def asp_output_dir(self):
        return self.root_dir.joinpath(self.ASP_OUTPUT_DIR_NAME)

    def __setup_project_structure(self):
        for directory in [self.dg_input_dir, self.asp_output_dir]:
            directory = Path(directory)
            if not directory.exists():
                directory.mkdir()
            del directory
