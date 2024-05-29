import re


class UhrBoxPBSettingsStringError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class UhrBoxPBGroupSettingsStringValidator():

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{i+1}".rjust(2,'0') for i in range(26)]

    def __init__(self):
        self.charset_flag = None
        self.group = None

    def validate(self, settings_string, charset_flag, group, previous=None):
        """
        Takes an uhr box plugboard settings group string. Can be in the following forms
        "A B C D E F G H I J K" or "01 02 03 04 05 06 07 08 09 10" or "1,2,3,4,5,6,7,8,9,10".
        Can be space or comma seperated. A group argument of "A" or "B" is required to
        determine which uhr box plug group these settings will be assigned. If this is the
        second group then the previous group needs to be provided to check for consistency.
        Returns a connections dictionary. If not valid raises an UhrBoxPBSettingsStringError.
        {
            "PLUGBOARD_CONNECTIONS":{
                "01A":"A","02A":"B",
                "03A":"C","04A":"D",
                "05A":"E","06A":"F",
                "07A":"G","08A":"H",
                "09A":"I","10A":"J"
            },
            "PLUGBOARD_MODE":"U",
            "PLUGBOARD_CHARSET_FLAG":"L",
            "GROUP":"A"
        }
        """
        self.settings_string = settings_string
        self.previous = previous
        self._valid_charset_flag(charset_flag)
        self._valid_group(group)
        pattern = self._create_regex_pattern()
        pb_settings = self._extract_socket_ids(pattern)
        self._check_pb_settings_exist(pb_settings)
        pb_settings = self._format_number_settings(pb_settings)
        self._valid_socket_ids(pb_settings)
        self._check_for_10_socket_ids(pb_settings)
        self._check_for_unique_socket_ids(pb_settings)
        self._check_previous(pb_settings)
        connections_dict = self._make_connections_dict(pb_settings)

        return connections_dict

    def _valid_charset_flag(self, charset_flag):
        charset_flag = charset_flag.upper()
        if charset_flag not in ["L","N"]:
            raise Exception(f"{charset_flag} is not a valid charset_flag. Must be 'L' or 'N'.")
        self.charset_flag = charset_flag
            
    def _valid_group(self, group):
        group = group.upper()
        if group not in ["A","B"]:
            raise Exception(f"{group} is not a valid group id. Must be 'A' or 'B'.")
        else:
            self.group = group
            
    def _create_regex_pattern(self):
        if self.charset_flag == "L":
            pattern = "[a-zA-Z]+"
        elif self.charset_flag == "N":
            pattern = "[0-9]+"
        return pattern
        
    def _extract_socket_ids(self, pattern):
        regex = re.compile(pattern)
        pb_settings = re.findall(regex, self.settings_string)
        pb_settings = [c.upper() for c in pb_settings]
        return pb_settings
        
    def _check_pb_settings_exist(self, pb_settings):
        if not pb_settings:
            err_msg = f""
            raise UhrBoxPBSettingsStringError(err_msg)
            
    def _format_number_settings(self, pb_settings):
        if self.charset_flag == "N":
            for socket_id in pb_settings:
                if len(socket_id) == 1 and socket_id not in ["1","2","3","4","5","6","7","8","9"]:
                    err_msg = f"Invalid socket id {socket_id} in lugboard connections {self.settings_string}."
                    raise UhrBoxPBSettingsStringError(err_msg)
                
            return [f"{c}".rjust(2,'0') for c in pb_settings]
        else:
            return pb_settings    

    def _valid_socket_ids(self, pb_settings):
        for socket_id in pb_settings:
            err_msg = None
            if (self.charset_flag == "L" and socket_id not in self.LETTERS) or (self.charset_flag == "N" and socket_id not in self.NUMBERS):
                err_msg = f"Invalid socket id {socket_id} in plugboard settings {self.settings_string}."
            if err_msg:
                 raise UhrBoxPBSettingsStringError(err_msg)
                
    def _check_for_10_socket_ids(self, pb_settings):
        if len(pb_settings) != 10:
            err_msg = f""
            raise UhrBoxPBSettingsStringError(err_msg)
            
    def _check_for_unique_socket_ids(self, pb_settings):
        for socket_id in pb_settings:
            if pb_settings.count(socket_id) > 1:
                err_msg = f""
                raise UhrBoxPBSettingsStringError(err_msg)

    def _check_previous(self, pb_settings):
        if not self.previous:
            return
        if self.previous["GROUP"] == self.group:
            err_msg = f""
            raise UhrBoxPBSettingsStringError(err_msg)
            
        for _, socket_id in self.previous["PLUGBOARD_CONNECTIONS"].items():
            if socket_id in pb_settings:
                err_msg = f""
                raise UhrBoxPBSettingsStringError(err_msg)
                
    def _make_connections_dict(self, pb_settings):
        connections = {}

        for i in range(10):
            connections[f"{str(i+1).rjust(2,'0')}{self.group}"] = pb_settings[i]

        connections_dict = {
            "PLUGBOARD_CONNECTIONS":connections,
            "GROUP":self.group,
            "PLUGBOARD_MODE":"U",
            "PLUGBOARD_CHARSET_FLAG":self.charset_flag
        }

        return connections_dict
