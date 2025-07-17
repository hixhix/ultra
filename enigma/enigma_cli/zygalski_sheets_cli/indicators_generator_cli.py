from enigma_core.validators.scrambler_validators.scrambler_validators import *
from enigma_core.validators.plugboard_validators.plugboard_validators import *
from argparse import ArgumentError, RawTextHelpFormatter
from zygalski_sheets.generate_indicators import generate_indicators
from zygalski_sheets.filter_indicators import filter_females
from enigma_core.factory import make_machine
from argparse import RawTextHelpFormatter


class IndicatorsGeneratorCli:

    def __init__(self, parser):
        self.parser = parser
        self._wehrmacht_early_data = None
        self._wehrmacht_late_data = None
        self._load_machine_data()
        self._add_description()
        self._add_parser_arguments()

    def process_args(self, args):
        if args['indicators'] == 'generate_indicators':
            number = args["number"]
            settings = {
                "MACHINE_TYPE":self._machine_type,
                "SCRAMBLER_SETTINGS":{
                    "REFLECTOR_TYPE":self._reflector,
                    "ROTOR_TYPES":self._rotor_types,
                    "RING_SETTINGS":self._ring_settings,
                    "SCRAMBLER_CHARSET_FLAG":"L"
                },
                "PLUGBOARD_SETTINGS":self._pb_settings
            }

            f = args['f']
            indicators = generate_indicators(self._machine_type, settings, number, f)
            for indicator in indicators:
                print(indicator)
        else:
            self._filter_indicators(args)

    def _load_machine_data(self):
        machine_obj = make_machine("WEHRMACHT early")
        self._wehrmacht_early_data = machine_obj.scrambler.collection.collection_dict()

        machine_obj = make_machine("WEHRMACHT late")
        self._wehrmacht_late_data = machine_obj.scrambler.collection.collection_dict()

    def _filter_indicators(self, args):
        file_path = args['indicators_file']
        with open(file_path, 'r') as f:
            indicators = f.read()

        indicators = indicators.split('\n')

        indicators = [indicator for indicator in indicators if len(indicator) == 10]

        filtered = filter_females(indicators)

        if args['unique_slow_rotors']:
            used_slow_rotors = []
            _filtered = []
            for indicator in filtered:
                if indicator[0] not in used_slow_rotors:
                    used_slow_rotors.append(indicator[0])
                    _filtered.append(indicator)
            filtered = _filtered

        for indicator in filtered:
            print(indicator)

    def _add_description(self):
        self.parser.formatter_class = RawTextHelpFormatter
        self.parser.description = "Allows for the creation and filtering of indicators."

    def _add_parser_arguments(self):
        subparsers = self.parser.add_subparsers(dest='indicators')
        generate_traffic = subparsers.add_parser('generate_indicators', help='generates indicators', formatter_class=RawTextHelpFormatter)
        generate_traffic.description = (f"Allows for the creation of indicators from enigma machine types WEHRMACHT early and WEHRMACHT late.\n"
                                        f"The -f flag if provided will produce indicators that will be representative of the days first ring\n"
                                        f"settings where due to human factors and operator error the distribution of the inital rotor settings\n"
                                        f"will not be as random as the rest of the day allowing for the herival tip to be used to get that days\n"
                                        f"ring settings.\n\n")
        generate_traffic.add_argument('machine_type', type=self._valid_machine_type, help='Machine type "WEHRMACHT early" or "WEHRMACHT late"')
        ref_str = (f"WEHRMACHT early ( {' | '.join(self._wehrmacht_early_data['REFLECTORS'])} )\n"
                   f"WEHRMACHT late ( {' | '.join(self._wehrmacht_late_data['REFLECTORS'])} )\n")
        generate_traffic.add_argument('reflector', type=self._valid_reflector, help=ref_str)
        rotor_types_str = (f"WEHRMACHT early ( {' | '.join(self._wehrmacht_early_data['ROTORS_DYNAMIC'])} )\n"
                           f"WEHRMACHT late ( {' | '.join(self._wehrmacht_late_data['ROTORS_DYNAMIC'])} )\n")
        generate_traffic.add_argument('rotor_types', type=self._valid_rotor_types, help=rotor_types_str)
        generate_traffic.add_argument('ring_settings', type=self._valid_ring_settings, help=f'Ring settings A-Z in format{" "*27}"RS,RM,RF"')
        generate_traffic.add_argument('plugboard_settings', type=self._valid_plugboard_settings, help=f'plugboard settings in format{" "*26}"AB,CD,EF,GH,IJ,KL,MN,OP,QR,ST"')
        generate_traffic.add_argument('number', type=int, help=f'number of indicators{" "*34}INTEGER')
        generate_traffic.add_argument('-f',action='store_true',help='creates days first settings that contain Herivel tips')

        filter_traffic = subparsers.add_parser('filter_indicators', help='filters females from indicators', formatter_class=RawTextHelpFormatter)
        filter_traffic.description = (f"Allows for females to be filtered from an indicators file. The -u unique slow rotor flag if used will\n"
                                      f"return a set filtered females where the slow rotor setting is not repeated in the set.\n\n")
        filter_traffic.add_argument('indicators_file', type=str, help='indicators file path')
        filter_traffic.add_argument('-u', '--unique_slow_rotors', action='store_true', help='return indicators with unique slow rotor characters')

    def _valid_machine_type(self, machine_type):
        valid_machines = ["WEHRMACHT early","WEHRMACHT late"]

        for _machine_type in valid_machines:
            if machine_type.upper() == _machine_type.upper():
                self._machine_type = _machine_type
                return _machine_type
        raise ArgumentError(f"{machine_type} is not a valid enigma machine. Must be 'WEHRMACHT early' or 'WEHRMACHT late'")

    def _valid_reflector(self, reflector):
        try:
            reflector = ScramblerValidators.valid_reflector_type(self._machine_type, reflector)
        except ReflectorTypeError as e:
            raise ArgumentError(e.__str__())
        else:
            self._reflector = reflector

    def _valid_rotor_types(self, rotor_types):
        try:
            rotor_types = ScramblerValidators.valid_rotor_types_string(self._machine_type, rotor_types)
        except RotorTypesStringError as e:
            raise ArgumentError(e.__str__())
        else:
            self._rotor_types = rotor_types

    def _valid_ring_settings(self, ring_settings):
        try:
            ring_settings = ScramblerValidators.valid_ring_settings_string(ring_settings, "L", 3)
        except RingSettingsStringError as e:
            raise ArgumentError(e.__str__())
        else:
            self._ring_settings = ring_settings

    def _valid_plugboard_settings(self, pb_settings):
        try:
            pb_settings = PlugboardValidators.valid_stecker_pb_settings_string(pb_settings, "L")
        except SteckerPBSettingsStringError as e:
            raise ArgumentError(e.__str__())
        else:
            self._pb_settings = pb_settings
