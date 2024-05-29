from enigma_core.settings.settings import EQUIPMENT_DICT
import re


class PermutationError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class PermutationStringValidator:

    def __init__(self):
        self.machine_type = None
        self.permutation_string = None
        self.rs_flag = None
        self.group_flag = None

    def validate(self, machine_type, permutation_string, rs_flag=True, group_flag=True):
        # valid machine type
        # 
        self.permutation_string = permutation_string.upper()
        self.rs_flag = rs_flag
        self.group_flag = group_flag

        self._valid_machine_type(machine_type)
        pattern = self._create_pattern()
        permutation_data = self._extract_permutation(pattern)
        self._valid_rotor_types(permutation_data)
        output_dict = self._make_output_dict(permutation_data)

        return output_dict

    def _valid_machine_type(self, machine_type):
        for machine in ["WEHRMACHT early","WEHRMACHT late"]:
            if machine.upper() == machine_type.upper():
                self.machine_type = machine
                return
        err_msg = f"{machine_type} is not a valid enigma machine."
        raise Exception(err_msg)

    def _create_pattern(self):
        pattern = ""

        if self.rs_flag:
            pattern += "(?P<rs_setting>[A-Z]).?"

        if self.machine_type == "WEHRMACHT early":
            pattern += "(?P<ref_type>UKW-A).?(?P<rs_type>[i]+).?(?P<rm_type>[i]+).?(?P<rf_type>[i]+).?"
        elif self.machine_type == "WEHRMACHT late":
            pattern += "(?P<ref_type>UKW-B|UKW-C).?(?P<rs_type>[iv]+).?(?P<rm_type>[iv]+).?(?P<rf_type>[iv]+).?"
        if self.group_flag:
            pattern += "(?P<group>G1|G2|G3)"
        return pattern

    def _extract_permutation(self, pattern):
        regex = re.compile(pattern, re.IGNORECASE)
        permutation_data = regex.search(self.permutation_string)

        if not permutation_data:
            err_msg = f"{self.permutation_string} is not a valid permutation string for a {self.machine_type} enigma."
            raise PermutationError(err_msg)

        return permutation_data

    def _valid_rotor_types(self, permutation_data):
        rotor_types = EQUIPMENT_DICT[self.machine_type]["ROTORS"]

        dynamic_rotors_list = [r for r in rotor_types.keys() if rotor_types[r]["turnover_chars"] != []]

        rs_type = permutation_data.group("rs_type")
        rm_type = permutation_data.group("rm_type")
        rf_type = permutation_data.group("rf_type")

        rotors_list = [rs_type,rm_type,rf_type]

        for rotor_type1 in rotors_list:
            error = True
            for rotor_type2 in dynamic_rotors_list:
                if rotor_type1.upper() == rotor_type2.upper():
                    error = False
            if error:
                err_msg = f"{rotor_type1} is not a valid rotor type for rotor psoitions 'RS,RM,RF' {self.machine_type} enigma."
                raise PermutationError(err_msg)
        
    def _make_output_dict(self, permutation_data):
        output_dict = {}

        output_dict["REFLECTOR"] = permutation_data.group("ref_type")
        output_dict["RS_TYPE"] = permutation_data.group("rs_type")
        output_dict["RM_TYPE"] = permutation_data.group("rm_type")
        output_dict["RF_TYPE"] = permutation_data.group("rf_type")
        if self.rs_flag:
            output_dict["RS_SETTING"] = permutation_data.group("rs_setting")
        if self.group_flag:
            output_dict["GROUP"] = permutation_data.group("group")
        return output_dict
