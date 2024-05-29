from enigma_core.settings.settings import NUMBERS, LETTERS
import re


class RingSettingsStringError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class RingSettingsStringValidator:

    POSITIONS = ["RF","RM","RS","R4"]

    def __init__(self):
        self.settings_string = None
        self.charset_flag = None
        self.positions = None

    def validate(self, settings_string, charset_flag, positions):
        self.settings_string = settings_string

        self._valid_charset_flag(charset_flag)
        self._valid_positions(positions)
        pattern = self._create_pattern()
        settings = self._extract_settings(pattern)
        settings = self._valid_settings(settings)
        output_dict = self._make_output_dict(settings)

        return output_dict

    def _valid_charset_flag(self, charset_flag):
        charset_flag = charset_flag.upper()
        if charset_flag not in ["L","N"]:
            err_msg = f"{charset_flag} is not a valid charset flag. Must be 'L' or 'N'."
            raise Exception(err_msg)
        else:
            self.charset_flag = charset_flag
        
    def _valid_positions(self, positions):
        if positions < 1 or positions > 4:
            err_msg = f"{positions} is an invalid value for positions. Must be in range 1-4."
            raise Exception(err_msg)
        else:
            self.positions = positions

    def _create_pattern(self):
        if self.charset_flag == "L":
            pattern = "[a-zA-Z]"
        elif self.charset_flag == "N":
            pattern = "[0-9]+"
        return pattern

    def _extract_settings(self, pattern):
        regex = re.compile(pattern)
        ring_settings = re.findall(regex, self.settings_string)
        ring_settings = [c.upper() for c in ring_settings]
        return ring_settings

    def _valid_settings(self, settings):
        settings_range = "'A-Z'" if self.charset_flag == "L" else "'01-26'"

        if not settings:
            err_msg = f"{self.settings_string} are not valid ring settings. Must be in range {settings_range}."
            raise RingSettingsStringError(err_msg)

        valid_settings = []

        if len(settings) != self.positions:
            err_msg = f"{self.settings_string} are not valid ring settings. Must be in range {settings_range}."
            raise RingSettingsStringError(err_msg)
        if self.charset_flag == "N":
            for ring_setting in settings:
                _ring_setting = ring_setting.rjust(2,'0')
                if _ring_setting not in NUMBERS:
                    err_msg = f"Invalid ring setting {ring_setting}. Must be a number in range {settings_range}."
                    raise RingSettingsStringError(err_msg)
                else:
                    valid_settings.append(_ring_setting)
        if self.charset_flag == "L":
            for ring_setting in settings:
                valid_settings.append(ring_setting)

        return valid_settings

    def _make_output_dict(self, settings):
        output_dict = {}

        settings.reverse()

        for i in range(self.positions):
            output_dict[self.POSITIONS[i]] = settings[i]

        return output_dict
