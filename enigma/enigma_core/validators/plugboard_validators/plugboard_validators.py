from enigma_core.validators.plugboard_validators.validators.pb_socket_id_validator import valid_pb_socket_id, PBSocketIDError
from enigma_core.validators.plugboard_validators.validators.stecker_pb_dict_validator import SteckerPBDictValidator, SteckerPBSettingsDictError
from enigma_core.validators.plugboard_validators.validators.stecker_pb_settings_string_validator import SteckerPBSettingsStringValidator, SteckerPBSettingsStringError
from enigma_core.validators.plugboard_validators.validators.uhr_box_pb_dict_validator import UhrBoxPBDictValidator, UhrBoxPBSettingsDictError
from enigma_core.validators.plugboard_validators.validators.uhr_box_pb_group_settings_string_validator import UhrBoxPBGroupSettingsStringValidator, UhrBoxPBSettingsStringError
from enigma_core.validators.plugboard_validators.validators.uhr_box_pb_settings_validator import UhrBoxPBSettingsValidator, UhrBoxPBSettingsStringError
from enigma_core.validators.plugboard_validators.validators.uhr_box_plug_id_validator import valid_uhr_box_plug_id, UhrBoxPlugIDError


class PlugboardValidators:

    def valid_socket_id(socket_id, charset_flag):
        try:
            socket_id = valid_pb_socket_id(socket_id, charset_flag)
        except PBSocketIDError as e:
            raise e
        else:
            return e

    def valid_stecker_pb_settings_dict(settings_dict):
        try:
            validator = SteckerPBDictValidator()
            settings_dict = validator.validate(settings_dict)
        except SteckerPBSettingsDictError as e:
            raise e
        else:
            return settings_dict

    def valid_stecker_pb_settings_string(settings_string, charset_flag, pairs=None):
        try:
            validator = SteckerPBSettingsStringValidator()
            settings_dict = validator.validate(settings_string, charset_flag, pairs)
        except SteckerPBSettingsStringError as e:
            raise e
        else:
            return settings_dict

    def valid_uhr_box_pb_dict(settings_dict):
        try:
            validator = UhrBoxPBDictValidator()
            settings_dict = validator.validate(settings_dict)
        except UhrBoxPBSettingsDictError as e:
            raise e
        else:
            return settings_dict

    def valid_uhr_box_pb_group_settings(settings_string, charset_flag, group, previous=None):
        try:
            validator = UhrBoxPBGroupSettingsStringValidator()
            settings_dict = validator.validate(settings_string, charset_flag, group, previous)
        except UhrBoxPBSettingsStringError as e:
            raise e
        else:
            return settings_dict

    def valid_uhr_box_pb_settings(settings_string, charset_flag):
        try:
            validator = UhrBoxPBSettingsValidator()
            settings_dict = validator.validate(settings_string, charset_flag)
        except UhrBoxPBSettingsStringError as e:
            raise e
        else:
            return settings_dict

    def valid_uhr_box_plug_id(plug_id, group):
        try:
            plug_id = valid_uhr_box_plug_id(plug_id, group)
        except UhrBoxPlugIDError as e:
            raise e
        else:
            return plug_id
