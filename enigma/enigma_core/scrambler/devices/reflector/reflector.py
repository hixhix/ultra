
from enigma_core.settings.settings import LETTERS, NUMBERS
from enigma_core.scrambler.exceptions.exceptions import ReflectorIndexError, CharacterSetFlagError, WiringError


class Reflector:
    """
    
    """

    def __init__(self, reflector_id, wiring_characters, rewireable, charset_flag ='L'):
        """

        """
        self._charset = None
        self._charset_flag = None
        self.character_set_flag = charset_flag
        self._reflector_id = reflector_id
        self.rewireable = rewireable
        self._flag = "REF"
        self._translation_array = None
        self._wire_chars = self._valid_wiring(wiring_characters, self_wired=False)
        self._make_translation_array()

    def __repr__(self):
        """
        Returns the string repressentation of the reflector.
        """
        return self.reflector_id

    def __str__(self):
        """
        Returns a string with the reflector id and wiring characters.
        """
        def list_to_string(list_):
            return ','.join(['{:<2}'.format(char) for char in list_])

        return (f"REFLECTOR_ID -------: {self.reflector_id}\n"
                f"WIRING CHARACTERS --: {list_to_string(self.wire_characters)}\n")
    
    @property
    def device_id(self):
        """
        Returns the device id.
        """
        return self._reflector_id

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
    
    def set_wiring(self, wire_list):
        """
        
        """
        if self.rewireable:
            try:
                self._wire_chars = self._valid_wiring(wire_list)
            except WiringError as e:
                raise e
            else:
                self._make_translation_array()
        else:
            raise Exception(f"{self.reflector_id} is not a rewireable reflector.")

    @property
    def flag(self):
        """
        Returns the reflectors flag.
        """
        return self._flag

    @property
    def reflector_id(self):
        """
        Returns the device id.
        """
        return self._reflector_id

    @property
    def wire_characters(self):
        """
        Returns the list of wiring characters.
        """
        return [self._charset[i] for i in self._translation_array]

    def output(self, index):
        """
        Takes an index integer and returns the output index integer from the
        translation array.
        """
        try:
            return self._translation_array[index]
        except IndexError:
            raise ReflectorIndexError(index)

    def _make_translation_array(self):
        """
        Makes the translation array to convert the reflector input index to
        an output index.
        """
        self._translation_array = [self._charset.index(l) for l in self._wire_chars]

    def _valid_wiring(self, wiring_list, self_wired=False):
        """
        
        """
        # check is list
        if type(wiring_list) != list:
            msg = (f"{self.device_id} wire list is type "
                   f"{type(wiring_list)}. Must be type list")
            raise WiringError(msg)

        # check list is correct length
        if len(wiring_list) != len(self._charset):
            msg = (f"{self.device_id} wire list is length {len(wiring_list)}. "
                   f"Must be length {len(self._charset)}")
            raise WiringError(msg)

        # check for invalid characters
        invalid_chars = [c for c in wiring_list if c not in self._charset]
        if invalid_chars:
            msg = (f"Invalid character(s) '{','.join(invalid_chars)}' "
                   f"in wiring for {self.device_id}. "
                   f"Wiring list must contain characters A-Z.")
            raise WiringError(msg)

        # check for duplicate characters
        duplicate = [c for c in wiring_list if wiring_list.count(c) > 1]
        duplicate = list(set(duplicate))
        if duplicate:
            msg = (f"Duplicate character(s) '{','.join(duplicate)}'"
                   f" in wiring list for {self.device_id}")
            raise WiringError(msg)
        
        # check for self wired if applicable
        self_wired_chars = [c for i, c in enumerate(wiring_list) if c == self._charset[i]]
        if not self_wired and self_wired_chars:
            msg = (f"Character(s) '{','.join(self_wired_chars)}' are "
                   f"self wired for {self.device_id}. Self wired "
                   f"characters are not permitted for this device.")
            raise WiringError(msg)

        return wiring_list