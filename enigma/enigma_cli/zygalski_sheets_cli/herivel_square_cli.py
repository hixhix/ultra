from zygalski_sheets.herivel_square import herivel_square
from argparse import ArgumentError
import os


class HerivelSquareCli:

    def __init__(self, parser):
        self._parser = parser
        self._add_parser_arguments()

    def process_args(self, args):
        """
        
        """
        with open(self._indicators_file_path, "r") as f:
            indicators_str = f.read()

        indicators = indicators_str.split("\n")

        indicators = [ind for ind in indicators if len(ind) != 0]

        square_str = herivel_square(indicators)

        print(square_str)

    def _add_parser_arguments(self):
        """
        
        """
        self._parser.add_argument('indicators_file', type=self._valid_indicators_file, help='The indicators file path.')

    def _valid_indicators_file(self, indicators_file):
        """
        
        """
        if os.path.isfile(indicators_file):
            self._indicators_file_path = indicators_file
        else:
            raise ArgumentError(f"{indicators_file} is not a valid input file path.")