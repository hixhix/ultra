from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.validators.machine_validators.machine_validators import *
from enigma_core.validators.scrambler_validators.scrambler_validators import *
from enigma_core.validators.plugboard_validators.plugboard_validators import *
from enigma_core.factory import machine_list, make_machine
import argparse
import os


class CommandLineEnigmaCli:

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{i+1}".rjust(2, '0') for i in range(26)]

    def __init__(self, parser):
        self._parser = parser
        self._machine_data = {}
        self._machine_type = None
        self._positions = None
        self._sc_char_flag = None
        self._sc_mode = None
        self._reflector = None
        self._reflector_wiring = None
        self._rotor_types = None
        self._ring_settings = None
        self._rotor_settings = None
        self._pb_char_flag = None
        self._pb_mode = None
        self._uhr_box_setting = None
        self._pb_connections = None
        self._input_file_path = None
        self._output_file_path = None
        self._message = None
        self._load_machine_data()
        self._add_description()
        self._add_parser_arguments()

    def process_args(self, args):
        try:
            self._valid_machine_type(args)
            self._valid_reflector(args)
            self._valid_rotor_types(args)
            self._valid_ring_settings(args)
            self._valid_rotor_settings(args)
            self._valid_plugboard_settings(args)
            self._valid_input_file(args)
            self._valid_output_file(args)
            self._read_input_file(args)
            self._get_machine_output(args)
        except Exception as e:
            #print(e)
            raise e

    def _valid_machine_type(self, args):
        """

        """
        machine = args['machine']
        try:
            machine = MachineValidators.valid_enigma_machine(machine)
        except EnigmaMachineError as e:
            raise e
        else:
            if not self._machine_data[machine]["ROTORS_STATIC"]:
                self._positions = 3
            else:
                self._positions = 4
            self._machine_type = machine
            return machine

    def _valid_reflector(self, args):
        """

        """
        reflector = args['reflector']
        try:
            ScramblerValidators.valid_reflector_type(self._machine_type, reflector)
        except ReflectorTypeError as e:
            raise e
        else:
            self._reflector = reflector
            return reflector

    def _valid_rotor_types(self, args):
        """

        """
        rotor_types_str = args['rotors']
        try:
            rotor_types = ScramblerValidators.valid_rotor_types_string(self._machine_type, rotor_types_str)
        except RotorTypesStringError as e:
            raise e
        else:
            self._rotor_types = rotor_types
            return rotor_types

    def _valid_ring_settings(self, args):
        """

        """
        ring_settings_str = args['rng_settings']
        if ring_settings_str:
            try:
                ring_settings = ScramblerValidators.valid_ring_settings_string(ring_settings_str, self._sc_char_flag, self._positions)
            except RingSettingsStringError as e:
                raise e
            else:
                self._ring_settings = ring_settings
                return ring_settings

    def _valid_rotor_settings(self, args):
        """

        """
        rotor_settings_str = args['rot_settings']
        if rotor_settings_str:
            try:
                rotor_settings = ScramblerValidators.valid_rotor_settings_string(rotor_settings_str, self._sc_char_flag, self._positions)
            except RotorSettingsStringError as e:
                raise e
            else:
                self._rotor_settings = rotor_settings
                return rotor_settings

    def _valid_plugboard_settings(self, args):
        """

        """
        conns = None

        pb_str = args['plugboard_connections']
        if pb_str:
            if self._pb_mode == 'S' and pb_str:
                try:
                    conns = PlugboardValidators.valid_stecker_pb_settings_string(pb_str, self._pb_char_flag)
                except SteckerPBSettingsStringError as e:
                    raise e
            elif self._pb_mode == 'U' and pb_str:
                try:
                    conns = PlugboardValidators.valid_uhr_box_pb_settings(pb_str, self._pb_char_flag)
                except UhrBoxPBSettingsStringError as e:
                    raise e
            self._pb_connections = conns
            return conns

    def _valid_input_file(self, args):
        """

        """
        input_file = args['input-file']
        if input_file:
            if input_file != '' and  not os.path.isfile(input_file):
                raise Exception(f"{input_file} is not a valid input file path.")
            self._input_file_path = input_file

    def _valid_output_file(self, args):
        """

        """
        output_file = args['output_file']
        if output_file:
            dirpath = os.path.split(output_file)[0]
            if dirpath != '' and  not os.path.isdir(dirpath):
                raise Exception(f"{dirpath} is not a valid output directory path.")
            self._output_file_path = output_file

    def _read_input_file(self, args):
        """

        """
        output_file = args["input-file"]

        with open(output_file, "r") as f:
            self._message = f.read()

    def _get_machine_output(self, args):
        """

        """
        settings = self._make_settings_dict()
        machine_obj = make_machine(self._machine_type)
        machine_obj.settings = settings

        settings = machine_obj.settings

        outp = ""
        for c in self._message:
            o = machine_obj.character_input(c)
            if o:
                outp += o

        if self._output_file_path:
            with open(self._output_file_path, 'w') as f:
                f.write(outp)
        else:
            print(outp)

    def _make_settings_dict(self):
        """

        """
        settings = {
            "MACHINE_TYPE":self._machine_type,
            "SCRAMBLER_SETTINGS":{
                "TURNOVER_FLAG":self._sc_mode,
                "SCRAMBLER_CHARSET_FLAG":self._sc_char_flag,
                "REFLECTOR_TYPE":self._reflector,
                "ROTOR_TYPES":self._rotor_types,
                "RING_SETTINGS":self._ring_settings,
                "ROTOR_SETTINGS":self._rotor_settings
            },
            "PLUGBOARD_SETTINGS":{
                "PLUGBOARD_MODE":self._pb_mode,
                "PLUGBOARD_CHARSET_FLAG":self._pb_char_flag,
                "PLUGBOARD_CONNECTIONS":self._pb_connections
            }
        }

        if self._pb_mode == "U":
            if self._uhr_box_setting:
                settings["PLUGBOARD_SETTINGS"]["UHR_BOX_SETTING"] = self._uhr_box_setting
            else:
                settings["PLUGBOARD_SETTINGS"]["UHR_BOX_SETTING"] = 0

        return settings

    def _load_machine_data(self):
        machines = machine_list()

        for machine in machines:
            machine_obj = make_machine(machine)
            self._machine_data[machine] = machine_obj.scrambler.collection.collection_dict()

    def _add_description(self):
        """

        """
        self._parser.description = (f"Provides an accurate command line simulation of a selection of enigma machines.\n"
                                    f"The following enigma machines are simulated.\n"
                                    f"\n"
                                    f"1. WEHRMACHT early\n"
                                    f"2. WEHRMACHT late\n"
                                    f"3. LUFTWAFFE\n"
                                    f"4. Kriegsmarine M3\n"
                                    f"5. Kriegsmarine M4\n"
                                    f"\n"
                                    f"Although not historicaly accurate the following functionality is provided to all enigma machine types.\n"
                                    f"It is possible to seperatly configure the scrambler and plugboard to use letters or numbers.\n"
                                    f"The plugboard can be configured as a standard plugboard that uses stecker cables or alternativly to use an uhr box attachment.\n\n")

    def _add_parser_arguments(self):
        """

        """
        self._add_machine_arg()
        self._add_scrambler_char_arg()
        self._add_scrambler_mode_arg()
        self._add_reflector_arg()
        self._add_rotor_types_arg()
        self._add_ring_settings_arg()
        self._add_rotor_settings_arg()
        self._add_plugboard_char_arg()
        self._add_plugboard_mode_arg()
        self._add_uhr_box_setting_arg()
        self._add_plugboard_settings_arg()
        self._add_input_file_arg()
        self._add_output_file_arg()

    def _add_machine_arg(self):
        machines = machine_list()
        machines_str = " | ".join(machines)
        machines_str = f"( {machines_str} )"
        self._parser.add_argument('machine', type=str, help=f'Enigma machine type {machines_str}')

    def _add_scrambler_char_arg(self):
        self._parser.add_argument(
            '-sc',
            '--scrambler-charset',
            type=self.valid_scrambler_char_flag, 
            help=f'Scrambler character set ( L | N ) where\n'
                 f'L = Letters\n'
                 f'N = Numbers')

    def _add_scrambler_mode_arg(self):
        self._parser.add_argument(
            '--scrambler-mode',
            type=self.valid_scrambler_mode,
            help='Scrambler turnover mode ( True | False )')

    def _add_reflector_arg(self):
        reflector_strs = {}

        for machine in self._machine_data:
            reflectors = self._machine_data[machine]["REFLECTORS"]
            reflector_str = " | ".join(reflectors)
            reflector_strs[machine] = f"( {reflector_str} )"

        ref_strs = "\n"
        for machine, ref_str in reflector_strs.items():
            ref_strs += f"{machine}".ljust(25, ' ')
            ref_strs += f"{ref_str}"
            ref_strs += '\n'

        self._parser.add_argument(
            'reflector',
            type=str,
            help=f'Reflector type in format "REF" {ref_strs}')

    def _add_rotor_types_arg(self):
        rotor_strs = {}

        for machine in self._machine_data:
            rotors_static = self._machine_data[machine]["ROTORS_STATIC"]
            rotors_dynamic = self._machine_data[machine]["ROTORS_DYNAMIC"]
            rotors_static_str = " | ".join(rotors_static)
            rotors_dynamic_str = ", ".join(rotors_dynamic)
            rotor_strs[machine] = (f"( {rotors_static_str} )".ljust(17, ' ')
	                         + f" [{rotors_dynamic_str}]")

        rot_strs = "\n"
        for machine, rot_str in rotor_strs.items():
            rot_strs += f"{machine}".ljust(25, ' ')
            rot_strs += f"{rot_str}"
            rot_strs += '\n'

        self._parser.add_argument('rotors',
            type=str,
            help=f'Rotor types in format "R4,RS,RM,RF" or "RS,RM,RF" where\n'
                 f'R4 = Static Rotor if applicable\n'
                 f'RS = Slow Rotor\n'
                 f'RM = Middle Rotor\n'
                 f'RF = Fast Rotor\n'
                 f' {rot_strs}')

    def _add_ring_settings_arg(self):
        self._parser.add_argument(
            '--rng-settings',
            type=str,
            help='Ring settings in format [RS,RM,RF]')

    def _add_rotor_settings_arg(self):
        self._parser.add_argument(
            '--rot-settings',
            type=str,
            help='Rotor settings in format [R4,RS,RM,RF] or [RS,RM,RF]')

    def _add_plugboard_char_arg(self):
        self._parser.add_argument(
            '-pc',
            '--plugboard-charset',
            type=self.valid_plugboard_char_flag,
            help=f'Plugboard character set ( L | N ) where\n'
                 f'L = Letters\n'
                 f'N = Numbers')

    def _add_plugboard_mode_arg(self):
        self._parser.add_argument(
            '--plugboard-mode',
            type=self.valid_plugboard_mode,
            help=f'Plugboard mode ( S | U ) where\n'
                 f'S = Stecker\n'
                 f'U = Uhr Box')

    def _add_uhr_box_setting_arg(self):
        self._parser.add_argument(
            '--uhr-box-setting',
            type=self.valid_uhr_box_setting,
            help='Uhr box setting in range 0 - 39')

    def _add_plugboard_settings_arg(self):
        self._parser.add_argument(
            '--plugboard-connections',
            type=str,
            help=f'Plugboard settings for stecker mode\n'
                 f'in format [AB,CD,EF,GH,IJ,KL,MN,OP,QR,ST] letters mode\n'
                 f'in format [1 2,3 4,5 6,7 8,9 10,11 12,13,14,15 16,17,18,19 20] numbers mode\n'
                 f'Plugboard settings for uhr box mode\n'
                 f'in format "A=[A,B,C,D,E,F,G,H,I,J] '
                 f'B=[K,L,M,N,O,P,Q,R,S,T]" letter mode\n'
                 f'in format "A=[1,2,3,4,5,6,7,8,9,10] '
                 f'B=[11,12,13,14,15,16,17,18,19,20]" number mode')

    def _add_input_file_arg(self):
        self._parser.add_argument(
            'input-file',
            type=str,
            help='The input file path')

    def _add_output_file_arg(self):
        self._parser.add_argument(
            '-o',
            '--output-file',
            type=str,
            help='The output file path')

    def valid_scrambler_char_flag(self, v):
        if v.upper() in ["L","N"]:
            v = v.upper()
            self._sc_char_flag = v
            return v
        else:
            raise argparse.ArgumentError("'L' or 'N' expected")

    def valid_scrambler_mode(self, v):
        mode = None
        if isinstance(v, bool):
            mode = v
        if v.lower() == 'true':
            mode = True
        elif v.lower() == 'false':
            mode = False
        if mode == None:
            raise argparse.ArgumentTypeError('Boolean value expected')
        self._scrambler_mode = mode
        return mode

    def valid_plugboard_char_flag(self, v):
        if v.upper() in ["L","N"]:
            v = v.upper()
            self._pb_char_flag = v
            return v
        else:
            raise argparse.ArgumentError("'L' or 'N' expected")

    def valid_plugboard_mode(self, v):
        if v.upper() in ["S","U"]:
            v = v.upper()
            return v
        else:
            raise argparse.ArgumentError("'S' or 'U' expected")

    def valid_uhr_box_setting(self, v):
        v = int(v)
        if v in range(40):
            self._uhr_box_setting = v
            return v
        else:
            raise argparse.ArgumentTypeError(f'{v} is not a valid uhr box setting. Must be in range "00"-> "39"')
