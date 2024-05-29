

class UhrBoxPBSettingsDictError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class UhrBoxPBDictValidator:

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{i+1}".rjust(2,'0') for i in range(26)]

    plug_ids = [
        "01A","02A","03A","04A","05A",
        "06A","07A","08A","09A","10A",
        "01B","02B","03B","04B","05B",
        "06B","07B","08B","09B","10B"
    ]

    def __init__(self):
        """"
        "PLUGBOARD SETTINGS":{
            "PLUGBOARD_CONNECTIONS":{
                "01A":"A","02A":"B",
                "03A":"C","04A":"D",
                "05A":"E","06A":"F",
                "07A":"G","08A":"H",
                "09A":"I","10A":"J",
                "01B":"K","02B":"L",
                "03B":"M","04B":"N",
                "05B":"O","06B":"P",
                "07B":"Q","08B":"R",
                "09B":"S","10B":"T",
            }
            "PLUGBOARD_MODE":"U",
            "PLUGBOARD_CHARSET_FLAG":"L"
        } 
        """
        self.settings_dict = None
        self.valid_settings = None

    def validate(self, settings_dict):

        self.valid_settings = {"PLUGBOARD_MODE":"U"}
        self.settings_dict = settings_dict

        self._check_connections_exist()
        self._check_charset_flag()
        self._check_plug_ids()
        self._check_numbers()
        self._check_letters()
        self._check_contradictions()

        return self.valid_settings

    def _check_connections_exist(self):
        if "PLUGBOARD_CONNECTIONS" not in self.settings_dict.keys():
            err_msg = f""
            raise UhrBoxPBSettingsDictError(err_msg)
        else:
            self.valid_settings["PLUGBOARD_CONNECTIONS"] = {}

    def _check_charset_flag(self):
        if "PLUGBOARD_CHARSET_FLAG" not in self.settings_dict.keys():
            err_msg = f""
            raise UhrBoxPBSettingsDictError(err_msg)
        elif self.settings_dict["PLUGBOARD_CHARSET_FLAG"] not in ["L","N"]:
            err_msg = f""
            raise UhrBoxPBSettingsDictError(err_msg)
        else:
            self.valid_settings["PLUGBOARD_CHARSET_FLAG"] = self.settings_dict["PLUGBOARD_CHARSET_FLAG"]

    def _check_plug_ids(self):
        for plug_id in self.settings_dict["PLUGBOARD_CONNECTIONS"].keys():
            if plug_id not in self.plug_ids:
                err_msg = f""
                raise UhrBoxPBSettingsDictError(err_msg)

    def _check_numbers(self):
        if self.valid_settings["PLUGBOARD_CHARSET_FLAG"] == "N":
            for plug_id, socket_id in self.settings_dict["PLUGBOARD_CONNECTIONS"].items():
                if len(socket_id) == 1 and socket_id not in "123456789":
                    err_msg = f""
                    raise UhrBoxPBSettingsDictError(err_msg)
                else:
                    socket_id = f"{socket_id}".rjust(2,'0')
                    if socket_id not in self.NUMBERS:
                        err_msg = f""
                        raise UhrBoxPBSettingsDictError(err_msg)
                    else:
                        self.valid_settings["PLUGBOARD_CONNECTIONS"][plug_id] = socket_id

    def _check_letters(self):
        if self.valid_settings["PLUGBOARD_CHARSET_FLAG"] == "L":
            for plug_id, socket_id in self.settings_dict["PLUGBOARD_CONNECTIONS"].items():
                socket_id = socket_id.upper()
                if socket_id not in self.LETTERS:
                    err_msg = f""
                    raise UhrBoxPBSettingsDictError(err_msg)
                else:
                    self.valid_settings["PLUGBOARD_CONNECTIONS"][plug_id] = socket_id

    def _check_contradictions(self):
        used = {}

        for plug_id, socket_id in self.valid_settings["PLUGBOARD_CONNECTIONS"].items():
            if socket_id in used.keys():
                err_msg = f""
                raise UhrBoxPBSettingsDictError(err_msg)
            else:
                used[socket_id] = plug_id
