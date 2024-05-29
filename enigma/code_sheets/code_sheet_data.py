from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from collections import deque
import random


class CodeSheetData:

    def msg_id_list(number):
        id_list = []

        while len(id_list) < number:
            id_str = ""
            for i in range(3):
                id_str += random.choice(LETTERS)
            if id_str not in id_list:
                id_list.append(id_str)

        return id_list

    def reflector_types_list(machine_type, n):
        reflectors = EQUIPMENT_DICT[machine_type]["REFLECTORS"]

        reflector_types_list = []

        for reflector_type, ref_dict in reflectors.items():
            if ref_dict["rewireable"] == False:
                reflector_types_list.append(reflector_type)

        reflector_list = []

        for i in range(n):
            reflector_list.append(random.choice(reflector_types_list))

        return reflector_list
    
    def reflector_wiring_list(charset_flag):
        wire_lists = []

        charset = LETTERS if charset_flag == "L" else NUMBERS

        for i in range(3):
            wire_list = []
            wire_list_chars = charset.copy()
            random.shuffle(wire_list_chars)
            for n in range(13):
                c1 = wire_list_chars.pop()
                c2 = wire_list_chars.pop()
                wire_list.append([c1,c2])
            wire_lists.append(wire_list)

        return wire_lists

    def rotor_types_list(machine_type, number, non_repeat=False):
        positions = ["RF","RM","RS"]

        rotor_types_list = []

        rotors_dict = EQUIPMENT_DICT[machine_type]["ROTORS"]

        rotors_dynamic = [r for r in rotors_dict.keys() if len(rotors_dict[r]["turnover_chars"]) != 0]
        rotors_static = [r for r in rotors_dict.keys() if len(rotors_dict[r]["turnover_chars"]) == 0]

        for n in range(number):
            rotor_types = {}
            while True:
                used = []
                for i in range(3):
                    while True:
                        rotor_type = random.choice(rotors_dynamic)
                        if rotor_type not in used:
                            rotor_types[positions[i]] = rotor_type
                            used.append(rotor_type)
                            break
                if rotors_static:
                    rotor_types["R4"] = random.choice(rotors_static)

                if non_repeat and rotor_types in rotor_types_list:
                    continue
                else:
                    if len(rotor_types_list) != 0 and rotor_types != rotor_types_list[-1]:
                        rotor_types_list.append(rotor_types)
                        break
                    elif len(rotor_types_list) == 0:
                        rotor_types_list.append(rotor_types)
                        break
                    else:
                        continue

        return rotor_types_list

    def ring_settings_list(charset_flag, number, positions=3):
        rotor_positions = ["RF","RM","RS","R4"]

        ring_settings_list = []

        charset = LETTERS if charset_flag == "L" else NUMBERS

        for n in range(number):
            ring_settings = {}
            for p in range(positions):
                if p != 3:
                    ring_settings[rotor_positions[p]] = random.choice(charset)
                elif p == 3:
                    ring_settings[rotor_positions[p]] = charset[0]
            ring_settings_list.append(ring_settings)

        return ring_settings_list

    def rotor_settings_list(charset_flag, number, positions=3):
        rotor_positions = ["RF","RM","RS","R4"]

        rotor_settings_list = []

        charset = LETTERS if charset_flag == "L" else NUMBERS

        for n in range(number):
            rotor_settings = {}
            for p in range(positions):
                rotor_settings[rotor_positions[p]] = random.choice(charset)
            rotor_settings_list.append(rotor_settings)

        return rotor_settings_list

    def stecker_plugboard_connections(charset_flag, number, pairs, csko=False):
        def consecutive(charset, char):
            c1 = None
            c2 = None
            index = charset.index(char)

            if index != 0:
                c1 = charset[index -1]
            elif index == 0:
                c1 = charset[-1]
            if index != len(charset) -1:
                c2 = charset[index] +1
            elif index == len(charset) -1:
                c2 = charset[index] +1

            return [c1,c2]

        plugboard_connections_list = []

        charset = LETTERS if charset_flag == "L" else NUMBERS

        for n in range(number):
            used = []
            plugboard_connections = []
            for p in range(pairs):
                pair = []
                c1 = None
                while True:
                    c1 = random.choice(charset)
                    if c1 not in used:
                        pair.append(c1)
                        used.append(c1)
                        break
                while True:
                    c2 = random.choice(charset)
                    if c2 not in used:
                        if (csko == False) or (csko == True and c2 not in consecutive(charset, c2)):
                            pair.append(c2)
                            used.append(c2)
                            break
                plugboard_connections.append(pair)
            plugboard_connections_list.append(plugboard_connections)
        return plugboard_connections_list

    def uhr_box_plugboard_connections(charset_flag, number):
        plugboard_connections_list = []

        charset = LETTERS if charset_flag == "L" else NUMBERS

        for n in range(number):
            conns = charset.copy()
            random.shuffle(conns)
            conns = conns[0:20]
            plugboard_connections_list.append(conns)

        return plugboard_connections_list

    def uhr_settings_list(number):
        uhr_settings_list = []

        for n in range(number):
            uhr_settings_list.append(random.randrange(0,39))

        return uhr_settings_list

    def kengruppen_list(charset_flag, number):
        kengruppen_list = []

        used = []

        charset = LETTERS if charset_flag == "L" else NUMBERS

        for n in range(number):
            group_list = []
            while len(group_list) < 4:
                group_str = ""
                for i in range(3):
                    group_str += random.choice(charset)
                    if i != 2 and charset_flag == "N":
                        group_str += "/"
                if group_str not in used:
                    group_list.append(group_str)
                    used.append(group_str)
            kengruppen_list.append(group_list)

        return kengruppen_list
    
    def bigram_dict(charset_flag):
        bigram_dict = {}

        charset = LETTERS if charset_flag == "L" else NUMBERS

        pairs = []

        for c1 in charset:
            for c2 in charset:
                pairs.append([c1,c2])

        random.shuffle(pairs)

        pairs = deque(pairs)

        while len(pairs) != 0:
            c1,c2 = pairs.pop()
            c3 = None
            c4 = None
            while True:
                c3,c4 = pairs[0]
                if c3 != c1:
                    break
                elif len(pairs) == 1:
                    return CodeSheetData.bigram_dict(charset_flag)
                else:
                    pairs.rotate(1)
            pairs.remove([c3,c4])
            if charset_flag == "L":
                bigram_dict[f"{c1}{c2}"] = f"{c3}{c4}"
                bigram_dict[f"{c3}{c4}"] = f"{c1}{c2}"
            elif charset_flag == "N":
                bigram_dict[f"{c1}/{c2}"] = f"{c3}/{c4}"
                bigram_dict[f"{c3}/{c4}"] = f"{c1}/{c2}"

        return bigram_dict