from enigma_core.settings.settings import LETTERS, NUMBERS
from collections import deque
from enigma_core.scrambler.exceptions.exceptions import (RingCharacterError,
                                                         RotorInputIndexError,
                                                         CharacterSetFlagError,
                                                         WiringError,
                                                         TurnoverListError)


class Rotor:
    """
    
    """

    POSITIONS = 26

    def __init__(self,
            rotor_id,
            wiring_characters,
            turnover_characters =None,
            charset_flag ='L'
        ):
        """
        Takes a string value for the rotor id, wiring characters list, 
        optional turnover characters list and optional character set flag
        of 'L' or 'N' defaults to 'L'.
        """
        self._rotor_id = rotor_id
        self._rng_offset = 0
        self._rot_offset = 0
        self._charset_flag = None
        self._charset = None
        self.character_set_flag = charset_flag
        self._lh_translation_map = {}
        self._rh_translation_map = {}
        self._wire_chars = self._valid_wiring(wiring_characters, True)
        self._turn_chars = self._valid_turnover_chars(turnover_characters)
        self._make_translation_maps()

    def __repr__(self):
        """
        Returns a string with the 'ROTOR_ID' 'RING CHARACTERS'
        'WIRING CHARACTERS' and 'TURNOVER CHARACTERS'. The parameters
        are the same as those used to initialize the rotor.
        """

        rot_str = (f"ROTOR ID : {self._rotor_id}\n"
                   f"RING CHARACTERS : {self.ring_characters}\n"
                   f"WIRING CHARACTERS : {self._wire_chars}\n"
                   f"TURNOVER CHARACTERS : {self.turnover_characters}\n")

        rot_str += "LH_TRANSLATION_TABLE\n"
        for position, translation in self._lh_translation_map.items():
            trans_str = ""
            for i in translation:
                trans_str += f"{self._charset[i]} "
            rot_str += f"{str(position).rjust(2, '0')} {trans_str}\n"

        rot_str += "RH_TRANSLATION_TABLE\n"
        for position, translation in self._rh_translation_map.items():
            trans_str = ""
            for i in translation:
                trans_str += f"{self._charset[i]} "
            rot_str += f"{str(position).rjust(2, '0')} {trans_str}\n"

        return rot_str

    def __str__(self):
        """
        Returns a string with the 'ROTOR ID' 'ROTOR SETTING'
        'RING SETTING' 'RING CHARACTERS' 'WIRING CHARACTERS'
        and 'TURNOVER CHARACTERS'. The rotor setting and ring
        setting are the current settings. The rest of the 
        parameters are the same as those used to initialize
        the rotor.
        """
        def list_to_string(list_):
            return ','.join(['{:<2}'.format(char) for char in list_])

        return (f"ROTOR ID -----------: {self._rotor_id}\n"
                f"ROTOR SETTING ------: {self.rotor_setting}\n"
                f"RING SETTING -------: {self.ring_setting}\n"
                f"RING CHARACTERS ----: {list_to_string(self.ring_characters)}\n"
                f"WIRING CHARACTERS --: {list_to_string(self.wiring_characters)}\n"
                f"TURNOVER CHARACTERS : {list_to_string(self.turnover_characters)}\n")

    @property
    def device_id(self):
        """
        Returns the device id from the rotor core.
        """
        return self._rotor_id

    @property
    def rotor_id(self):
        """
        Returns the device id from the rotor core.
        """
        return self._rotor_id

    @property
    def flag(self):
        """
        Returns the rotating rotor 'R_ROT' or fixed rotor 'F_ROT' flag for 
        this rotor.
        """
        return "R_ROT" if self.can_turnover() else "F_ROT"

    @property
    def turnover_characters(self):
        """
        Returns a list of turnover characters or an empty list if no turnover.
        """
        return [self._charset[i] for i in self._turn_chars]

    def can_turnover(self):
        """
        Returns a boolean value indicating if the rotor can be turned over
        by the stepping mechanism for the current rotor setting.
        """
        return True if len(self._turn_chars) != 0 else False

    def on_turnover(self):
        """
        Returns a boolean reflecting if the rotor is at a rotor setting which
        will allow it to turn over.
        """
        return True if self.rotor_setting in self.turnover_characters else False

    def keyed_rotor(self):
        """
        Increments the the rotor setting one step and returns the on_turnover
        state before the rotor setting was incremented.
        """
        turnover = self.on_turnover()
        self.inc_rotor_setting()
        return turnover

    @property
    def ring_characters(self):
        """
        Returns the ring characters list.
        """
        return self._charset

    @property
    def rotor_setting(self):
        """
        Returns the current rotor setting.
        """
        return self._charset[self._rot_offset]

    @rotor_setting.setter
    def rotor_setting(self, rotor_setting):
        """
        Takes a rotor setting and sets that value if valid.
        """
        rotor_setting = self.valid_ring_character(rotor_setting)
        self._rot_offset = self._charset.index(rotor_setting)

    @property
    def ring_setting(self):
        """
        Returns the current ring setting.
        """
        return self._charset[self._rng_offset]

    @ring_setting.setter
    def ring_setting(self, ring_setting):
        """
        Takes a ring setting and sets that value if valid.
        """
        ring_setting = self.valid_ring_character(ring_setting)
        self._rng_offset = self._charset.index(ring_setting)

    def valid_ring_character(self, character):
        """
        Returns a valid ring character or raises RotorRingCharacterError
        if not a valid ring character.
        """
        if character in self._charset:
            return character
        else:
            msg = f"{character} is not a valid ring character."
            raise RingCharacterError(msg)

    def inc_rotor_setting(self):
        """
        Increments the rotor setting by one step.
        """
        self._rot_offset = self._change_offset(self._rot_offset, 1)

    def dec_rotor_setting(self):
        """
        Decrements the rotor setting by one step.
        """
        self._rot_offset = self._change_offset(self._rot_offset, -1)

    def inc_ring_setting(self):
        """
        Increments the ring setting by one step.
        """
        self._rng_offset = self._change_offset(self._rng_offset, 1)

    def dec_ring_setting(self):
        """
        Decrements the ring setting by one step.
        """
        self._rng_offset = self._change_offset(self._rng_offset, -1)

    def reset_rotor(self):
        """
        Resets the ring and rotor settings to their default values
        which is the same values they had at rotor initialization.
        """
        self._rng_offset = 0
        self._rot_offset = 0

    def default_rotor_setting(self):
        """
        Resets rotor setting to its default value which is the value
        it had at rotor initialization.
        """
        self._rot_offset = 0

    def core_offset(self):
        """
        Returns the rotor core offset.
        """
        offset = self._rot_offset - self._rng_offset
        if offset < 0:
            offset = offset + 26
        return offset
    
    def current_ring_characters(self):
        """
        
        """
        ring_chars = deque(self._charset)
        ring_chars.rotate(self._rng_offset)
        ring_chars = list(ring_chars)
        return ring_chars

    def _change_offset(self, value, direction):
        """
        Returns a new offset value within the limits of the rotor positions.
        """
        if direction == 1:
            if value >= self.POSITIONS-1:
                value = 0
            else:
                value += 1
        elif direction == -1:
            if value == 0:
                value = self.POSITIONS-1
            else:
                value -= 1
        return value
    
    @property
    def device_id(self):
        """
        Returns the device id.
        """
        return self._rotor_id

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
            translation = None
            if flag == 'L' and self._charset_flag == 'N':
                translation = { NUMBERS[i] : LETTERS[i] for i in range(26)}
            elif flag == 'N' and self._charset_flag == 'L':
                translation = { LETTERS[i] : NUMBERS[i] for i in range(26)}
            if hasattr(self, '_wire_chars') and translation:
                self._wire_chars = [translation[l] for l in self._wire_chars]
            self._charset_flag = flag
            self._charset = LETTERS if flag == 'L' else NUMBERS
        else:
            raise CharacterSetFlagError(flag)

    @property
    def wiring_characters(self):
        """
        Returns a list of the wiring characters.
        """
        return self._wire_chars

    @property
    def rotor_dict(self):
        """
        Returns a dictionary object with 'ROTOR_TYPE' 'ROTOR_SETTING'
        'RING_SETTING' 'RING_CHARACTERS' 'ROTOR_CHARACTERS' and
        'TURNOVER_CHARACTERS'. The ring characters list and rotor characters
        list are shifted to reflect there current values for the current ring
        and rotor settings.
        """
        return {
            "ROTOR_TYPE": self.device_id,
            "ROTOR_SETTING": self.rotor_setting,
            "RING_SETTING": self.ring_setting,
            "RING_CHARACTERS": self.current_ring_characters(),
            "WIRING_CHARACTERS": self.current_wiring_characters(),
            "TURNOVER_CHARACTERS": self.turnover_characters
            }

    def lh_output(self, index):
        """
        Returns an integer value for the output index for the left hand 
        output of the rotor core.
        """
        if self.valid_input_index(index):
            offset = self.core_offset()
            return self._lh_translation_map[offset][index]

    def rh_output(self, index):
        """
        Returns an integer value for the output index for the right hand
        output of the rotor core.
        """
        if self.valid_input_index(index):
            offset = self.core_offset()
            return self._rh_translation_map[offset][index]

    def valid_input_index(self, index):
        """
        Takes an index integer value and returns True if valid else raises
        a RotorInputIndexError.
        """
        if index not in range(26):
            msg = f"{index} is not a valid index for rotor {self._rotor_id}"
            raise RotorInputIndexError(msg)
        else:
            return True

    def current_wiring_characters(self):
        """
        Returns a list of wiring characters that are offset to the current 
        core offset.
        """
        char_map = { i : self._charset[i] for i in range(26) }
        return [char_map[i] for i in self._lh_translation_map[self.core_offset()]]

    def _make_translation_maps(self):
        """
        Makes the translation maps for left hand and right hand output.
        Each translation map maps rotor core position to an integer list
        of the output indexes for that rotor core position.
        """
        lh_translation_map = {}
        rh_translation_map = {}

        connections = deque(self._wire_chars)
        letters = deque(self._charset)

        for i in range(26):
            lh_translation_arr = [letters.index(l) for l in connections]
            rh_translation_arr = [connections.index(l) for l in letters]
            lh_translation_map[i] = lh_translation_arr
            rh_translation_map[i] = rh_translation_arr
            connections.rotate(-1)
            letters.rotate(-1)
        self._lh_translation_map = lh_translation_map
        self._rh_translation_map = rh_translation_map
    
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
    
    def _valid_turnover_chars(self, turnover_chars):
        if not turnover_chars:
            return []
        for char in turnover_chars:
           if char not in self._charset:
               raise TurnoverListError(f"")
        turnovers = [self._charset.index(c) for c in turnover_chars]

        return turnovers