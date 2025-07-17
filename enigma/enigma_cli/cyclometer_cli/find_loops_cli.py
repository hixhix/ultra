from cyclometer.loop_finder import LoopFinder
from argparse import ArgumentError
import os


class FindLoopsCli:

    def __init__(self, parser):
        """

        """
        self.parser = parser
        self._input_file_path = None
        self._add_description()
        self._add_arguments()

    def process_args(self, args):
        """

        """
        with open(self._input_file_path, "r") as f:
            indicators_str = f.read()

        indicators = indicators_str.split('\n')

        indicators = [ind for ind in indicators if len(ind) == 6]

        loop_finder = LoopFinder()

        loops = loop_finder.find_all_loops(indicators)

        loops_str = f"G1 {loops['G1']} G2 {loops['G2']} G3 {loops['G3']}"

        print(loops_str)

    def _add_description(self):
        """

        """
        self.parser.description = "Finds the cyclometer loops using an indicators file.\n\n"

    def _add_arguments(self):
        """

        """
        self.parser.add_argument('indicator_file',type=self._valid_input_file,help='The indicators file path')

    def _valid_input_file(self, input_file):
        """

        """
        if os.path.isfile(input_file):
            self._input_file_path = input_file
        else:
            raise ArgumentError(f"{input_file} is not a valid input file path.")
