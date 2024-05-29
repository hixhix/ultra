from collections import OrderedDict
from enigma_core.scrambler.scrambler.cell import Cell
from enigma_core.scrambler.collection.collection import Collection
from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.scrambler.exceptions.exceptions import (ScramblerNotValid,
                                                         DeviceBorrowedError,
                                                         CellDeviceError)


class Scrambler:
    """

    """

    def __init__(self, machine, char_set_flag = 'L'):
        self.machine = machine
        self.collection = Collection(machine, char_set_flag)
        self._cells = OrderedDict()
        self._make_cells(machine)
        self._turnover_flag = True

    def __str__(self):
        """
        Returns the string repressentation of the scrambler.
        """
        sd = self.settings
        rotors_length = len(sd["ROTOR_SETTINGS"].keys())*6

        def header_string():
            header_str = f"{' '*17}REFLECTOR{' '*4}"
            header_str += "ROTORS".center(rotors_length, ' ')
            header_str += '\n'
            return header_str

        def positions_string():
            position_str = "POSITIONS".ljust(31, ' ')
            positions = list(sd["ROTOR_TYPES"].keys())
            for position in positions:
                position_str += f" {position.center(4, '-')} "
            position_str += '\n'
            return position_str

        def types_string():
            types_str = "TYPES".ljust(17, ' ')
            ref_id = sd["REFLECTOR_TYPE"] or "--"
            types_str += ref_id.center(9, ' ')
            types_str += ' '*5
            rotor_types = sd["ROTOR_TYPES"]
            positions = list(rotor_types.keys())
            for position in positions:
                rotor_id = rotor_types[position] or "--"
                types_str += rotor_id.center(6, ' ')
            types_str += '\n'
            return types_str

        def rotor_settings_string():
            settings_str = "ROTOR SETTINGS".ljust(31, ' ')
            rotor_settings = sd["ROTOR_SETTINGS"]
            positions = list(rotor_settings.keys())
            for position in positions:
                rotor_setting = rotor_settings[position] or "--"
                settings_str += rotor_setting.center(6, ' ')
            settings_str += '\n'
            return settings_str

        def ring_settings_string():
            settings_str = "RING SETTINGS".ljust(31, ' ')
            ring_settings_str = ""
            ring_settings = sd["RING_SETTINGS"]
            positions = list(ring_settings.keys())
            for position in positions:
                ring_setting = ring_settings[position] or "--"
                ring_settings_str += ring_setting.center(6, ' ')
            settings_str += ring_settings_str.rjust(rotors_length, ' ')
            return settings_str

        scrambler_str = header_string()
        scrambler_str += positions_string()
        scrambler_str += types_string()
        scrambler_str += rotor_settings_string()
        scrambler_str += ring_settings_string()
        return scrambler_str

    def set_device(self, position, device_id):
        """
        
        """
        self.collection.valid_position(self.machine, position)

        self.collection.compatible_device_type(self.machine, device_id, ["REF","F_ROT","R_ROT"])

        self.collection.compatible_device_position(self.machine, device_id, position)

        self.remove_device(position)

        try:
            device_obj = self.collection.borrow_device(device_id)
        except DeviceBorrowedError as e:
            raise e
        else:
            self._cells[position].set_device(device_obj)

    def get_device(self, position):
        """

        """
        self.collection.valid_position(self.machine, position)

        try:
            device_obj = self._cells[position].get_device()
        except CellDeviceError:
            device_obj = None

        return device_obj

    def remove_device(self, position):
        """

        """
        self.collection.valid_position(self.machine, position)

        try:
            device_obj = self._cells[position].remove_device()
        except CellDeviceError:
            pass
        else:
            self.collection.return_device(device_obj)

    def get_device_id(self, position):
        """

        """
        self.collection.valid_position(self.machine, position)

        device_obj = self.get_device(position)
        if device_obj:
            device_id = device_obj.device_id
        else:
            device_id = None
        
        return device_id

    def clear_scrambler(self):
        """
        
        """
        for position in self._cells.keys():
            device_obj = self.remove_device(position)
            if device_obj:
                self.collection.return_device(device_obj)

    def default_settings(self):
        """
        
        """
        rotors_signature = self.collection.device_signature(self.machine, ["F_ROT","R_ROT"])

        for position in rotors_signature.keys():
            try:
                rotor_obj = self.get_device(position)
                rotor_obj.reset_rotor()
            except CellDeviceError:
                pass

    def valid_scrambler(self):
        """
        
        """
        for cell in self._cells:
            try:
                self._cells[cell].get_device()
            except CellDeviceError:
                return False
        return True
    
    @property
    def settings(self):
        """
        
        """
        settings = {}
        settings["ROTOR_TYPES"] = self.rotor_types
        settings["ROTOR_SETTINGS"] = self.rotor_settings
        settings["RING_SETTINGS"] = self.ring_settings
        settings["REFLECTOR_TYPE"] = self.get_device_id("REF")
        settings["TURNOVER_FLAG"] = self.turnover_flag
        settings["SCRAMBLER_CHARSET_FLAG"] = self.collection.character_set_flag
        return settings

    @settings.setter
    def settings(self, settings):
        """
        
        """
        #self.clear_scrambler()
        try:
            char_set_flag = settings["SCRAMBLER_CHARSET_FLAG"]
        except KeyError:
            pass
        else:
            if char_set_flag:
                self.character_set_flag = char_set_flag

        try:
            rotor_types = settings["ROTOR_TYPES"]
        except KeyError:
            pass
        else:
            if rotor_types:
                self.rotor_types = rotor_types

        try:
            rotor_settings = settings["ROTOR_SETTINGS"]
        except KeyError:
            pass
        else:
            if rotor_settings:
                self.rotor_settings = rotor_settings

        try:
            ring_settings = settings["RING_SETTINGS"]
        except KeyError:
            pass
        else:
            if ring_settings:
                self.ring_settings = ring_settings

        try:
            reflector = settings["REFLECTOR_TYPE"]
        except KeyError:
            pass
        else:
            if reflector != "UKW-D":
                self.set_device("REF", reflector)
            elif reflector == "UKW-D":
                self.set_device("REF", reflector)
                if "REFLECTOR_WIRING" in settings.keys():
                    wiring_list = settings["REFLECTOR_WIRING"]
                    device = self.get_device("REF")
                    device.set_wiring(wiring_list)

        try:
            turnover_flag = settings["TURNOVER_FLAG"]
        except KeyError:
            pass
        else:
            if turnover_flag:
                self.turnover_flag = turnover_flag

    def keyed_input(self, index):
        """
        
        """
        self.rotor_turnover()
        return self.output(index)

    def output(self, index):
        """
        
        """
        rotors_dict = self.collection.device_signature(self.machine, ["F_ROT","R_ROT"])

        positions = list(rotors_dict.keys())

        positions.reverse()

        try:
            for position in positions:
                rotor_obj = self.get_device(position)
                index = rotor_obj.lh_output(index)
            reflector_obj = self.get_device("REF")
            index = reflector_obj.output(index)
            positions.reverse()
            for position in positions:
                rotor_obj = self.get_device(position)
                index = rotor_obj.rh_output(index)
            return index
        except CellDeviceError as e:
            raise e
        
    def rotor_turnover(self):
        """
        
        """
        turnovers = [True, False, False]

        if self.valid_scrambler():
            if self._turnover_flag:
                # middle rotor turnover
                if self._cells["RF"].get_device().on_turnover():
                    turnovers[1] = True
                if self._cells["RM"].get_device().on_turnover():
                    turnovers[1] = True
                # slow rotor turnover
                if self._cells["RM"].get_device().on_turnover():
                    turnovers[2] = True

            self._cells["RF"].get_device().inc_rotor_setting()
            if turnovers[1]:
                self._cells["RM"].get_device().inc_rotor_setting()
            if turnovers[2]:
                self._cells["RS"].get_device().inc_rotor_setting()

        else:
            raise ScramblerNotValid("Rotor group is not valid")

    @property
    def turnover_flag(self):
        """
        
        """
        return self._turnover_flag

    @turnover_flag.setter
    def turnover_flag(self, flag):
        """
        
        """
        if isinstance(flag, bool):
            self._turnover_flag = flag
        else:
            msg = f""
            raise ValueError(msg)

    @property
    def character_set(self):
        """
        
        """
        return self.collection.character_set

    @property
    def character_set_flag(self):
        """
        
        """
        return self.collection.character_set_flag

    @character_set_flag.setter
    def character_set_flag(self, flag):
        """
        
        """
        self.collection.character_set_flag = flag

    @property
    def rotor_types(self):
        """
        
        """
        rotor_signature = self.collection.device_signature(self.machine, ["F_ROT","R_ROT"])

        rotor_types = {}

        for position in rotor_signature.keys():
            rotor_id = self.get_device_id(position)
            if rotor_id:
                rotor_types[position] = rotor_id
            else:
                rotor_types[position] = None
        
        return rotor_types

    @rotor_types.setter
    def rotor_types(self, rotor_types):
        """
        Takes a dictionary with key, value pairs of positions and rotor type.
        If the rotor type is valid for the position set that rotor tye at that
        position.
        """
        for position, rotor in rotor_types.items():
            self.collection.valid_position(self.machine, position)
            rotor, flag = self.collection.compatible_device_type(self.machine, rotor, ["F_ROT","R_ROT"])
            self.collection.compatible_device_position(self.machine, rotor, position)
            self.set_device(position, rotor)

    @property
    def rotor_settings(self):
        """
        
        """
        settings = {}

        rotor_signature = self.collection.device_signature(self.machine, ["F_ROT","R_ROT"])

        for position in rotor_signature.keys():
            rotor_obj = self.get_device(position)
            if rotor_obj:
                settings[position] = rotor_obj.rotor_setting
            else:
                settings[position] = None

        return settings

    @rotor_settings.setter
    def rotor_settings(self, rotor_settings):
        """
        
        """
        for position, rotor_setting in rotor_settings.items():
            self.collection.valid_position(self.machine, position)
            self.collection.valid_ring_character(rotor_setting)
            try:
                rotor_obj = self.get_device(position)
                rotor_obj.rotor_setting = rotor_setting
            except CellDeviceError as e:
                raise e

    @property
    def ring_settings(self):
        """
        
        """
        settings = {}

        rotor_signature = self.collection.device_signature(self.machine, ["F_ROT","R_ROT"])

        for position in rotor_signature.keys():
            rotor_obj = self.get_device(position)
            if rotor_obj:
                settings[position] = rotor_obj.ring_setting
            else:
                settings[position] = None

        return settings

    @ring_settings.setter
    def ring_settings(self, ring_settings):
        """
        
        """
        for position, ring_setting in ring_settings.items():
            self.collection.valid_position(self.machine, position)
            self.collection.valid_ring_character(ring_setting)
            try:
                rotor_obj = self.get_device(position)
                rotor_obj.ring_setting = ring_setting
            except CellDeviceError as e:
                raise e

    def _make_cells(self, machine):
        """
        
        """
        cells = EQUIPMENT_DICT[machine]["CELLS_MAP"]

        for position, cell_flag in cells.items():
            self._cells[position] = Cell(position, cell_flag)