from zygalski_sheets.filter_indicators import filter_females
from zygalski_sheets.scrambler_permutations import ScramblerPermutations
from argparse import ArgumentError


class PermutationsFilterCli:

    def __init__(self, parser):
        self._parser = parser
        self._add_arguments()

    def process_args(self, args):
        from pprint import pprint
        indicators_fpath = args['indicators_file']
        verbose_flag = args['verbose']

        with open(indicators_fpath, 'r') as f:
            indicators_str = f.read()

        indicators = indicators_str.split('\n')

        indicators = [indicator for indicator in indicators if len(indicator) == 10]

        indicators = filter_females(indicators)

        sp = ScramblerPermutations()

        permutations = sp.solve(self._machine_type, indicators, verbose_flag)

        perm_str = "\n"

        for permutation, perm_dict in permutations.items():
            perm_str += f"{permutation}\n"
            rs = perm_dict["rs"]
            ring_settings = perm_dict["ring_settings"]
            ring_settings = [f"{rs}{ring_setting}" for ring_setting in ring_settings]
            ring_settings = " ".join(ring_settings)
            perm_str += f"RING SETTINGS: {ring_settings}\n"
            indicators = perm_dict["indicators"]
            for indicator in indicators:
                perm_str += f"{indicator}\n"

        print(perm_str)

    def _add_description(self):
        """

        """
        self._parser.formatter_class = RawTextHelpFormatter
        self._parser.description = (f"Produces a herivel square from an indicators file.\n"
                                    f"In order for the herivel square to work correctly the indicators file needs to have been generated using\n"
                                    f"the -f flag to generate the first days settings.\n\n")

    def _add_arguments(self):
        self._parser.add_argument('machine_type', type=self._valid_machine_type, help='Machine type "WEHRMACHT early" or "WEHRMACHT late"')
        self._parser.add_argument('indicators_file', type=str, help='indicators file path')
        self._parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode. Displays permutations as they are being checked')

    def _valid_machine_type(self, machine_type):
        valid_machines = ["WEHRMACHT early","WEHRMACHT late"]

        for _machine_type in valid_machines:
            if machine_type.upper() == _machine_type.upper():
                self._machine_type = _machine_type
                return _machine_type
        raise ArgumentError(f"{machine_type} is not a valid enigma machine. Must be 'WEHRMACHT early' or 'WEHRMACHT late'")
