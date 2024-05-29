from enigma_core.settings.settings import LETTERS, NUMBERS


class RingCharacterError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class RingCharacterValidator:

    def __init__(self):
        pass

    def validate(self, ring_character, charset_flag):
        charset_flag = self._valid_charset_flag(charset_flag)

        err_msg = None

        if charset_flag == "L":
            ring_character = ring_character.upper()
            if ring_character not in LETTERS:
                err_msg = f"{ring_character} is not a valid letters ring character. Must be A-Z."
        elif charset_flag == "N":
            _ring_character = ring_character.rjust(2,'0')
            if _ring_character not in NUMBERS:
                err_msg = f"{ring_character} is not a valid number ring character. Must be 01-26."

        if err_msg:
            raise RingCharacterError(err_msg)
        else:
            return ring_character

    def _valid_charset_flag(self, charset_flag):
        charset_flag = charset_flag.upper()
        if charset_flag not in ["L","N"]:
            err_msg = f"{charset_flag} is not a valid charset flag. Must be 'L' or 'N'."
            raise Exception(err_msg)
        else:
            return charset_flag
