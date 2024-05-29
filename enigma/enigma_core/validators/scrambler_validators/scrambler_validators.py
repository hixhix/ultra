from enigma_core.validators.scrambler_validators.validators.reflector_type_validator import ReflectorTypeValidator, ReflectorTypeError
from enigma_core.validators.scrambler_validators.validators.rotor_types_string_validator import RotorTypesStringValidator, RotorTypesStringError
from enigma_core.validators.scrambler_validators.validators.rotor_types_dict_validator import RotorTypesDictValidator, RotorTypesDictError
from enigma_core.validators.scrambler_validators.validators.rotor_settings_string_validator import RotorSettingsStringValidator, RotorSettingsStringError
from enigma_core.validators.scrambler_validators.validators.rotor_settings_dict_validator import RotorSettingsDictValidator, RotorSettingsDictError
from enigma_core.validators.scrambler_validators.validators.ring_settings_string_validator import RingSettingsStringValidator, RingSettingsStringError
from enigma_core.validators.scrambler_validators.validators.ring_settings_dict_validator import RingSettingsDictValidator, RingSettingsDictError
from enigma_core.validators.scrambler_validators.validators.ring_character_validator import RingCharacterValidator, RingCharacterError
from enigma_core.validators.scrambler_validators.validators.permutation_string_validator import PermutationStringValidator, PermutationError
from enigma_core.validators.scrambler_validators.validators.reflector_wire_string_validator import ReflectorWireStringValidator, ReflectorWireStringError


class ScramblerValidators:

    def valid_reflector_type(machine_type, reflector_type):
        try:
            validator = ReflectorTypeValidator()
            reflector_type = validator.validate(machine_type, reflector_type)
        except ReflectorTypeError as e:
            raise e
        else:
            return reflector_type

    def valid_rotor_types_string(machine_type, rotor_types_string):
        try:
            validator = RotorTypesStringValidator()
            rotor_types_dict = validator.validate(machine_type, rotor_types_string)
        except RotorTypesStringError as e:
            raise e
        else:
            return rotor_types_dict

    def valid_rotor_types_dict(machine_type, rotor_types_dict):
        try:
            validator = RotorTypesDictValidator()
            rotor_types_dict = validator.validate(machine_type, rotor_types_dict)
        except RotorTypesDictError as e:
            raise e
        else:
            return rotor_types_dict

    def valid_rotor_settings_string(settings_string, charset_flag, positions):
        try:
            validator = RotorSettingsStringValidator()
            settings_dict = validator.validate(settings_string, charset_flag, positions)
        except RotorSettingsStringError as e:
            raise e
        else:
            return settings_dict

    def valid_rotor_settings_dict(settings_dict, charset_flag, check_positions=None):
        try:
            validator = RotorSettingsDictValidator()
            settings_dict = validator.validate(settings_dict, charset_flag, check_positions)
        except RotorSettingsDictError as e:
            raise e
        else:
            return settings_dict

    def valid_ring_settings_string(settings_string, charset_flag, positions):
        try:
            validator = RingSettingsStringValidator()
            settings_dict = validator.validate(settings_string, charset_flag, positions)
        except RingSettingsStringError as e:
            raise e
        else:
            return settings_dict

    def valid_ring_settings_dict(settings_dict, charset_flag, check_positions=None):
        try:
            validator = RingSettingsDictValidator()
            settings_dict = validator.validate(settings_dict, charset_flag, check_positions)
        except RingSettingsDictError as e:
            raise e
        else:
            return settings_dict

    def valid_ring_character(ring_character, charset_flag):
        try:
            validator = RingCharacterValidator()
            ring_character = validator.validate(ring_character, charset_flag)
        except RingCharacterError as e:
            raise e
        else:
            return ring_character

    def valid_permutation_string(machine_type, permutation_string, rs_flag=True, group_flag=True):
        try:
            validator = PermutationStringValidator()
            permutation_dict = validator.validate(machine_type, permutation_string, rs_flag, group_flag)
        except PermutationError as e:
            raise e
        else:
            return permutation_dict

    def valid_reflector_wiring(wire_string, charset_flag):
        try:
            validator = ReflectorWireStringValidator()
            wire_list = validator.validate(wire_string, charset_flag)
        except ReflectorWireStringError as e:
            raise e
        else:
            return wire_list