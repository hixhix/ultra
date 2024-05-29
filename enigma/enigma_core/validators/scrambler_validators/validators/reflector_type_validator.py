from enigma_core.settings.settings import EQUIPMENT_DICT


class ReflectorTypeError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


class ReflectorTypeValidator:

    def __init__(self):
        pass

    def validate(self, machine_type, reflector_type):
        machine_type = self._valid_machine_type(machine_type)
        reflector_type = self._valid_reflector_type(machine_type, reflector_type)
        return reflector_type

    def _valid_machine_type(self, machine_type):
        for machine in EQUIPMENT_DICT.keys():
            if machine.lower() == machine_type.lower():
                return machine
        err_msg = f""
        raise Exception(err_msg)
    
    def _valid_reflector_type(self, machine_type, reflector_type):
        for reflector in EQUIPMENT_DICT[machine_type]["REFLECTORS"]:
            if reflector.lower() == reflector_type.lower():
                return reflector
        err_msg = f"{reflector_type} is not a valid reflector type for {machine_type} enigma."
        raise ReflectorTypeError(err_msg)
