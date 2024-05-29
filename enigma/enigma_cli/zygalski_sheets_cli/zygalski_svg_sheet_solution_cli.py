from zygalski_sheets.zygalski_sheets_svg.svg_sheet_solution import ZygalskiSheetSolution
from argparse import ArgumentError


class ZygalskiSheetSVGSolutionCli:

    def __init__(self, parser):
        self._parser = parser
        self._add_parser_arguments()

    def process_args(self, args):
        """
        
        """
        indicators_file = args["indicators_file"]
        permutation = args["permutation"]
        out_file = args['output_file']
        rs = args['rs']

        with open(indicators_file, "r") as f:
            indicators = f.read()

        indicators = indicators.split('\n')

        indicators = [ind for ind in indicators if len(ind) != 0]

        solution = ZygalskiSheetSolution()
        solution_svg = solution.show_solution(self._machine_type, indicators, permutation, rs)

        out_file = f"{out_file}.svg"

        with open(out_file, "w") as f:
            f.write(solution_svg)

    def _add_parser_arguments(self):
        """
        
        """
        self._parser.add_argument('machine_type', type=self._valid_machine_type, help='Machine type "WEHRMACHT early" or "WEHRMACHT late"')
        self._parser.add_argument('indicators_file', type=str, help='The indicators file path.')
        self._parser.add_argument('permutation', type=str, help='The permutation string.')
        self._parser.add_argument('rs', type=str, help='The slow rotor ring setting')
        self._parser.add_argument('output_file', type=str, help='The output file name')

    def _valid_machine_type(self, machine_type):
        valid_machines = ["WEHRMACHT early","WEHRMACHT late"]

        for _machine_type in valid_machines:
            if machine_type.upper() == _machine_type.upper():
                self._machine_type = _machine_type
                return _machine_type
        raise ArgumentError(f"{machine_type} is not a valid enigma machine. Must be 'WEHRMACHT early' or 'WEHRMACHT late'")