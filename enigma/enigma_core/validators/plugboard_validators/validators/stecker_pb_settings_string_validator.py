import re


class SteckerPBSettingsStringError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class SteckerPBSettingsStringValidator:

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{i+1}".rjust(2,'0') for i in range(26)]

    def __init__(self):
        self.settings_string = None
        self.charset_flag = None
        self.pairs = None

    def validate(self, settings_string, charset_flag, pairs=None):
        """
        Takes a stecker plugboard settings string. Can be in the form "AB,CD,EF,GH" or
        "AB CD EF GH" or "01,02 03,04" or "1,2 3,4 5,6 7,8". Return a settings dictionary
        with valid plugboard settings. If not valid raises a SteckerPBSettingsStringError.
        {
            "PLUGBOARD_CONNECTIONS":{
                "A":"B","B":"A","C":"D","D":"C",
                "E":"F","F":"E","G":"H","H":"G",
                "I":"J","J":"I","K":"L","L":"K",
                "M":"N","N":"M","O":"P","P":"O",
                "Q":"R","R":"Q","S":"T","T":"S",
                "U":"U","V":"V","W":"W","X":"X",
                "Y":"Y","Z":"Z"
            },
            "PLUGBOARD_MODE":"S",
            "PLUGBOARD_CHARSET_FLAG":"L" 
        }
        """
        self.settings_string = settings_string
        self._valid_charset_flag(charset_flag)
        self._valid_pairs(pairs)
        pattern = self._create_regex_pattern()
        pb_settings = self._extract_socket_ids(pattern)
        if not pb_settings:
            connections_dict = self._make_connections_dict([])
        else:
            pb_settings = self._format_letters_settings(pb_settings)
            pb_settings = self._format_numbers_settings(pb_settings)
            self._valid_socket_ids(pb_settings)
            self._complete_pairs(pb_settings)
            pairs_list = self._make_pairs(pb_settings)
            pairs_list = self._remove_recipricol_pairs(pairs_list)
            self._check_for_contradictions(pairs_list)
            self._check_for_number_of_pairs(pairs_list)
            connections_dict = self._make_connections_dict(pairs_list)
  
        return connections_dict 

    def _valid_charset_flag(self, charset_flag):
        charset_flag = charset_flag.upper()
        if charset_flag not in ["L","N"]:
            raise Exception(f"{charset_flag} is not a valid charset_flag. Must be 'L' or 'N'.")
        self.charset_flag = charset_flag

    def _valid_pairs(self, pairs):
        if pairs and (pairs < 0 or pairs > 10):
            err_msg = f""
            raise Exception(err_msg)
        else:
            self.pairs = pairs

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
        
    def _format_letters_settings(self, pb_settings):
        if self.charset_flag == "L":
            socket_id_str = ""
            for string in pb_settings:
                for c in string:
                    socket_id_str += c
            return [c for c in socket_id_str]
        else:
            return pb_settings

    def _format_numbers_settings(self, pb_settings):
        if self.charset_flag == "N":
            for socket_id in pb_settings:
                if len(socket_id) == 1 and socket_id not in ["1","2","3","4","5","6","7","8","9"]:
                    err_msg = f"Invalid socket id {socket_id} in lugboard connections {self.settings_string}."
                    raise SteckerPBSettingsStringError(err_msg)
                
            return [f"{c}".rjust(2,'0') for c in pb_settings]
        else:
            return pb_settings

    def _valid_socket_ids(self, pb_settings):
        for socket_id in pb_settings:
            err_msg = None
            if (self.charset_flag == "L" and socket_id not in self.LETTERS) or (self.charset_flag == "N" and socket_id not in self.NUMBERS):
                err_msg = f"Invalid socket id {socket_id} in plugboard settings {self.settings_string}."
            if err_msg:
                raise SteckerPBSettingsStringError(err_msg)

    def _complete_pairs(self, pb_settings):
        if len(pb_settings) % 2 != 0:
            err_msg = f"Incomplete plugboard pairs in {self.settings_string}"
            raise SteckerPBSettingsStringError(err_msg)
                
    def _check_for_contradictions(self, pairs_list):
        used = {}

        err_msg = None

        for pair in pairs_list:
            c1 = pair[0]
            c2 = pair[1]
            if c1 in used.keys() and used[c1] != c2:
                err_msg = f"Socket id {c1} is connected to socket {c2} and socket {used[c1]} in plugboard connections {self.settings_string}."
            if c2 in used.keys() and used[c2] != c1:
                err_msg = f"Socket id {c2} is connected to socket {c1} and socket {used[c2]} in plugboard connections {self.settings_string}."
            if err_msg:
                raise SteckerPBSettingsStringError(err_msg)
            else:
                used[c1] = c2
                used[c2] = c1
                
    def _make_pairs(self, pb_settings):
        pairs_list = []

        for i in range(int(len(pb_settings) / 2)):
            pair = []
            pair.append(pb_settings.pop())
            pair.append(pb_settings.pop())
            pairs_list.append(pair)

        return pairs_list
        
    def _remove_recipricol_pairs(self, pairs_list):
        pairs = []

        for pair in pairs_list:
            c1 = pair[0]
            c2 = pair[1]
            if [c1,c2] not in pairs or [c2,c1] not in pairs:
                pairs.append([c1,c2])

        return pairs
        
    def _check_for_number_of_pairs(self, pairs_list):
        if self.pairs and len(pairs_list) != self.pairs:
            err_msg = f"{self.pairs} plugboard pairs required. {len(pairs_list)} given in {self.settings_string}."
            raise SteckerPBSettingsStringError(err_msg)
        
    def _make_connections_dict(self, pairs_list):
        connections_dict = None
        if self.charset_flag == "L":
            connections_dict = {chr(i):chr(i) for i in range(65, 91)}
        elif self.charset_flag == "N":
            connections_dict = {f"{str(i+1).rjust(2,'0')}":f"{str(i+1).rjust(2,'0')}" for i in range(26)}

        for pair in pairs_list:
            c1 = pair[0]
            c2 = pair[1]
            connections_dict[c1] = c2
            connections_dict[c2] = c1

        connections_dict = {
            "PLUGBOARD_CONNECTIONS":connections_dict,
            "PLUGBOARD_MODE":"S",
            "PLUGBOARD_CHARSET_FLAG":f"{self.charset_flag}"
        }

        return connections_dict
