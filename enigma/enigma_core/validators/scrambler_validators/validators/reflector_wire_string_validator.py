from enigma_core.settings.settings import LETTERS, NUMBERS
import re


class ReflectorWireStringError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class ReflectorWireStringValidator:

    def __init__(self):
        self._charset_flag = None

    def validate(self, wire_string, charset_flag):

        self._set_charset(charset_flag)

        

        # create pattern
        pattern = self._create_pattern()
        # extract data from string
        wire_list = self._extract_wire_list(pattern, wire_string)
        # check wire list exists
        self._check_wire_list_exists(wire_list, wire_string)
        # check length
        self._valid_wire_list_length(wire_list)
        # check valid characters
        wire_list = self._valid_wire_characters(wire_list)
        # check for unique characters
        self._unique_characters(wire_list)
        # check not self wired
        self._check_not_self_wired(wire_list)

        return wire_list
    
    def _set_charset(self, charset_flag):
        """
        
        """
        if charset_flag == "L":
            self._charset_flag = "L"
            self._charset = LETTERS
        elif charset_flag == "N":
            self._charset_flag = "N"
            self._charset = NUMBERS
        else:
            err_msg = f"{charset_flag} is not a valid charset flag."
            raise Exception(err_msg)
        
    def _create_pattern(self):
        """
        
        """
        if self._charset_flag == "L":
            return "[a-zA-Z]"
        elif self._charset_flag == "N":
            return "[0-9]+"
        
    def _extract_wire_list(self, pattern, wire_string):
        """
        
        """
        regex = re.compile(pattern)
        wire_list = re.findall(regex, wire_string)
        wire_list = [c.upper() for c in wire_list]

        return wire_list
    
    def _check_wire_list_exists(self, wire_list, wire_string):
        """
        
        """
        if not wire_list:
            err_msg = f"{wire_string} is not a valid wire list."
            raise ReflectorWireStringError(err_msg)
    
    def _valid_wire_list_length(self, wire_list):
        """
        
        """
        if len(wire_list) != 26:
            err_msg = f"Wire list is length {len(wire_list)}. Wire list must contain 26 characters."
            raise ReflectorWireStringError(err_msg)
    
    def _valid_wire_characters(self, wire_list):
        """
        
        """
        valid_wire_chars = []

        format = "A-Z" if self._charset_flag == "L" else "01-26"

        for wire_char in wire_list:
            if self._charset_flag == "N":
                wire_char = wire_char.rjust(2,"0")
            if wire_char not in self._charset:
                err_msg = f"{wire_char} is not a valid wire character. Must be in range {format}."
                raise ReflectorWireStringError(err_msg)
            else:
                valid_wire_chars.append(wire_char)

        return valid_wire_chars

    def _check_not_self_wired(self, wire_list):
        """
        
        """
        for wire_char in wire_list:
            if wire_list.index(wire_char) == self._charset.index(wire_char):
                err_msg = f"Wire char {wire_char} is self wired."
                raise ReflectorWireStringError(err_msg)

    def _unique_characters(self, wire_list):
        """
        
        """
        for wire_char in wire_list:
            if wire_list.count(wire_char) != 1:
                err_msg = f"Wire char {wire_char} is repeated. All wire chars must be unique."
                raise ReflectorWireStringError(err_msg)
