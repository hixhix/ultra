from enigma_core.settings.settings import EQUIPMENT_DICT


class RotorTypesDictError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class RotorTypesDictValidator:

    POSITIONS = ["R4","RS","RM","RF"]

    def __init__(self):
        self.machine_type = None
        self.settings_dict = None
        self.check_positions = None
        self.output_dict = None

    def validate(self, machine_type, settings_dict, check_positions=None):
        self.output_dict = {}
        self._valid_machine_type(machine_type)
        self._valid_settings_dict_keys(settings_dict)
        self._valid_check_positions(check_positions)
        self._valid_rotor_types(settings_dict)

        return self.output_dict
    
    def _valid_machine_type(self, machine_type):
        for machine in EQUIPMENT_DICT.keys():
            if machine.upper() == machine_type.upper():
                self.machine_type = machine
                return
        err_msg = f"{machine_type} is not a valid enigma machine."
        raise Exception(err_msg)

    def _valid_settings_dict_keys(self, settings_dict):
        cells_map = list(EQUIPMENT_DICT[self.machine_type]["CELLS_MAP"].keys())

        rotor_positions = cells_map[1::]

        for position in settings_dict.keys():
            if position not in rotor_positions:
                err_msg = f""
                raise Exception(err_msg)
            
        if len(rotor_positions) != len(settings_dict.keys()):
            err_msg = f""
            raise Exception(err_msg)
        
        self.check_positions = list(settings_dict.keys())

        self.output_dict = {k:"" for k in self.check_positions}

    def _valid_check_positions(self, check_positions):
        check_positions = [p.upper() for p in check_positions]

        if check_positions:
            cells_map = list(EQUIPMENT_DICT[self.machine_type]["CELLS_MAP"].keys())

            rotor_positions = cells_map[1::]

            for position in check_positions:
                if position not in rotor_positions:
                    err_msg = f""
                    raise Exception(err_msg)
            self.check_positions = check_positions

    def _valid_rotor_types(self, settings_dict):
        rotor_types = EQUIPMENT_DICT[self.machine_type]["ROTORS"]

        dynamic_rotors = [r for r in rotor_types.keys() if rotor_types[r]["turnover_chars"] != []]
        static_rotors = [r for r in rotor_types.keys() if rotor_types[r]["turnover_chars"] == []]

        dynamic_positions = ["RS","RM","RF"]

        # check dynamic rotor types exist
        for rotor_position in settings_dict.keys():
            if rotor_position in dynamic_positions:
                rotor_type = settings_dict[rotor_position]
                if rotor_position in self.check_positions:
                    error = True
                    for _rotor_type in dynamic_rotors:
                        if rotor_type.upper() == _rotor_type.upper():
                            self.output_dict[rotor_position] = _rotor_type
                            error = False
                    if error:
                        err_msg = (f"Invalid rotor type '{rotor_type}'. "
                                   f"is not a valid rotor type for rotor positions 'RS,RM,RF' in '{self.machine_type}' enigma machine.")
                        raise RotorTypesDictError(err_msg)
                else:
                    self.output_dict[rotor_position] = rotor_type

        # check for unique dynamic rotors
        for rotor_type in self.output_dict.values():
            if list(self.output_dict.values()).count(rotor_type) > 1:
                err_msg = f"Rotor type '{rotor_type}' in multiple rotor positions. All rotor types must be unique."
                raise RotorTypesDictError(err_msg)

        # check static rotor type exists
        if "R4" in settings_dict.keys():
            rotor_type = settings_dict["R4"]
            if rotor_position in self.check_positions:
                error = True
                for _rotor_type in static_rotors:
                    if rotor_type.upper() == _rotor_type.upper():
                        self.output_dict["R4"] = _rotor_type
                        error = False
                if error:
                    err_msg = (f"Invalid rotor type '{rotor_type}'. "
                               f"Is not a valid rotor type for rotor position 'R4' in  '{self.machine_type}' enigma machine.")
                    raise RotorTypesDictError(err_msg)
            else:
                self.output_dict["R4"] = rotor_type
