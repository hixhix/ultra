from enigma_core.factory import make_machine
from enigma_tools.setting_tools.setting_tools import scrambler_perms, RotorSettings
import json
import os
import re


def filter_permutations(machine_type, loops_str):
    """
    
    """
    loops = extract_loops(loops_str)

    matches = []

    machine_obj = make_machine(machine_type)

    collection = machine_obj.scrambler.collection.collection_dict()

    reflectors = collection["REFLECTORS"]
    rotors_dynamic = collection["ROTORS_DYNAMIC"]
    rotors_static = collection["ROTORS_STATIC"]

    perms = scrambler_perms(reflectors, rotors_dynamic, rotors_static)

    groups = ["G1","G2","G3"]

    for perm in perms:
        perm_str = f"{perm.REF}_{perm.RS}_{perm.RM}_{perm.RF}"
        dirpath = os.path.dirname(__file__)
        dirpath = os.path.join(dirpath, "cyclometer_catalog")
        dirpath = os.path.join(dirpath, machine_type.replace(" ","_"))
        fpath = os.path.join(dirpath, perm_str)

        with open(fpath, "r") as f:
            data = json.load(f)

        rotor_settings = RotorSettings('L', 3, True)

        while True:
            settings = rotor_settings.settings

            rs = settings["RS"]
            rm = settings["RM"]
            rf = settings["RF"]
            settings_str = f"{rs}{rm}{rf}"

            if loops == data[settings_str]:
                matches.append(f"{perm_str.ljust(18)} {settings_str}")
            
            try:
                rotor_settings.inc()
            except StopIteration:
                break

    return matches

def extract_loops(loops_str):
    """
        
    """
    #print(loops_str)
    loops = re.search(r"G1[^(]?([()\d]+).?G2[^(]?([()\d]+).?G3[^(]?([()\d]+)", loops_str)
    #print(loops.group(1))
    #print(loops.group(2))
    #print(loops.group(3))
    if not loops:
        err_msg = f"{loops_str} is not a valid loops string."
        raise Exception(err_msg)
    else:
        loops_dict = {
            "G1":loops.group(1),
            "G2":loops.group(2),
            "G3":loops.group(3)
        }

        return loops_dict