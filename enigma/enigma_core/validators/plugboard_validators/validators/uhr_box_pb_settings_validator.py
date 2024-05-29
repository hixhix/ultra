import re


class UhrBoxPBSettingsStringError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class UhrBoxPBSettingsValidator:

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{i+1}".rjust(2,'0') for i in range(26)]

    def __init__(self):
        self.setttings_string = None
        self.charset_flag = None

    def validate(self, settings_string, charset_flag):
        """
        Takes an uhr box plugboard settings string. Can be in the following forms 
        "A=[A,B,C,D,E,F,G,H,I,J] B=[K,L,M,N,O,P,Q,R,S,T]" 
        number mode in format "A=[1,2,3,4,5,6,7,8,9,10] B=[11,12,13,14,15,16,17,18,19,20]".
        Can be space or comma seperated. Returns a connections dictionary. If not valid
        raises an UhrBoxPBSettingsStringError.
        {
            "PLUGBOARD_CONNECTIONS":{
                "01A":"A","02A":"B",
                "03A":"C","04A":"D",
                "05A":"E","06A":"F",
                "07A":"G","08A":"H",
                "09A":"I","10A":"J",
                "01B":"K","02B";"L",
                "03B":"M","04B";"N",
                "05B":"O","06B":"P",
                "07B":"Q","08B":"R",
                "09B":"S","10B":"T"
            },
            "PLUGBOARD_MODE":"U",
            "PLUGBOARD_CHARSET_FLAG":"L"
        }
        """
        self.settings_string = settings_string
        self._valid_charset_flag(charset_flag)
        pattern = self._create_regex_pattern()
        pb_settings_data = self._extract_data_from_regex(pattern)
        self._check_pb_settings_data_exist(pb_settings_data)
        pb_settings_data_dict = self._extract_settings(pb_settings_data)
        pb_settings_data_dict = self._format_numbers(pb_settings_data_dict)
        pb_settings_data_dict = self._valid_socket_ids(pb_settings_data_dict)
        self._correct_number_of_socket_ids(pb_settings_data_dict)
        self._check_for_unique_socket_ids(pb_settings_data_dict)
        connections_dict = self._make_connections_dict(pb_settings_data_dict)

        return connections_dict

    def _valid_charset_flag(self, charset_flag):
        charset_flag = charset_flag.upper()
        if charset_flag not in ["L","N"]:
            raise Exception(f"{charset_flag} is not a valid charset_flag. Must be 'L' or 'N'.")
        self.charset_flag = charset_flag
            
    def _create_regex_pattern(self):
        if self.charset_flag == "L":
            pattern = r"(?P<id>[abAB])=\[(?P<plugs>[a-zA-Z,; ]+)\]"
        elif self.charset_flag == "N":
            pattern = r"(?P<id>[abAB])=\[(?P<plugs>[0-9,; ]+)\]"
        return pattern
        
    def _extract_data_from_regex(self, pattern):
        regex = re.compile(pattern)
        pb_settings_data = re.findall(regex, self.settings_string)
        return pb_settings_data
        
    def _check_pb_settings_data_exist(self, pb_settings_data):
        if not pb_settings_data:
            err_msg = f""
            raise UhrBoxPBSettingsStringError(err_msg)
            
    def _extract_settings(self, pb_settings_data):
        if len(pb_settings_data) != 2:
            err_msg = f""
            raise UhrBoxPBSettingsStringError(err_msg)
        else:
            pb_settings_data_dict = {}
            group1 = pb_settings_data[0]
            group2 = pb_settings_data[1]
            group1_id = group1[0]
            group2_id = group2[0]
            group1_id = group1_id.upper()
            group2_id = group2_id.upper()
            if group1_id == group2_id:
                err_msg = f""
                raise UhrBoxPBSettingsStringError(err_msg)
            
            if self.charset_flag == "L":
                pattern = r"[a-zA-Z]+"
            elif self.charset_flag == "N":
                pattern = r"[0-9]+"

            regex = re.compile(pattern)
            sockets1 = re.findall(regex, group1[1])
            sockets2 = re.findall(regex, group2[1])

            pb_settings_data_dict[group1_id] = sockets1
            pb_settings_data_dict[group2_id] = sockets2

            return pb_settings_data_dict
        
    def _format_numbers(self, pb_settings_data_dict):
        if self.charset_flag == "N":
            pb_settings_data_dict["A"] = [n.rjust(2,'0') for n in pb_settings_data_dict["A"]]
            pb_settings_data_dict["B"] = [n.rjust(2,'0') for n in pb_settings_data_dict["B"]]
        return pb_settings_data_dict
        
    def _valid_socket_ids(self, pb_settings_data_dict):
        groups = ["A","B"]
    
        charset = self.LETTERS if self.charset_flag == "L" else self.NUMBERS

        for group in groups:
            for socket_id in pb_settings_data_dict[group]:
                if socket_id not in charset:
                    err_msg = f""
                    raise UhrBoxPBSettingsStringError(err_msg)
        return pb_settings_data_dict

    def _correct_number_of_socket_ids(self, pb_settings_data_dict):
        err_msg = None
        if len(pb_settings_data_dict["A"]) != 10:
            err_msg = f""
        if len(pb_settings_data_dict["B"]) != 10:
            err_msg = f""
        if err_msg:
            raise UhrBoxPBSettingsStringError(err_msg)
        
        return pb_settings_data_dict

    def _check_for_unique_socket_ids(self, pb_settings_data_dict):
        all_socket_ids = pb_settings_data_dict["A"].copy() + pb_settings_data_dict["B"].copy()
        unique = set(all_socket_ids)
        if len(unique) != 20:
            err_msg = f""
            raise UhrBoxPBSettingsStringError(err_msg)

    def _make_connections_dict(self, pb_settings_data_dict):
        connections_dict = {
            "PLUGBOARD_SETTINGS":{},
            "PLUGBOARD_MODE":"U",
            "PLUGBOARD_CHARSET_FLAG":self.charset_flag
        }

        groups = ["A","B"]

        for group in groups:
            for index, socket_id in enumerate(pb_settings_data_dict[group], start=1):
                connections_dict["PLUGBOARD_SETTINGS"][f"{str(index).rjust(2,'0')}{group}"] = socket_id
        return connections_dict
