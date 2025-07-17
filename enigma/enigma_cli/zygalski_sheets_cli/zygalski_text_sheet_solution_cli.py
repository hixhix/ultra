from zygalski_sheets.zygalski_sheets_text.text_sheet_solution import ZygalskiTextSheetSolution
from argparse import ArgumentError, RawTextHelpFormatter
import os


class ZygalskiSheetTextSolutionCli:

    def __init__(self, parser):
        self._parser = parser
        self._add_description()
        self._add_parser_arguments()

    def process_args(self, args):
        permutation = args["permutation"]
        rs = args["rs"]

        with open(self._indicators_file_path, "r") as f:
            indicators_str = f.read()

        indicators = indicators_str.split("\n")
        indicators = [ind for ind in indicators if len(ind) == 10]

        text_sheet_solution = ZygalskiTextSheetSolution()
        solution_string = text_sheet_solution.solution(self._machine_type, indicators, permutation, rs)
        print(solution_string)

    def _add_description(self):
        self._parser.formatter_class = RawTextHelpFormatter
        self._parser.description = (f"Generates a zygalski sheet solution in text format.\n\n")

    def _add_parser_arguments(self):
        self._parser.add_argument('machine_type', type=self._valid_machine_type, help='Machine type "WEHRMACHT early" or "WEHRMACHT late"')
        self._parser.add_argument('indicators_file', type=self._valid_indicators_file, help='The indicators file path.')
        self._parser.add_argument('permutation', type=str, help='The permutation string.')
        self._parser.add_argument('rs', type=str, help='The slow rotor ring setting')

    def _valid_machine_type(self, machine_type):
        valid_machines = ["WEHRMACHT early","WEHRMACHT late"]

        for _machine_type in valid_machines:
            if machine_type.upper() == _machine_type.upper():
                self._machine_type = _machine_type
                return _machine_type
        raise ArgumentError(f"{machine_type} is not a valid enigma machine. Must be 'WEHRMACHT early' or 'WEHRMACHT late'")

    def _valid_indicators_file(self, indicators_file):
        """

        """
        if os.path.isfile(indicators_file):
            self._indicators_file_path = indicators_file
        else:
            raise ArgumentError(f"{indicators_file} is not a valid input file path.")
