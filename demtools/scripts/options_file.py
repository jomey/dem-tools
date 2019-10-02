from .input_path import InputPath


class OptionsFile(InputPath):
    """
    Class to use with argparse 'type' option.
    When set as a 'type'f for an ArgumentParser argument, the given option
    will parse the file, given as the value, line by line and return the result
    as a list.

    Example:
        argument_parser = argparse.ArgumentParser()
        argument_parser.add_argument(
            '--my-opts',
            type=OptionsFile(),
        )
    """
    @staticmethod
    def parse_options(input_path):
        """
        Parse given file line by line.

        :param input_path: Path to file
        :return: List with line entries of the input file
        """
        with open(input_path) as options_file:
            return [line.rstrip() for line in list(options_file)]

    def __call__(self, options_file):
        options_file = super().__call__(options_file)
        return self.parse_options(options_file)
