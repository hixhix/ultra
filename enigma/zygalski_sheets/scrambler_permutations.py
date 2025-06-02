from enigma_core.scrambler.collection.collection import Collection
from enigma_tools.setting_tools.setting_tools import scrambler_perms, RotorSettings
from collections import deque
from pprint import pprint
import multiprocessing
import json
import os


class ScramblerPermutations:

    LETTERS = [chr(i) for i in range(65,91)]

    def __init__(self):
        """

        """
        self._sheet = None
        self._filtered_permutations = {}
        self._permutations = None
        self._indicator_groups = None
        self._verbose_flag = False
        self._sheet_data = {}

    def solve(self, machine_type, indicators, verbose_flag):
        """
        
        """
        self._machine_type = machine_type

        self._make_permutations()

        self._verbose_flag = verbose_flag

        self._indicator_groups = self.group_indicators(indicators)

        #for group in self._indicator_groups:
        #    print(group)

        for permutation in self._permutations:
            self._sheet_data = {}
            self._stack_sheets(permutation)

        return self._filtered_permutations

    @classmethod    
    def group_indicators(cls, indicators):
        """
        
        """
        letters = deque(cls.LETTERS)

        groups = []
        # 26 14 1
        for i in range(26):
            lets = list(letters)[0:14]

            group = []

            for indicator in indicators:
                if indicator[2] not in lets:
                    group.append(indicator)

            groups.append(group)

            letters.rotate(1)
           
        return groups
    
    def _stack_sheets(self, perm):
        """
        
        """
        ref = perm.REF
        rs = perm.RS
        rm = perm.RM
        rf = perm.RF
        perm_str = f"{ref}_{rs}_{rm}_{rf}"

        if self._verbose_flag:
            print(perm_str)

        for indicators in self._indicator_groups:
            if len(indicators) >= 6:
                #if len(indicators) > 12:
                #    indicators = indicators[0:12]
                #self._indicators = indicators

                #if perm_str != "UKW-B_I_IV_III":
                #    continue

                lets = deque(self.LETTERS) # for ceaser cipher shift on rs
                for i in range(26):
                    lets.rotate(1)

                    self._make_blank_sheet()

                    for indicator in indicators:
                        rs = indicator[0]
                        rm = indicator[1]
                        rf = indicator[2]
                        index = lets.index(rs) # get index of rs in lets
                        rs = self.LETTERS[index] # ceaser cipher shift on rs
                        indicator = indicator[4:10] # extract double enciphered message key indicator
                        groups = self._groups(indicator) # get groups
                        sheet = self._get_sheet(rs, perm_str) # get sheet data
                        for group in groups:
                            self._stack_sheet(sheet, rm, rf, group) # stack sheets
                    self._scan_sheet(perm_str, indicators, self.LETTERS[25-i]) # scan sheets for holes

    def _groups(self, indicator):
        """
        
        """
        groups = ["G1","G2","G3"]

        _groups = []

        if indicator[0] == indicator[3]:
            _groups.append(groups[0])
        if indicator[1] == indicator[4]:
            _groups.append(groups[1])
        if indicator[2] == indicator[5]:
            _groups.append(groups[2])
        return _groups

    def _get_sheet(self, rs, permutation):
        """
        
        """
        perm_str = f"{rs}_{permutation}"
        dirpath = os.path.dirname(__file__)
        dirpath = os.path.join(dirpath, "zygalski_catalog")
        dirpath = os.path.join(dirpath, self._machine_type.replace(" ","_"))
        dirpath = os.path.join(dirpath, permutation)
        fpath = os.path.join(dirpath, f"{rs}_{permutation}.json")

        if perm_str not in self._sheet_data.keys():
            with open(fpath, "r") as f:
                data = json.load(f)
                self._sheet_data[perm_str] = data
        else:
            data = self._sheet_data[perm_str]

        return data

    def _stack_sheet(self, sheet, rm, rf, group):
        """
        
        """
        x_offset = deque(self.LETTERS)
        x_offset.rotate(self.LETTERS.index(rm))
        y_offset = deque(self.LETTERS)
        y_offset.rotate(self.LETTERS.index(rf))

        settings_map = {f"{self.LETTERS[x]}{self.LETTERS[y]}":f"{x_offset[x]}{y_offset[y]}" for x in range(26) for y in range(26)}

        for norm, offset in settings_map.items():
            if not sheet[norm][group]:
                self._sheet[offset] = False

    def _make_permutations(self):
        """

        """
        reflectors = Collection.device_list(self._machine_type, ["REF"])
        rotors_dynamic = Collection.device_list(self._machine_type, ["R_ROT"])

        self._permutations = scrambler_perms(reflectors, rotors_dynamic)

    def _make_blank_sheet(self):
        """
        
        """
        blank_sheet = {}

        for rm in self.LETTERS:
            for rf in self.LETTERS:
                blank_sheet[f"{rm}{rf}"] = True
        self._sheet = blank_sheet
                        
    def _scan_sheet(self, permutation, indicators, rs):
        """
        
        """
        sheet = self._adjust_sheet()

        ring_settings = []

        count = 0

        for rm in self.LETTERS:
            for rf in self.LETTERS:
                ring_setting = f"{rm}{rf}"
                if sheet[ring_setting]:
                    ring_settings.append(ring_setting)
                    count += 1

        if count > 0:
            perm_str = f"{rs}_{permutation}"
            if perm_str not in self._filtered_permutations.keys():
                self._filtered_permutations[perm_str] = {
                    "count":count,
                    "rs":rs,
                    "indicators":indicators,
                    "ring_settings":ring_settings
                }
            else:
                self._filtered_permutations[perm_str]["count"] += 1
                self._filtered_permutations[perm_str]["indicators"] = indicators
                self._filtered_permutations[perm_str]["ring_settings"] = ring_settings

    def _adjust_sheet(self):
        """
        
        """
        l1 = [self.LETTERS[0]]
        l2 = self.LETTERS[1::]
        l2.reverse()
        translations = l1 + l2

        translation_map ={}

        for i in range(26):
            c1 = self.LETTERS[i]
            c2 = translations[i]
            translation_map[c1] = c2
            translation_map[c2] = c1

        adjusted_sheet = {}

        for rm in self.LETTERS:
            for rf in self.LETTERS:
                data = self._sheet[f"{rm}{rf}"]
                rm = translation_map[rm]
                rf = translation_map[rf]
                adjusted_sheet[f"{rm}{rf}"] = data

        return adjusted_sheet

    def _sheet_str(self, permutation, sheet):
        """
        
        """
        sheet_str = f"{permutation}\n"

        sheet_str += "  ABCDEFGHIJKLMNOPQRSTUVWXYZ\n  ||||||||||||||||||||||||||\n"

        ring_settings = []

        for y in self.LETTERS:
            for x in self.LETTERS:
                if x == 'A':
                    sheet_str += f"{y}-"
                if sheet[f"{x}{y}"]:
                    ring_settings.append(f"{x}{y}")
                    sheet_str += '#'
                else:
                    sheet_str += '.'
                if x == 'Z':
                    sheet_str += f"-{y}\n"
        sheet_str += "  ||||||||||||||||||||||||||\n  ABCDEFGHIJKLMNOPQRSTUVWXYZ\n"

        if ring_settings:
            sheet_str += "\nRing Settings "
            for ring_setting in ring_settings:
                sheet_str += f" {ring_setting} "
            sheet_str += "\n"
        
        return sheet_str
