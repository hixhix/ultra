from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS
from enigma_core.keyboard.keyboard import Keyboard
from enigma_core.scrambler.scrambler.scrambler import Scrambler
from enigma_core.plugboard.stecker_plugboard import SteckerPlugboard
from enigma_core.plugboard.uhr_box_plugboard import UhrBoxPlugboard


class Enigma:

    def __init__(self,
            machine_type,
        ):

        self.machine_type = machine_type
        self.keyboard = Keyboard()
        self.scrambler = None
        self.plugboard = None
        self._init_plugboard()
        self._init_scrambler()

    def __str__(self):
        _str = f"{' '*16}{self.machine_type}\n\n"
        _str += self.scrambler.__str__()
        _str += '\n\n'
        _str += self.plugboard.__str__()
        _str += '\n'
        return _str
    
    def _init_scrambler(self):
        """
        
        """
        charset_flag = EQUIPMENT_DICT[self.machine_type]["DEFAULT_MODES"]["SCRAMBLER"]

        self.scrambler = Scrambler(self.machine_type, charset_flag)

    def _init_plugboard(self):
        """
        
        """
        charset_flag = EQUIPMENT_DICT[self.machine_type]["DEFAULT_MODES"]["PLUGBOARD"]

        self.set_plugboard_mode("S", charset_flag)
        
    def set_plugboard_mode(self, mode, plugboard_char_flag='L'):
        """
        
        """
        if mode not in ['S','U']:
            msg = f"{mode} is not a valid plugboard mode. Must be 'S' or 'U'"
            raise ValueError(msg)
        if self.plugboard:
            if mode == 'S' and self.plugboard.plugboard_mode == 'U':
                self.plugboard = SteckerPlugboard(plugboard_char_flag)
            elif mode == 'U' and self.plugboard.plugboard_mode == 'S':
                self.plugboard = UhrBoxPlugboard(plugboard_char_flag)
        elif not self.plugboard:
            if mode == 'S': self.plugboard = SteckerPlugboard(plugboard_char_flag)
            elif mode == 'U': self.plugboard = UhrBoxPlugboard(plugboard_char_flag)

    def character_input(self, char):
        """

        """
        try:
            index = self.keyboard.character_input(char)
        except ValueError:
            return None
        else:
            index = self.integer_input(index)
            return LETTERS[index]
        
    def non_keyed_input(self, char):
        """
        
        """
        try:
            index = self.keyboard.character_input(char)
        except ValueError:
            return None
        else:
            index = self.plugboard.lg_contact_output(index)
            index = self.scrambler.output(index)                
            index = self.plugboard.sm_contact_output(index)    
            return LETTERS[index]

    def integer_input(self, index):
        """

        """
        index = self.plugboard.lg_contact_output(index)
        index = self.scrambler.keyed_input(index)
        index = self.plugboard.sm_contact_output(index)
        return index

    def valid_enigma(self):
        """

        """
        return self.scrambler.valid_scrambler() and self.plugboard.valid_plugboard()

    def set_default_settings(self) -> None:
        """

        """
        self.scrambler.default_settings()
        self.plugboard.clear()

    def clear_enigma(self):
        """
        
        """
        self.scrambler.clear_scrambler()
        self.plugboard.clear()

    @property
    def settings(self):
        """

        """
        settings_dict = {}
        settings_dict["MACHINE_TYPE"] = self.machine_type
        settings_dict["SCRAMBLER_SETTINGS"] = self.scrambler.settings
        settings_dict["PLUGBOARD_SETTINGS"] = self.plugboard.settings

        return settings_dict

    @settings.setter
    def settings(self, settings):
        """
        
        """
        self.scrambler.settings = settings["SCRAMBLER_SETTINGS"]
        try:
            self.set_plugboard_mode(settings['PLUGBOARD_SETTINGS']["PLUGBOARD_MODE"])
        except Exception:
            pass
        else:
            self.plugboard.settings = settings["PLUGBOARD_SETTINGS"]

