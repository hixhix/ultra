from hashlib import sha256
from enigma_core.factory import make_machine
from enigma_tools.setting_tools.setting_tools import scrambler_perms
from zygalski_sheets.sheet_data import SheetDataGenerator
import multiprocessing
import shutil
import json
import os


class CatalogError(Exception):

    def __init__(self, err_msg):
        super().__init__(err_msg)


class ZygalskiSheetCatalog:

    LETTERS = [chr(i) for i in range(65, 91)]

    def __init__(self):
        self._machines = ["WEHRMACHT early","WEHRMACHT late"]

    def make_catalog(self):
        """
        
        """
        dir = os.path.dirname(__file__)

        dir = os.path.join(dir, "zygalski_catalog")

        if os.path.isdir(dir):
            shutil.rmtree(dir)
 
        for machine_type in self._machines:
            self._make_machine_catalog(machine_type)

        hash = self._catalog_hash()

        hash_fpath = os.path.join(dir, "hash_value.txt")

        with open(hash_fpath, "w") as f:
            f.write(hash)    

    def check_catalog(self):
        """
        
        """
        # check all files exist
        dir = os.path.dirname(__file__)

        dir = os.path.join(dir, "zygalski_catalog")

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

        processes = []

        perms = self._make_perms(machine_type)

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

    def _catalog_hash(self):
        """
        
        """
        hash_str = ""

        dir = os.path.dirname(__file__)

        dir = os.path.join(dir, "zygalski_catalog")

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
