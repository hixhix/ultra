import os
from enigma_core.factory import make_machine
from enigma_tools.setting_tools.setting_tools import scrambler_perms
from zygalski_sheets.sheet_data import SheetDataGenerator
import multiprocessing
import json


class ZygalskiSheetCatalog:

    LETTERS = [chr(i) for i in range(65, 91)]

    def __init__(self):
        self._machines = ["WEHRMACHT early","WEHRMACHT late"]

    def make_catalog(self):
        """
        
        """
        if not self.check_catalog():
 
            for machine_type in self._machines:
                self._make_machine_catalog(machine_type)

            return "Zygalski catalog successfully created."
        
        return "Zygalski catalog already exists."

    def check_catalog(self):
        """
        
        """
        # check all files exist
        dir = os.path.dirname(__file__)

        dir = os.path.join(dir, "zygalski_catalog")

        if not os.path.isdir(dir):
            return False

        for machine_type in self._machines:
            machine_dir = os.path.join(dir, machine_type.replace(" ","_"))

            if not os.path.isdir(machine_dir):
                return False
            
            machine = make_machine(machine_type)

            collection = machine.scrambler.collection.collection_dict()
            rotors_static = collection["ROTORS_STATIC"]
            rotors_dynamic = collection["ROTORS_DYNAMIC"]
            reflectors = collection["REFLECTORS"]

            perms = scrambler_perms(reflectors, rotors_dynamic, rotors_static)

            for perm in perms:

                dname = f"{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}"
                dpath = os.path.join(machine_dir, dname)
            
                for l in self.LETTERS:
                    fname = f"{l}_{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}.json"

                    fpath = os.path.join(dpath, fname)

                    if not os.path.isfile(fpath):
                        return False
                    
        return True

    def force_make_catalog(self):
        """
        
        """
        self.make_catalog()

        return "Zygalski catalog successfully created."

    def _make_machine_catalog(self, machine_type):
        """
        
        """
        dir = os.path.dirname(__file__)

        dir = os.path.join(dir, "zygalski_catalog")

        if not os.path.isdir(dir):
            os.mkdir(dir)

        dir = os.path.join(dir, machine_type.replace(" ","_"))

        if not os.path.isdir(dir):
            os.mkdir(dir)

        machine = make_machine(machine_type)

        collection = machine.scrambler.collection.collection_dict()
        rotors_static = collection["ROTORS_STATIC"]
        rotors_dynamic = collection["ROTORS_DYNAMIC"]
        reflectors = collection["REFLECTORS"]

        perms = scrambler_perms(reflectors, rotors_dynamic, rotors_static)

        processes = []

        for perm in perms:
            p = multiprocessing.Process(target=self.make_permutation_catalog, args=[perm, dir, machine_type])
            p.start()
            processes.append(p)

        for process in processes:
            process.join()

    def make_permutation_catalog(self, perm, dir, machine_type):
        """
        
        """
        dname = f"{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}"
        dpath = os.path.join(dir, dname)

        if not os.path.isdir(dpath):
            os.mkdir(dpath)

        for l in self.LETTERS:
            settings = {
                    "SCRAMBLER_SETTINGS":{
                    "SCRAMBLER_CHARSET_FLAG":"L",
                    "REFLECTOR_TYPE":perm.REF,
                    "ROTOR_TYPES":{"RS":perm.RS,"RM":perm.RM,"RF":perm.RF},
		            "ROTOR_SETTINGS":{"RS":l,"RM":"A","RF":"A"}
                }
            }

            fname = f"{l}_{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}.json"
            fpath = os.path.join(dpath, fname)
            print(fname)
            if os.path.isfile(fpath):
                continue

            generator = SheetDataGenerator()
            data = generator.data(settings, machine_type, 'M')
            data = json.dumps(data)

            with open(fpath, "w") as f:
                f.write(data)
