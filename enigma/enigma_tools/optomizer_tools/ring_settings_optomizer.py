"""

Inputs:

1. cipher_text
2. settings
3. partial plugboard settings

Optomizes on index of coincidence

Method:

For each ring setting it maintains the same core rotor start positions.

ROTOR_SETTINGS      RING_SETTINGS       EQUIVILANT
A A V               D E F               D E Z
"""
from enigma_core.factory import make_machine
from enigma_tools.setting_tools.setting_tools import RotorSettings
from enigma_tools.crypto_tools.crypto_tools import bigram_count, trigram_count, index_of_coincidence
from collections import deque


class RingSettingsOptomizer:

    LETTERS = [chr(i) for i in range(65,91)]

    def __init__(self, machine_type, cipher_text, settings, start_settings, verbose=False):
        """
        
        """
        self._machine_type = machine_type
        self._cipher_text = cipher_text
        self._settings = settings
        self._start_settings = start_settings
        self._verbose = verbose
        self._translations = {"RS":{},"RM":{},"RF":{}}
        self._machine = make_machine(self._machine_type)
        self._rotor_settings = RotorSettings('L',3)
        self._settings["SCRAMBLER_SETTINGS"]["RING_SETTINGS"] = self._make_start_ring_settings()
        self._make_translations()
        self._ioc = 0
        self._best_settings = []

    def solve(self):
        """
        
        """
        while True:
            self._set_settings()
            output_text = ""

            for c in self._cipher_text:
                if c in self.LETTERS:
                    output_text += self._machine.character_input(c)

            self._check_text(output_text)

            try:
                self._rotor_settings.inc()
            except StopIteration:
                break

        return self._best_settings

    def _make_translations(self):
        """
        
        """
        for position in ["RS","RM","RF"]:
            lets = deque(self.LETTERS)
            lets.rotate(-(self.LETTERS.index(self._settings["SCRAMBLER_SETTINGS"]["RING_SETTINGS"][position])))
            for i in range(26):
                self._translations[position][self.LETTERS[i]] = lets[i]

    def _check_text(self, text):
        """
        
        """
        ioc = index_of_coincidence(text)
        _bigram_count = bigram_count(text)
        _trigram_count = trigram_count(text)

        settings ={
            "ROTOR_SETTINGS":self._settings["SCRAMBLER_SETTINGS"]["ROTOR_SETTINGS"],
            "RING_SETTINGS":self._settings["SCRAMBLER_SETTINGS"]["RING_SETTINGS"],
            "index_of_coincidence":ioc[2],
            "bigram_count":_bigram_count[1],
            "trigram_count":_trigram_count[1]
        }
        self._best_settings.append((settings, ioc[2]))

        rotor_settings = self._settings["SCRAMBLER_SETTINGS"]['ROTOR_SETTINGS']
        rot_rs = rotor_settings["RS"]
        rot_rm = rotor_settings["RM"]
        rot_rf = rotor_settings["RF"]

        ring_settings = self._settings["SCRAMBLER_SETTINGS"]['RING_SETTINGS']
        rng_rs = ring_settings["RS"]
        rng_rm = ring_settings["RM"]
        rng_rf = ring_settings["RF"]

        if self._verbose:
            print(f"ROTOR SETTINGS ({rot_rs}{rot_rm}{rot_rf})  "
                  f"RING SETTINGS ({rng_rs}{rng_rm}{rng_rf})  "
                  f"IOC {ioc[2]:.4f}   "
                  f"BIGRAM {str(_bigram_count[1]).rjust(7, ' ')}  "
                  f"TRIGRAM {str(_trigram_count[1]).rjust(7, ' ')}")

        self._best_settings.sort(key = lambda x:x[1])
        self._best_settings.reverse()

        if len(self._best_settings) > 10:
            self._best_settings = self._best_settings[0:26]

    def _set_settings(self):
        """
        
        """
        rotor_settings = self._rotor_settings.settings

        self._settings["SCRAMBLER_SETTINGS"]["ROTOR_SETTINGS"] = rotor_settings

        rf = self._translations["RF"][rotor_settings["RF"]]
        rm = self._translations["RM"][rotor_settings["RM"]]
        rs = self._translations["RS"][rotor_settings["RS"]]

        ring_settings = {
            "RF":rf,
            "RM":rm,
            "RS":rs
        }

        self._settings["SCRAMBLER_SETTINGS"]["RING_SETTINGS"] = ring_settings
        self._machine.settings = self._settings

    def _make_start_ring_settings(self):
        """
        
        """
        positions = ["RS","RM","RF"]
        ring_settings = {}

        for pos in positions:
            ring_settings[pos] = self.LETTERS[(25 - self.LETTERS.index(self._start_settings[pos])) + 1]

        return ring_settings
