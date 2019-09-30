from pathlib import Path


class ProjectArea(object):
    """
    Class to manage project/study area root folders.
    """

    def __init__(self, root_dir, **kwargs):
        self._root_dir = Path(root_dir)
        self._name_prefix = kwargs.get('name_prefix')

    @property
    def root_dir(self):
        """
        Project root directory

        :return: Path object from initialized root_dir
        """
        return self._root_dir

    @property
    def name_prefix(self):
        """
        Name prefix that can be used for created output.

        :return: String with initialized name prefix
        """
        return self._name_prefix

    def add_folder(self, name):
        """
        Method to create a folder under the root dir.
        Will check for existence first.

        :return: Path object for newly created folder
        """
        directory = self.root_dir.joinpath(name)
        if not directory.exists():
            directory.mkdir()
        return directory
