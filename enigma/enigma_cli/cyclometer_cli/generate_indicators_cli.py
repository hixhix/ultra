from enigma_core.validators.scrambler_validators.scrambler_validators import *
from enigma_core.validators.plugboard_validators.plugboard_validators import *
from argparse import ArgumentError, RawTextHelpFormatter
from cyclometer.generate_indicators import generate_indicators
from enigma_core.factory import make_machine


class GenerateIndicatorsCli:

    def __init__(self, parser):
        self.parser = parser
        self._wehrmacht_early_data = None
        self._wehrmacht_late_data = None
        self._load_machine_data()
        self._add_parser_arguments()

    def process_args(self, args):
        number = args["number"]
        settings = {
            "MACHINE_TYPE":self._machine_type,
            "SCRAMBLER_SETTINGS":{
                "REFLECTOR_TYPE":self._reflector,
                "ROTOR_TYPES":self._rotor_types,
                "RING_SETTINGS":self._ring_settings,
                "ROTOR_SETTINGS":self._rotor_settings,
                "SCRAMBLER_CHARSET_FLAG":"L"
            },
            "PLUGBOARD_SETTINGS":self._pb_settings
        }

        indicators = generate_indicators(settings, number)
        for indicator in indicators:
            print(indicator)        

    def _load_machine_data(self):
        machine_obj = make_machine("WEHRMACHT early")
        self._wehrmacht_early_data = machine_obj.scrambler.collection.collection_dict()

        machine_obj = make_machine("WEHRMACHT late")
        self._wehrmacht_late_data = machine_obj.scrambler.collection.collection_dict()

    def _add_parser_arguments(self):
        self.parser.add_argument('machine_type', type=self._valid_machine_type, help='Machine type "WEHRMACHT early" or "WEHRMACHT late"')
        ref_str = (f"WEHRMACHT early ( {' | '.join(self._wehrmacht_early_data['REFLECTORS'])} )\n"
                   f"WEHRMACHT late ( {' | '.join(self._wehrmacht_late_data['REFLECTORS'])} )\n")
        self.parser.add_argument('reflector', type=self._valid_reflector, help=ref_str)
        rotor_types_str = (f"WEHRMACHT early ( {' | '.join(self._wehrmacht_early_data['ROTORS_DYNAMIC'])} )\n"
                           f"WEHRMACHT late ( {' | '.join(self._wehrmacht_late_data['ROTORS_DYNAMIC'])} )\n")
        self.parser.add_argument('rotor_types', type=self._valid_rotor_types, help=rotor_types_str)
        self.parser.add_argument('rotor_settings', type=self._valid_rotor_settings, help=f'Rotor setting A-Z in format{" "*27}"RS,RM,RF"')
        self.parser.add_argument('ring_settings', type=self._valid_ring_settings, help=f'Ring settings A-Z in format{" "*27}"RS,RM,RF"')
        self.parser.add_argument('plugboard_settings', type=self._valid_plugboard_settings, help=f'plugboard settings in format{" "*26}"AB,CD,EF,GH,IJ,KL,M,N,O,P,QR,ST"')
        self.parser.add_argument('number', type=int, help=f'number of indicators{" "*34}INTEGER')

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

    def _valid_rotor_settings(self, rotor_settings):
        try:
            rotor_settings = ScramblerValidators.valid_rotor_settings_string(rotor_settings, "L", 3)
        except RotorSettingsStringError as e:
            raise ArgumentError(e.__str__())
        else:
            self._rotor_settings = rotor_settings

    def _valid_plugboard_settings(self, pb_settings):
        try:
            pb_settings = PlugboardValidators.valid_stecker_pb_settings_string(pb_settings, "L")
        except SteckerPBSettingsStringError as e:
            raise ArgumentError(e.__str__())
        else:
            self._pb_settings = pb_settings
