

class SteckerPBSettingsDictError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class SteckerPBDictValidator:

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{i+1}".rjust(2,'0') for i in range(26)]

    def __init__(self):
        self.settings_dict = None
        self.valid_settings = None

    def validate(self, settings_dict):
        self.valid_settings = {"PLUGBOARD_MODE":"S"}
        self.settings_dict = settings_dict

        self._check_connections_exist()
        self._check_charset_flag()
        self._check_numbers()
        self._check_letters()
        self._make_pb_connections_dict()
        self._check_contradictions()

        return self.valid_settings
    
    def _check_connections_exist(self):
        if "PLUGBOARD_CONNECTIONS" not in self.settings_dict.keys():
            err_msg = f""
            raise SteckerPBSettingsDictError(err_msg)
        else:
            self.valid_settings["PLUGBOARD_CONNECTIONS"] = {}

    def _check_charset_flag(self):
        if "PLUGBOARD_CHARSET_FLAG" not in self.settings_dict.keys():
            err_msg = f""
            raise SteckerPBSettingsDictError(err_msg)
        elif self.settings_dict["PLUGBOARD_CHARSET_FLAG"] not in ["L","N"]:
            err_msg = f""
            raise SteckerPBSettingsDictError(err_msg)
        else:
            self.valid_settings["PLUGBOARD_CHARSET_FLAG"] = self.settings_dict["PLUGBOARD_CHARSET_FLAG"]

    def _check_numbers(self):
        err_msg = f""

        if self.valid_settings["PLUGBOARD_CHARSET_FLAG"] == "N":
            for s1, s2 in self.settings_dict.items():
                s1 = s1.rjust(2,'0')
                s2 = s2.rjust(2,'0')
                if s1 not in self.NUMBERS:
                    err_msg = f""
                if s2 not in self.NUMBERS:
                    err_msg = f""
                if err_msg:
                    raise SteckerPBSettingsDictError(err_msg)

    def _check_letters(self):
        err_msg = f""

        if self.valid_settings["PLUGBOARD_CHARSET_FLAG"] == "L":
            for s1, s2 in self.settings_dict["PLUGBOARD_CONNECTIONS"].items():
                s1 = s1.upper()
                s2 = s2.upper()
                if s1 not in self.LETTERS:
                    err_msg = f""
                if s2 not in self.LETTERS:
                    err_msg = f""
                if err_msg:
                    raise SteckerPBSettingsDictError(err_msg)
                
    def _make_pb_connections_dict(self):
        if self.valid_settings["PLUGBOARD_CHARSET_FLAG"] == "L":
            self.valid_settings["PLUGBOARD_CONNECTIONS"] = {chr(i):chr(i) for i in range(65,91)}
        elif self.valid_settings["PLUGBOARD_CHARSET_FLAG"] == "N":
            self.valid_settings["PLUGBOARD_CONNECTIONS"] = {f"{i+1}".rjust(2,'0'):f"{i+1}".rjust(2,'0') for i in range(26)}

    def _check_contradictions(self):
        used = {}

        err_msg = None

        for s1, s2 in self.settings_dict["PLUGBOARD_CONNECTIONS"].items():
            if s1 in used.keys() and used[s1] != s2:
                err_msg = f"ERROR"
            if s2 in used.keys() and used[s2] != s1:
                err_msg = f"ERROR"
            if err_msg:
                raise SteckerPBSettingsDictError(err_msg)
            else:
                used[s1] = s2
                used[s2] = s1
                self.valid_settings["PLUGBOARD_CONNECTIONS"][s1] = s2
                self.valid_settings["PLUGBOARD_CONNECTIONS"][s2] = s1
