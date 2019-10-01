import argparse
import os


class InputPath(object):
    """
    Class to use with argparse 'type' option.
    When given a directory or file paths, it first checks for existence and
    then whether the paths is accessible for reading.

    Example:
        argument_parser = argparse.ArgumentParser()
        argument_parser.add_argument(
            'file',
            type=InputPath(),
        )
    """
    @staticmethod
    def check_exists(input_path):
        if not os.path.exists(input_path):
            raise argparse.ArgumentTypeError(
                f'Unable to find input path: {input_path}'
            )

    @staticmethod
    def check_readable(input_path):
        if not os.access(input_path, os.R_OK):
            raise argparse.ArgumentTypeError(
                f'Given input path is not readable.'
                f'  Path: {input_path}'
            )

    def __call__(self, input_path):
        self.check_exists(input_path)
        self.check_readable(input_path)
        return input_path
