from zygalski_sheets.herivel_square import herivel_square
from argparse import ArgumentError, RawTextHelpFormatter
import os


class HerivelSquareCli:

    def __init__(self, parser):
        self._parser = parser
        self._add_description()
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

    def _add_description(self):
        """

        """
        self._parser.formatter_class = RawTextHelpFormatter
        self._parser.description = (f"Produces a herivel square from an indicators file.\n"
                                    f"In order for the herivel square to work correctly the indicators file needs to have been generated using\n"
                                    f"the -f flag to generate the first days settings.\n\n")

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
