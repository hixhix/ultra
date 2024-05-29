from enigma_tools.setting_tools.setting_tools import RotorSettings
from enigma_core.factory import make_machine
import json
import os
        

class SheetDataGenerator:

    LETTERS = [chr(i) for i in range(65, 91)]

    def __init__(self):
        """
        
        """
        self._machine_obj = None
        self._settings = None

    def data(self, settings, machine_type, source='A'):
        """
        
        """
        self._settings = settings
        self._machine_type = machine_type
        self._machine_obj = make_machine(self._machine_type)

        if source == 'M':
            data = self._make_data()
        elif source == 'F':
            data = self._file_data()
        elif source == 'A':
            try:
                data = self._file_data()
            except NotADirectoryError:
                data = self._make_data()
        return data

    def _file_data(self):
        """
        
        """
        self._settings["SCRAMBLER_SETTINGS"]["TURNOVER_FLAG"] = False
        dirpath = os.path.dirname(__file__)
        dirpath = os.path.join(dirpath, "zygalski_catalog")
        dirpath = os.path.join(dirpath, self._machine_type.replace(" ","_"))
        
        if os.path.isdir(dirpath):
            rs = self._settings["SCRAMBLER_SETTINGS"]["ROTOR_SETTINGS"]["RS"]
            ref = self._settings["SCRAMBLER_SETTINGS"]["REFLECTOR_TYPE"]
            rot_rs = self._settings["SCRAMBLER_SETTINGS"]["ROTOR_TYPES"]["RS"]
            rot_rm = self._settings["SCRAMBLER_SETTINGS"]["ROTOR_TYPES"]["RM"]
            rot_rf = self._settings["SCRAMBLER_SETTINGS"]["ROTOR_TYPES"]["RF"]
            dirname = f"{ref}_{rot_rs}_{rot_rm}_{rot_rf}"
            filename = f"{rs}_{ref}_{rot_rs}_{rot_rm}_{rot_rf}.json"
            dirpath = os.path.join(dirpath, dirname)
            filepath = os.path.join(dirpath, filename)

            with open(filepath, "r") as f:
                data = json.load(f)

            return data
        else:
            err_msg = f"{dirpath} does not exist."
            raise NotADirectoryError(err_msg)

    def _make_data(self):
        """
        
        """
        data = {}
        self._machine_obj.scrambler.character_set_flag = 'L'
        self._machine_obj.settings = self._settings
        self._settings = self._machine_obj.settings
        rotor_settings = self._machine_obj.settings["SCRAMBLER_SETTINGS"]["ROTOR_SETTINGS"]
        rot_set_gen = RotorSettings(positions=2)

        while True:
            rot_set = rot_set_gen.settings
            setting_data = {"G1":[],"G2":[],"G3":[]}
            self._settings["SCRAMBLER_SETTINGS"]["TURNOVER_FLAG"] = False
            for letter in self.LETTERS:
                inpt = letter*6
                self._machine_obj.settings = {"SCRAMBLER_SETTINGS":{"ROTOR_SETTINGS":rotor_settings}}
                self._machine_obj.settings = {"SCRAMBLER_SETTINGS":{"ROTOR_SETTINGS":rot_set}}
                outp = ""
                for l in inpt:
                    outp += self._machine_obj.character_input(l)
                if outp[0] == outp[3]:
                    setting_data["G1"].append([l,outp[0]])
                if outp[1] == outp[4]:
                    setting_data["G2"].append([l,outp[1]])
                if outp[2] == outp[5]:
                    setting_data["G3"].append([l,outp[2]])
            data[f"{rot_set['RM']}{rot_set['RF']}"] = setting_data

            try:
                rot_set_gen.inc()
            except StopIteration:
                break

        return data