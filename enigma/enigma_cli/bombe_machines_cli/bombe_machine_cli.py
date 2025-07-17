from bombe_machines.bombe_machine import BombeMachine
import multiprocessing
from argparse import RawTextHelpFormatter


class BombeMachineCli:

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{i+1}".rjust(2, '0') for i in range(26)]

    def __init__(self, parser):
        self._parser = parser
        self._add_description()
        self._add_parser_arguments()

    def run_bombe(self, plain_text, cipher_text, permutation, machine_type, csko_flag, diagonal_board_flag):
        bombe_machine = BombeMachine(plain_text, cipher_text, permutation, machine_type, csko_flag, diagonal_board_flag)
        bombe_machine.solve()

    def process_args(self, args):
        plain_text = args["plain_text"]
        cipher_text = args["cipher_text"]
        perm_file_path = args["permutations"]
        wehrmacht_flag = args['w']
        kriegsmarine_m3_flag = args['k']
        kriegsmarine_m4_flag = args['K']
        csko_flag = args['c']
        diagonal_board_flag = args['d']

        if wehrmacht_flag:
            machine_type = "WEHRMACHT"
        elif kriegsmarine_m3_flag:
            machine_type = "Kriegsmarine M3"
        elif kriegsmarine_m4_flag:
            machine_type = "Kriegsmarine M4"

        with open(perm_file_path, "r") as f:
            perms = f.readlines()

        perms = [line.strip() for line in perms]

        processes = []

        for perm in perms:
            p = multiprocessing.Process(target=self.run_bombe, args=[plain_text, cipher_text, perm, machine_type, csko_flag, diagonal_board_flag])
            p.start()
            processes.append(p)

        for process in processes:
            process.join()

    def _add_description(self):
        self._parser.formatter_class = RawTextHelpFormatter
        self._parser.description = (f"Provides a simulation of a turing bombe and naval bombe machines.\n"
                                    f"Additional features include consecutive stecker knockout and the ability to disable the diagonal board.\n\n")

    def _add_parser_arguments(self):
        """

        """
        self._parser.add_argument('plain_text', type=str, help='The assumed plain text')
        self._parser.add_argument('cipher_text', type=str, help='The cipher text')
        self._parser.add_argument('permutations', type=str, help='The scrambler permutation file')
        group = self._parser.add_mutually_exclusive_group()
        group.add_argument('-w',action='store_true', help='Runs a Turing Welchman bombe')
        group.add_argument('-k',action='store_true', help='Runs a Kriegsmarine M3 naval bombe')
        group.add_argument('-K',action='store_true', help='Runs a Kriegsmarine M4 naval bombe')
        group.required = True
        self._parser.add_argument('-c', action='store_true', help='Enables consecutive stecker knockout')
        self._parser.add_argument('-d', action='store_false', help='Disables the diagonal board')
