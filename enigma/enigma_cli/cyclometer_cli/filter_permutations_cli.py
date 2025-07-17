from cyclometer.filter_permutations import filter_permutations
from argparse import ArgumentError


class FilterPermutationsCli:

    def __init__(self, parser):
        """

        """
        self._parser = parser
        self._machine_type = None
        self._add_description()
        self._add_parser_arguments()

    def process_args(self, args):
        """

        """
        loops_str = args['loops-str']

        matches = filter_permutations(self._machine_type, loops_str)

        for match in matches:
            print(match)

    def _add_description(self):
        """

        """
        self._parser.description = "Finds reflector type and rotor types combination and rotor settings that produce the provided cycle loops.\n\n"

    def _add_parser_arguments(self):
        """

        """
        self._parser.add_argument(
            'machine_type',
            type=self._valid_machine_type,
            help='Machine type "WEHRMACHT early" or "WEHRMACHT late"')
        self._parser.add_argument(
            'loops-str',
            type=str,
            help='The loop string to filter on in format "G1 (13)(13) G2 (8)(8)(8)(1)(1) G3 (13)(13)"')

    def _valid_machine_type(self, machine_type):
        valid_machines = ["WEHRMACHT early","WEHRMACHT late"]

        for _machine_type in valid_machines:
            if machine_type.upper() == _machine_type.upper():
                self._machine_type = _machine_type
                return _machine_type
        err_msg = (f"{machine_type} is not a valid enigma machine. "
                   f"Must be 'WEHRMACHT early' or 'WEHRMACHT late'")
        raise ArgumentError(err_msg)
