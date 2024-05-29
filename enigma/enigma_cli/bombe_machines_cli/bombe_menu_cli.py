"""
ARGUMENTS TO PROVIDE.

1. Plain Text.
2. Cipher Text.
3. Permutation.
"""
from enigma_cli.bombe_machines_cli.bombe_machine_cli import BombeMachineCli
from enigma_cli.bombe_machines_cli.filter_cribs_cli import FilterCribsCli
import argparse


class BombeMenuCli:

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{i+1}".rjust(2, '0') for i in range(26)]

    def __init__(self, parser):
        self._parser = parser
        self._bombe_machine_cli = None
        self._ring_settings_optomizer_cli = None
        self._filter_cribs_cli = None
        self._add_parser_arguments()

    def process_args(self, args):
        """
        
        """
        if args['turing_bombe'] == "bombe_machine":
            self._bombe_machine_cli.process_args(args)
        elif args['turing_bombe'] == "filter_cribs":
            self._filter_cribs_cli.process_args(args)

    def _add_parser_arguments(self):
        """
        
        """
        subparsers = self._parser.add_subparsers(dest='turing_bombe')
        subparsers.required = True

        bombe_machine = subparsers.add_parser(
            'bombe_machine',
            help='Run the bombe machine')
        self._bombe_machine_cli = BombeMachineCli(bombe_machine)

        filter_cribs = subparsers.add_parser(
            'filter_cribs',
            help='Filter cribs from cipher text using provided plain text')
        self._filter_cribs_cli = FilterCribsCli(filter_cribs)
