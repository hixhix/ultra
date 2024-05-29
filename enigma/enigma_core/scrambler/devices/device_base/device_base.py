from enigma_core.settings.settings import LETTERS, NUMBERS
from enigma_core.scrambler.exceptions.exceptions import CharacterSetFlagError


class DeviceBase:

    def __init__(self, device_id, charset_flag):
        """
        Takes a device id and optional character set flag which defaults to 'L'.
        """
        self._device_id = device_id
        self._charset = None
        self._charset_flag = None
        self.character_set_flag = charset_flag

    @property
    def device_id(self):
        """
        Returns the device id.
        """
        return self._device_id

    def character_set(self):
        """
        Returns the character set list.
        """
        return self._charset

    @property
    def character_set_flag(self):
        """
        Returns the current character set flag.
        """
        return self._charset_flag

    @character_set_flag.setter
    def character_set_flag(self, flag):
        """
        Takes a character set flag for the device to use. If flag is not valid
        raises a CharacterSetFlagError.
        """
        if flag in ["L","N"]:
            if hasattr(self, '_wire_chars'):
                translation = None
                if flag == 'L' and self._charset_flag == 'N':
                    translation = { NUMBERS[i] : LETTERS[i] for i in range(26)}
                elif flag == 'N' and self._charset_flag == 'L':
                    translation = { LETTERS[i] : NUMBERS[i] for i in range(26)}
                if translation:
                    wire_list = [translation[l] for l in self._wire_chars]
                    self._wire_chars = wire_list
            self._charset_flag = flag
            self._charset = LETTERS if flag == 'L' else NUMBERS
        else:
            raise CharacterSetFlagError(flag)
