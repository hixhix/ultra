"""
TEST EXAMPLE FOR WEHRMACHT

REFLECTOR TYPE:         UKW-B
ROTOR TYPES:            III     II      I
ROTOR SETTINGS:         A       A       V
RING SETTINGS:          A       A       A
PLUGBOARD SETTINGS:     AC,BD,EG,FH,IK,JL,MO,NP,QS,RT
PERMUTATION:            UKW-B_III_II_I

PLAIN TEXT:             WEATHERFORECASTBISCAY
CIPHER TEXT:            YHXBDYCWCJAQPBLMHMBGP


TEST EXAMPLE FOR KRIEGSMARINE M3

REFLECTOR TYPE:         UKW-B
ROTOR TYPES:            III     II      I
ROTOR SETTINGS:         A       A       V
RING SETTINGS:          A       A       A
PLUGBOARD SETTINGS:     AC,BD,EG,FH,IK,JL,MO,NP,QS,RT
PERMUTATION:            UKW-B_III_II_I

PLAIN TEXT:             WEATHERFORECASTBISCAY
CIPHER TEXT:            YHXBDYCWCJAQPBLMHMBGP


TEST EXAMPLE FOR KRIEGSMARINE M4

REFLECTOR TYPE:         UKW-B
ROTOR TYPES:            Beta    III     II      I
ROTOR SETTINGS:         A       A       A       V
RING SETTINGS:          A       A       A       A
PLUGBOARD SETTINGS:     AC,BD,EG,FH,IK,JL,MO,NP,QS,RT
PERMUTATION:            UKW-B_Beta_III_II_I

PLAIN TEXT:             WEATHERFORECASTBISCAY
CIPHER TEXT:            YHXBDYCWCJAQPBLMHMBGP

"""

from enigma_core.factory import make_machine
from enigma_core.validators.scrambler_validators.scrambler_validators import *
from enigma_tools.setting_tools.setting_tools import RotorSettings
from collections import deque
from pprint import pprint
import os


