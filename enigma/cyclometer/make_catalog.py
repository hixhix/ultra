from hashlib import sha256
from enigma_tools.setting_tools.setting_tools import RotorSettings, scrambler_perms
from enigma_core.factory import make_machine
from collections import deque
import shutil
import json
import os


class CatalogError(Exception):

    def __init__(self, err_msg):
        super().__init__(err_msg)


class Cyclometer:

    LETTERS = [chr(i) for i in range(65,91)]

    def __init__(self):
        """
        
        """
        self._machine_obj1 = None
        self._machine_obj2 = None
        self._permutations = None
        self._rotor_settings = RotorSettings('L', 3)
        self._machines = ["WEHRMACHT early","WEHRMACHT late"]

    def make_cyclometer_catalogs(self):
        """
        
        """
        dir = os.path.dirname(__file__)

        dir = os.path.join(dir, "cyclometer_catalog")

        if os.path.isdir(dir):
            shutil.rmtree(dir)

        for machine in self._machines:
            self._make_cyclometer_catalog(machine)

        hash = self._catalog_hash()

        hash_fpath = os.path.join(dir, "hash_value.txt")

        with open(hash_fpath, "w") as f:
            f.write(hash) 

    def check_catalog(self):
        """
        
        """
        # check all files exist
        dir = os.path.dirname(__file__)

        dir = os.path.join(dir, "cyclometer_catalog")

        if not os.path.isdir(dir):
            raise CatalogError(f"{dir} does not exist.")

        for machine_type in self._machines:
            machine_dir = os.path.join(dir, machine_type.replace(" ","_"))

            if not os.path.isdir(machine_dir):
                raise CatalogError(f"{machine_dir} does not exist.")

            perms = self._make_perms(machine_type)

            for perm in perms:

                dname = f"{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}"
                dpath = os.path.join(machine_dir, dname)
            
                for l in self.LETTERS:
                    fname = f"{l}_{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}.json"

                    fpath = os.path.join(dpath, fname)

                    if not os.path.isfile(fpath):
                        raise CatalogError(f"{fpath} does not exist.")
                    
        hash = self._catalog_hash()

        hash_fpath = os.path.join(dir, "hash_value.txt")

        if not os.path.isfile(hash_fpath):
            raise CatalogError(f"{hash_fpath} does not exist.")

        with open(hash_fpath, "r") as f:
            valid_hash = f.read()

        valid_hash = valid_hash.strip()

        if hash != valid_hash:
            raise CatalogError(f"Inconsistant hash value for catalog.")

        return True

    def _make_cyclometer_catalog(self, machine_type):
        """
        
        """
        self._machine_type = machine_type

        self._initialize_machines()
        self._make_permutations()

        for perm in self._permutations:
            cycles_dictionary = {}
            
            self._initialize_machines()

            while True:
                rotor_settings = self._rotor_settings.settings
                self._set_machine_settings(perm, rotor_settings)

                cycles_dict = self._get_cycles()
                cycles_str = f"{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF} ".ljust(16, ' ')
                cycles_str += f"{rotor_settings['RS']}{rotor_settings['RM']}{rotor_settings['RF']} "
                cycles_dictionary[f"{rotor_settings['RS']}{rotor_settings['RM']}{rotor_settings['RF']}"] = {}
                for g in ["G1","G2","G3"]:
                    cycles_list = cycles_dict[g]
                    cycles_list = sorted(cycles_list, key=lambda x: len(x))
                    cycles_list.reverse()
                    cycle_nums = [len(l) for l in cycles_list]
                    cycle_nums_str = ""
                    for num in cycle_nums:
                        cycle_nums_str += f"({num})"
                        cycles_dictionary[f"{rotor_settings['RS']}{rotor_settings['RM']}{rotor_settings['RF']}"][g] = cycle_nums_str
                    cycles_str += f" {g} {cycle_nums_str}".ljust(50, ' ')
                print(cycles_str)
                cycles_str += '\n'

                try:
                    self._rotor_settings.inc()
                except StopIteration:
                    self._rotor_settings.reset()
                    break
            dirname = os.path.dirname(__file__)
            dirpath = os.path.join(dirname, "cyclometer_catalog")
            if not os.path.isdir(dirpath):
                os.mkdir(dirpath)
            machine_type = self._machine_type.replace(" ","_")
            dirpath = os.path.join(dirpath, machine_type)
            if not os.path.isdir(dirpath):
                os.mkdir(dirpath)
            fpath = os.path.join(dirpath, f"{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}")
            with open(fpath,"w") as f:
                json.dump(cycles_dictionary, f)

    def check_cyclometer_catalog_exists(self):
        """
        
        """
        if not os.path.isdir("cyclometer_catalog"):
            return False
        return True

    def filter_indicators(self):
        """
        
        """
        indicators = [ind for ind in indicators if len(ind) == 10]
        groups = self._make_groups(indicators)

        return groups

    def _make_groups(self, indicators):
        """
        
        """
        lets = deque(self.LETTERS)

        cycles = []

        while True:
            for i in range(26):
                lets.rotate(i)
                groups = []
                for n in range(4):
                    letters = list(lets)[0:20]
                    groups.append(self._get_indicator_group(indicators, letters))
                    lets.rotate(6)
                try:
                    cycles = self._get_indicators_cycles(groups)
                except Exception:
                    pass
                else:
                    break
                lets.rotate(-24)
            break

        return cycles

    def _get_indicator_group(self, indicators, letters):
        """
        
        """
        group = []

        for indicator in indicators:
            if indicator[2] in letters:
                group.append(indicator)
        return group

    def _get_indicators_cycles(self, groups):
        """
        
        """
        cycle_groups = []

        for group in groups:
            cycles = self._get_indicator_cycles(group)
            if cycles:
                cycle_groups.append(group)
        if len(cycle_groups) == 4:
            return cycle_groups
        else:
            raise Exception()

    def _get_indicator_cycles(self, group):
        """
        
        """
        cycles = []
        cycles_dict = {}
        
        pairs = self._get_pairs(group)

        for pair in pairs:
            c1, c2 = pair

            cycles_dict[c1] = c2

        if len(cycles_dict.keys()) != 26:
            print("EIXT ON NOT ENOUGH KEYS")
            return []
        if len(set(cycles_dict.keys())) != 26:
            return []
        if len(set(cycles_dict.values())) != 26:
            return []

        used = []
        cycle = ""
        for l in self.LETTERS:
            if l in used:
                continue
            used.append(l)
            cycle = l
            o1 = cycles_dict[l]
            while True:
                o2 = cycles_dict[o1]
                if o2 == l:
                    cycles.append(cycle)
                    break
                else:
                    used.append(o2)
                    cycle += o2
                o1 = cycles_dict[o2]
        return cycles

    def _get_pairs(self, group):
        """
        
        """
        pairs = []

        for indicator in group:
            c1 = indicator[4]
            c2 = indicator[7]
            pairs.append((c1,c2))
        return pairs

    def _get_cycles(self):
        """
        
        """
        cycles_dict = {}

        for i in range(3):
            used = []
            cycles = []

            for l in self.LETTERS:
                if l in used:
                    continue
                used.append(l)
                cycle = l
                o1 = self._machine_obj1.non_keyed_input(l)
                while True:
                    o2 = self._machine_obj2.non_keyed_input(o1)
                    if o2 == l:
                        cycles.append(cycle)
                        break
                    else:
                        used.append(o2)
                        cycle += o2
                    o1 = self._machine_obj1.non_keyed_input(o2)
            cycles_dict[f"G{i+1}"] = cycles
            self._machine_obj1.character_input('A')
            self._machine_obj2.character_input('A')

        return cycles_dict

    def _set_machine_settings(self, perm, rotor_settings):
        """
        
        """
        settings = {
            "SCRAMBLER_SETTINGS":{
                "SCRAMBLER_CHARSET_FLAG":"L",
                "TURNOVER_FLAG":False,
                "REFLECTOR_TYPE":perm.REF,
                "ROTOR_TYPES":{
                    "RS":perm.RS,
                    "RM":perm.RM,
                    "RF":perm.RF
                },
                "ROTOR_SETTINGS":{
                    "RS":rotor_settings["RS"],
                    "RM":rotor_settings["RM"],
                    "RF":rotor_settings["RF"]
                }
            }
        }

        self._machine_obj1.settings = settings
        self._machine_obj2.settings = settings

        self._machine_obj1.character_input('A')

        for i in range(4):
            self._machine_obj2.character_input('A')

    def _initialize_machines(self):
        """
        
        """
        self._machine_obj1 = make_machine(self._machine_type)
        self._machine_obj2 = make_machine(self._machine_type)

    def _make_perms(self, machine_type):
        """
        
        """
        machine = make_machine(machine_type)

        collection = machine.scrambler.collection.collection_dict()
        rotors_static = collection["ROTORS_STATIC"]
        rotors_dynamic = collection["ROTORS_DYNAMIC"]
        reflectors = collection["REFLECTORS"]

        perms = scrambler_perms(reflectors, rotors_dynamic, rotors_static)

        return perms

    def _make_permutations(self):
        """
        
        """
        collection_dict = self._machine_obj1.scrambler.collection.collection_dict()
        reflectors = collection_dict["REFLECTORS"]
        rotors_dynamic = collection_dict["ROTORS_DYNAMIC"]
        self._permutations = scrambler_perms(reflectors, rotors_dynamic, [])

    def _catalog_hash(self):
        """
        
        """
        hash_str = ""

        dir = os.path.dirname(__file__)

        dir = os.path.join(dir, "cyclometer_catalog")

        if not os.path.isdir(dir):
            raise CatalogError(f"{dir} does not exist")
        
        for machine_type in self._machines:
            machine_dir = os.path.join(dir, machine_type.replace(" ","_"))

            if not os.path.isdir(machine_dir):
                raise CatalogError(f"{machine_dir} does not exist")
            
            perms = self._make_perms(machine_type)

            for perm in perms:

                dname = f"{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}"
                dpath = os.path.join(machine_dir, dname)
            
                for l in self.LETTERS:
                    fname = f"{l}_{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}.json"

                    fpath = os.path.join(dpath, fname)

                    if not os.path.isfile(fpath):
                        raise CatalogError(f"{fpath} does not exist")
                    
                    else:
                        with open(fpath, "r") as f:
                            data = f.read()

                            hash = sha256(data.encode("utf-8")).hexdigest()

                            hash_str += hash

        hash = sha256(hash_str.encode("utf-8")).hexdigest()
                    
        return hash
