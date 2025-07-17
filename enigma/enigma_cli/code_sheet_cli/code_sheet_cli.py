from code_sheets.wehrmacht_early_code_sheet import WehrmachtEarlyCodeSheet
from code_sheets.wehrmacht_late_code_sheet import WehrmachtLateCodeSheet
from code_sheets.luftwaffe_code_sheet import LuftwaffeCodeSheet
from code_sheets.kriegsmarine_m3_code_sheet import KriegsmarineM3CodeSheet
from code_sheets.kriegsmarine_m4_code_sheet import KriegsmarineM4CodeSheet
from enigma_core.validators.machine_validators.machine_validators import MachineValidators, EnigmaMachineError
from enigma_core.factory import machine_list
import argparse
import os


class CodeSheetsCli:

    def __init__(self, parser):
        self._parser = parser
        self._days = 31
        self._sc_char_flag = None
        self._pb_char_flag = None
        self._pb_mode = None
        self._output_file_path = None
        self._add_description()
        self._add_parser_arguments()

    def process_args(self, args):
        dora_flag = args["dora_flag"]
        if self._machine_type == "WEHRMACHT early":
            code_sheet = WehrmachtEarlyCodeSheet(self._sc_char_flag, self._pb_char_flag, self._pb_mode, self._days)
        elif self._machine_type == "WEHRMACHT late":
            code_sheet = WehrmachtLateCodeSheet(self._sc_char_flag, self._pb_char_flag, self._pb_mode, self._days)
        elif self._machine_type == "LUFTWAFFE":
            code_sheet = LuftwaffeCodeSheet(self._sc_char_flag, self._pb_char_flag, self._pb_mode, self._days, dora_flag)
        elif self._machine_type == "Kriegsmarine M3":
            code_sheet = KriegsmarineM3CodeSheet(self._sc_char_flag, self._pb_char_flag, self._pb_mode, self._days)
        elif self._machine_type == "Kriegsmarine M4":
            code_sheet = KriegsmarineM4CodeSheet(self._sc_char_flag, self._pb_char_flag, self._pb_mode, self._days)

        sheet_str = code_sheet.sheet()

        if self._output_file_path:
            with open(self._output_file_path, "w") as f:
                f.write(sheet_str)
        else:
            print(sheet_str)

    def _valid_output_file(self, args):
        """

        """
        output_file = args['output_file']
        if output_file:
            dirpath = os.path.split(output_file)[0]
            if dirpath != '' and  not os.path.isdir(dirpath):
                raise Exception(f"{dirpath} is not a valid output directory path.")
            self._output_file_path = output_file

    def _add_description(self):
        """

        """
        self._parser.description = (
            f"Allows for the creation of enigma machine code sheets.\n"
            f"The scrambler and plugboard settings can be configured seperatly to use letters or numbers.\n"
            f"The plugboard settings can be configured for a standard plugboard that uses stecker cables or alternativly to use an uhr box attachment.\n"
            f"A rewireable dora reflector UKW-D is simulated for the luftwaffe enigma machine.\n")


    def _add_parser_arguments(self):
        """

        """
        self._add_machine_arg()
        self._add_scrambler_char_flag_arg()
        self._add_plugboard_char_flag_arg()
        self._add_plugboard_mode_arg()
        self._add_reflector_dora_flag_arg()
        self._add_output_file_arg()

    def _add_machine_arg(self):
        machines = machine_list()
        machines_str = " | ".join(machines)
        machines_str = f"( {machines_str} )"
        self._parser.add_argument('machine', type=self._valid_machine_type, help=f'Enigma machine type {machines_str}')

    def _add_scrambler_char_flag_arg(self):
        self._parser.add_argument(
            'scrambler-char-flag',
            type=self.valid_scrambler_char_flag,
            help="The scrambler charset flag 'L' or 'N'.")

    def _add_plugboard_char_flag_arg(self):
        self._parser.add_argument(
            'plugboard-char-flag',
            type=self.valid_plugboard_char_flag,
            help="The plugboard charset flag 'L' or 'N'.")

    def _add_plugboard_mode_arg(self):
        self._parser.add_argument(
            'plugboard-mode',
            type=self.valid_plugboard_mode,
            help="The plugboard mode 'S' or 'U'.")

    def _add_reflector_dora_flag_arg(self):
        self._parser.add_argument(
            '-d','--dora-flag',
            action='store_true',
            help="Provide this flag with Luftwaffe enigma for rewireable UKW-D.")

    def _add_output_file_arg(self):
        self._parser.add_argument(
            '-o','--output-file',
            type=self.valid_output_file,
            help='Optional output file. Will print to terminal if not provided.')

    def _valid_machine_type(self, machine):
        """

        """
        try:
            machine = MachineValidators.valid_enigma_machine(machine)
        except EnigmaMachineError as e:
            raise argparse.ArgumentError(e.__str__())
        else:
            self._machine_type = machine
            return machine

    def valid_scrambler_char_flag(self, v):
        if v.upper() in ["L","N"]:
            v = v.upper()
            self._sc_char_flag = v
            return v
        else:
            raise argparse.ArgumentError(f"Invalid scrambler char flag {v}. 'L' or 'N' expected")

    def valid_plugboard_char_flag(self, v):
        if v.upper() in ["L","N"]:
            v = v.upper()
            self._pb_char_flag = v
            return v
        else:
            raise argparse.ArgumentError(f"Invalid plugboard char flag {v}. 'L' or 'N' expected")

    def valid_plugboard_mode(self, v):
        if v.upper() in ["S","U"]:
            v = v.upper()
            self._pb_mode = v
            return v
        else:
            raise argparse.ArgumentError(f"Invalid plugboard mode {v}. 'S' or 'U' expected")

    def valid_output_file(self, args):
        """

        """
        output_file = args['output_file']
        if output_file:
            dirpath = os.path.split(output_file)[0]
            if dirpath != '' and  not os.path.isdir(dirpath):
                raise argparse.ArgumentError(f"{dirpath} is not a valid output directory path.")
            else:
                self._output_file_path = output_file