class BombeMachine:

    LETTERS = [chr(i) for i in range(65,91)]

    def __init__(self, plain_text, cipher_text, permutation, machine_type, csko=False, diagonal_board=True):
        """
        
        """
        self._plain_text = plain_text
        self._cipher_text = cipher_text
        self._permutation = permutation
        self._machine_type = machine_type
        self._positions = None
        self._csko = csko
        self._diagonal_board = diagonal_board
        self._test_register = None
        self._cables = None
        self._registers = {l:[False for i in range(26)] for l in self.LETTERS}
        self._stops = []
        self._scramblers = None
        self._menu_chars = None
        self._bombe_str = None
        self._get_positions()
        self._machine = self._make_machine(machine_type)
        self._rotor_settings_gen = RotorSettings('L', self._positions)
        self._perm = self._valid_permutation()
        self._menu_characters()
        self._initialize_logs()
        self._valid_crib()
        self._initialize_bombe()

    def solve(self):
        """
        
        """
        print(f"STARTING RUN ON {self._machine_type} {self._permutation}")
        while True:
            self._wire_scramblers()
            for _ in range(26):
                self._bombe_str = self._bombe_settings_str()
                self._check_stop()
                self._scramblers.rotate(-1)
                try:
                    self._rotor_settings_gen.inc()
                    pprint(self._rotor_settings_gen.settings)
                except StopIteration:
                    print(f"FINISHED RUN ON {self._permutation}")
                    return self._stops
        
    def _initialize_bombe(self):
        """
        
        """
        self._initialize_machine()
        self._wire_bombe()
        self._test_register = self._menu_chars[0]
        
    def _initialize_machine(self):
        """
        
        """
        perm_dict = self._perm[1]
        settings = {
            "reflector":perm_dict["REF"],
            "rotor_types":{
                "RS":perm_dict["ROT_RS"],
                "RM":perm_dict["ROT_RM"],
                "RF":perm_dict["ROT_RF"]
            },
            "ring_settings":{"RS":"A","RM":"A","RS":"A"},
            "turnover_flag":False
        }

        if "ROT_R4" in perm_dict.keys():
            settings["rotor_types"]["R4"] = perm_dict["ROT_R4"]

        self._machine.settings = settings
        self._set_machine()  

    def _get_positions(self):
        """
        
        """
        if self._machine_type == "WEHRMACHT":
            self._positions = 3
        elif self._machine_type == "Kriegsmarine M3":
            self._positions = 3
        elif self._machine_type == "Kriegsmarine M4":
            self._positions = 4
        else:
            err_msg = f"{self._machine_type} is not a valid enigma machine"
            raise Exception(err_msg)

    def _valid_crib(self):
        """
        
        """
        self._plain_text = self._plain_text.upper()
        self._cipher_text = self._cipher_text.upper()

        if len(self._plain_text) != len(self._cipher_text):
            err_msg = (f"Plain text is length {len(self._plain_text)} and the cipher text is length {len(self._cipher_text)}\n. "
                       f"Plain text and cipher text Must be the same length.")
            raise Exception(err_msg)

        for l in self._plain_text:
            if l not in self.LETTERS:
                err_msg = f"Character {l} in plain text is not valid. Must be A-Z."
                raise Exception(err_msg)

        for i in self._cipher_text:
            if l not in self.LETTERS:
                err_msg = f"Character {l} in cipher text is not valid. Must be A-Z."
                raise Exception(err_msg)

        for i in range(len(self._plain_text)):
            if self._plain_text[i] == self._cipher_text[i]:
                err_msg = (f"Plain text and cipher text has the same letter {self._plain_text[i]} at index {i}. "
                           f"A letter at an index in the plain text must be different "
                           f"from the letter in the cipher text at the same index.")
                raise Exception(err_msg)

    def _menu_characters(self):
        """
        
        """
        text = self._plain_text + self._cipher_text
        self._menu_chars = list(set(text))
        self._menu_chars.sort()

    def _valid_permutation(self):
        """
        
        """
        if self._positions != 3 and self._positions != 4:
            err_msg = f"{self._positions} is an invalid value for positions. Must be integer with value of 3 or 4"
            raise Exception(err_msg)

        perm = None

        try:
            perm = ScramblerValidators.valid_permutation_string(self._machine_type, self._permutation, rs_flag=True, group_flag=True)
        except PermutationError:
            pass
        if not perm:
            try:
                perm = ScramblerValidators.valid_permutation_string(self._machine_type, self._permutation, rs_flag=False, group_flag=True)
            except PermutationError:
                pass
        if not perm:
            try:
                perm = ScramblerValidators.valid_permutation_string(self._machine_type, self._permutation, rs_flag=False, group_flag=False)
            except PermutationError:
                err_msg = f"Permutation {self._permutation} is not a valid permutation."
                raise PermutationError(err_msg)

        if self._positions == 4 and "R4_TYPE" not in perm[1].keys():
            err_msg = f""
            raise Exception(err_msg)
        elif self._positions == 3 and "R4_TYPE" in perm[1].keys():
            err_msg = ""
            raise Exception(err_msg)

        return perm

    def _make_machine(self, machine_type):
        """
        
        """
        try:
            machine_obj = make_machine(machine_type)
        except Exception as e:
            raise e

        return machine_obj

    def _set_machine(self):
        """
        
        """
        rot_settings = self._rotor_settings_gen.settings
        settings = {
            "SCRAMBLER_SETTINGS":{
                "ROTOR_SETTINGS":{
                    "RS":rot_settings["RS"],
                    "RM":rot_settings["RM"],
                    "RF":rot_settings["RF"]
                }
            }
        }

        if "R4" in rot_settings.keys():
            settings["SCRAMBLER_SETTINGS"]["ROTOR_SETTINGS"]["R4"] = rot_settings["R4"]

        self._machine.settings = settings

    def _wire_bombe(self):
        """
        
        """
        self._cables = {c:[] for c in self._menu_chars}

        for i in range(len(self._plain_text)):
            p = self._plain_text[i]
            c = self._cipher_text[i]
            self._cables[p].append(
                {
                    "position":i,
                    "cable":c
                }
            )
            self._cables[c].append(
                {
                    "position":i,
                    "cable":p
                }
            )

    def _wire_scramblers(self):
        """
        
        """
        self._set_machine()
        scramblers = []

        for _ in range(26):
            scrambler = {}
            self._machine.character_input('A')
            for cin in self.LETTERS:
                cout = self._machine.non_keyed_input(cin)
                scrambler[cin] = cout
            scramblers.append(scrambler)

        self._scramblers = deque(scramblers)

    def _trace_paths(self, cable, wire):
        """
        
        """
        wires = []
        self._trace_path(cable, wire, wires)

    def _trace_path(self, cable, wire, wires):
        """
        
        """
        # record cable and wire in wires.
        wires.append(f"{cable}{wire}")
        # set this wire in this cables register to True.
        self._registers[cable][self.LETTERS.index(wire)] = True
        # if diagonal board applicable set wire in connected cable.
        if (cable != wire) and wire in self._menu_chars and f"{wire}{cable}" not in wires and self._diagonal_board:
            self._trace_path(wire, cable, wires)
        # for scrambler connected to cable trace path in connected cables.
        for scrambler_dict in self._cables[cable]:
            position = scrambler_dict["position"]
            conn_cable = scrambler_dict["cable"]
            scrambler = self._scramblers[position]
            conn_wire = scrambler[wire]
            if f"{conn_cable}{conn_wire}" not in wires:
                self._trace_path(conn_cable, conn_wire, wires)

    def _check_stop(self):
        """
        
        """
        self._reset_registers()
        self._trace_paths(self._test_register, 'A')
        if (self._registers[self._test_register].count(True) == 26):
            return False
        else:
            # check for 1 or 25 wires
            for l in self.LETTERS:
                self._reset_registers()
                self._trace_paths(self._test_register, l)
                if (self._registers[self._test_register].count(True) == 25):
                    # make 1 wire in each registry live and look for contradictions.
                    self._invert_registers()
                if (self._registers[self._test_register].count(True) == 1):
                    if self._csko:
                        if self._valid_registers() and self._no_contradictions() and self._no_consecutive_steckers():
                            self._record_stop_settings()
                            self._record_stop(l)
                            break
                    else:
                        if self._valid_registers() and self._no_contradictions():
                            self._record_stop_settings()
                            self._record_stop(l)
                            break
                
    def _valid_registers(self):
        """
        
        """
        for c in self._menu_chars:
            if self._registers[c].count(True) not in [0,1]:
                return False
        return True

    def _invert_registers(self):
        """
        
        """
        for c in self._menu_chars:
            register = self._registers[c]
            for i in range(len(register)):
                if register[i] == True:
                    register[i] = False
                elif register[i] == False:
                    register[i] = True

    def _reset_registers(self):
        """
        
        """
        self._registers = {l:[False for i in range(26)] for l in self.LETTERS}

    def _no_contradictions(self):
        """
        
        """
        pairs = {}

        for c1 in self._menu_chars:
            try:
                ind = self._registers[c1].index(True)
            except ValueError:
                continue
            else:
                c2 = self.LETTERS[ind]

                if (c1 in pairs.keys() and c2 != pairs[c1]) or (c2 in pairs.keys() and c1 != pairs[c2]):
                    return False
                else:
                    pairs[c1] = c2
                    pairs[c2] = c1
        return True
    
    def _no_consecutive_steckers(self):
        """
        
        """
        steckers = self._stecker_pairs()

        for pair in steckers:
            n1 = ord(pair[0])
            n2 = ord(pair[1])
            if (n1 == 65 and n2 == 90) or (n1 == 90 and n2 == 65):
                return False
            elif n2 == n1+1 or n2 == n1-1:
                return False
        return True

    def _stecker_pairs(self):
        """
        
        """
        stecker_pairs = []

        for c1 in self._menu_chars:
            try:
                ind = self._registers[c1].index(True)
            except ValueError:
                continue
            else:
                c2 = self.LETTERS[ind]
                pair = [c1,c2]
                pair.sort()
                stecker_pairs.append(pair)

        stecker_pairs = [tuple(pair) for pair in set(tuple(pair) for pair in stecker_pairs)]
        stecker_pairs = sorted(stecker_pairs, key=lambda x: x[0])

        return stecker_pairs

    def _record_stop_settings(self):
        """
        
        """
        steckers = self._stecker_pairs()

        stop = {
            "settings":self._rotor_settings_gen.settings,
            "stecker_pairs":steckers
        }
        self._stops.append(stop)

        steckers_str = f""

        for pair in steckers:
            steckers_str += f"{pair[0]}{pair[1]} "
        
        fpath = os.path.join("bombe_logs","stops.log")

        with open(fpath,"a+") as f:
            f.write(f"{self._permutation} {self._bombe_settings_str()} {steckers_str}\n")

    def _record_stop(self, c):
        """
        
        """
        registers_str = f"{self._permutation} {self._bombe_settings_str()}\n"
        registers_str += self._registers_str(c)

        fpath = os.path.join("bombe_logs","registers.log")

        with open(fpath, "a+") as f:
            f.write(f"{registers_str}\n")

    def _registers_str(self, c):
        """
        
        """
        reg_str = (f"Test Register {self._test_register}: Test Wire {c}\n"
                   f"  {self._menu_str()}\n"
                   f"  {''.join(self.LETTERS)}\n")

        for l in self.LETTERS:
            reg_str += f"{self._register_str(l)}\n"
        return reg_str

    def _register_str(self, l):
        """
        
        """
        reg_str = f"{l} "

        register = self._registers[l]
        for b in register:
            if b:
                reg_str += '|'
            elif not b:
                reg_str += '-'
        if l in self._menu_chars:
            reg_str += '='
        return reg_str

    def _bombe_settings_str(self):
        """
        
        """
        settings = self._rotor_settings_gen.settings
        rs = settings["RS"]
        rm = settings["RM"]
        rf = settings["RF"]

        settings_str = f"{rs}{rm}{rf}"

        if "R4" in settings.keys():
            r4 = settings["R4"]
            settings_str == r4
        
        return settings_str
    
    def _menu_str(self):
        """
        
        """
        menu_str = ""

        for l in self.LETTERS:
            if l not in self._menu_chars:
                menu_str += '_'
            else:
                menu_str += l
        return menu_str

    def _log_stop(self, c):
        """
        
        """
        stop_setting = self._bombe_settings_str()

        for stop in self._stops:
            if stop == stop_setting:
                self._record_stop(c)
    
    def _initialize_logs(self):
        """
        
        """
        if not os.path.isdir("bombe_logs"):
            os.mkdir("bombe_logs")
