from enigma_core.settings.settings import EQUIPMENT_DICT
import re


class RotorTypesStringError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class RotorTypesStringValidator:

    POSITIONS = ["R4","RS","RM","RF"]

    def __init__(self):
        self.machine_type = None
        self.positions = None

    def validate(self, machine_type, settings_string):
        self.settings_string = settings_string
        self._valid_machine_type(machine_type)
        self._set_positions()
        pattern = self._create_pattern()
        rotor_types = self._extract_rotor_types(pattern)
        rotor_types = self._check_for_valid_rotor_types(rotor_types)
        self._check_for_unique_rotors(rotor_types)
        output_dict = self._create_output_dict(rotor_types)

        return output_dict

    def _valid_machine_type(self, machine_type):
        for machine in EQUIPMENT_DICT.keys():
            if machine.upper() == machine_type.upper():
                self.machine_type = machine
                return
        err_msg = f"{machine_type} is not a valid enigma machine."
        raise Exception(err_msg)
    
    def _set_positions(self):
        cells_map = EQUIPMENT_DICT[self.machine_type]["CELLS_MAP"]

        self.positions = len(cells_map.keys()) -1

    def _create_pattern(self):
        if self.positions == 3:
            pattern = "^[^IV]?([IV]+)[^IV]+([IV]+)[^IV]+([IV]+)"
        elif self.positions == 4:
            pattern = "^.?(Beta|Gamma)[^IV]+([IV]+)[^IV]+([IV]+)[^IV]+([IV]+)"
        return pattern

    def _extract_rotor_types(self, pattern):
        regex = re.compile(pattern, re.IGNORECASE)
        rotor_types = re.findall(regex, self.settings_string)
        
        if not rotor_types:
            err_msg = f"{self.settings_string} is not a valid rotor types string for a {self.machine_type} enigma."
            raise RotorTypesStringError(err_msg)

        return rotor_types[0]

    def _check_for_valid_rotor_types(self, rotor_types_list):
        rotor_types = EQUIPMENT_DICT[self.machine_type]["ROTORS"]

        dynamic_rotors = [r for r in rotor_types.keys() if rotor_types[r]["turnover_chars"] != []]
        static_rotors = [r for r in rotor_types.keys() if rotor_types[r]["turnover_chars"] == []]

        valid_rotor_types = []

        if self.positions == 4:
            static_rotor = rotor_types_list[0]
            for rotor_type in static_rotors:
                if rotor_type.upper() == static_rotor.upper():
                    valid_rotor_types.append(rotor_type)

        _dynamic_rotors = rotor_types_list[-3:]

        for rotor_type1 in _dynamic_rotors:
            error = True
            for rotor_type2 in dynamic_rotors:
                if rotor_type1.upper() == rotor_type2.upper():
                    valid_rotor_types.append(rotor_type2)
                    error = False
            if error:
                err_msg = f"{rotor_type1} is not a valid rotor type for rotor psoitions 'RS,RM,RF' {self.machine_type} enigma."
                raise RotorTypesStringError(err_msg)
            
        return valid_rotor_types

    def _check_for_unique_rotors(self, rotor_types):
        dynamic_rotors = rotor_types[-3:]

        for rotor_type in dynamic_rotors:
            if dynamic_rotors.count(rotor_type) > 1:
                err_msg = f"Rotor type {rotor_type} is used in multiple rotor positions. All rotor types must be unique."
                raise RotorTypesStringError(err_msg)

    def _create_output_dict(self, rotor_types):
        output_dict = {}
        
        if self.positions == 4:
            positions = self.POSITIONS
        elif self.positions == 3:
            positions = self.POSITIONS[-3:]

        for i in range(len(positions)):
            output_dict[positions[i]] = rotor_types[i]

        return output_dict
