from enigma_core.validators.scrambler_validators.scrambler_validators import *
from zygalski_sheets.sheet_data import SheetDataGenerator
from collections import deque
from pprint import pprint
import json
import os


class ZygalskiTextSheetSolution:

    LETTERS = [chr(i) for i in range(65,91)]

    def __init__(self):
        """
        
        """
        self._indicators = None
        self._permutation = None
        self._rs = None
        self._sheet = None
        self._sheet_string = ""
        self._translations = None
        self._make_blank_sheet()

    def solution(self, machine_type, indicators, permutation, rs):
        """
        
        """
        self._machine_type = machine_type
        self._indicators = indicators
        self._permutation = permutation
        self._rs = rs
        self._make_translations()
        perm_dict = ScramblerValidators.valid_permutation_string(self._machine_type, permutation, rs_flag=False, group_flag=False)

        for indicator in indicators:
            groups = self._groups(indicator[4::])
            rm = indicator[1]
            rf = indicator[2]
            for group in groups:
                settings = {
                    "SCRAMBLER_SETTINGS":{
                        "REFLECTOR_TYPE":perm_dict["REFLECTOR"],
                        "ROTOR_TYPES":{
                            "RS":perm_dict["RS_TYPE"],
                            "RM":perm_dict["RM_TYPE"],
                            "RF":perm_dict["RF_TYPE"]
                        },
                        "ROTOR_SETTINGS":{
                            "RS":self._translations[indicator[0]],
                            "RM":"A",
                            "RF":"A"
                        },
                        "RING_SETTINGS":{"RS":'A',"RM":"A","RF":"A"}
                    }
                }
                sheet_data = self._get_sheet(settings)
                self._stack_sheet(sheet_data, rm, rf, group)
                reflector = perm_dict["REFLECTOR"]
                rs_type = perm_dict["RS_TYPE"]
                rm_type = perm_dict["RM_TYPE"]
                rf_type = perm_dict["RF_TYPE"]
                perm_str = f"{self._rs}_{reflector}_{rs_type}_{rm_type}_{rf_type}"
                self._sheet_string = self._sheet_str(perm_str, self._sheet)
        self._sheet = self._adjust_sheet()
        self._sheet_string = self._sheet_str(perm_str, self._sheet)

        return self._sheet_string
    
    def _make_translations(self):
        """
        
        """
        self._translations = {}
        offset = self.LETTERS.index(self._rs)
        lets = deque(self.LETTERS.copy())
        lets.rotate(offset)
        lets = list(lets)

        for i in range(26):
            c1 = self.LETTERS[i]
            c2 = lets[i]
            self._translations[c1] = c2

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

    def _make_blank_sheet(self):
        """
        
        """
        blank_sheet = {}

        for rm in self.LETTERS:
            for rf in self.LETTERS:
                blank_sheet[f"{rm}{rf}"] = True
        self._sheet = blank_sheet

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
        
    def _get_sheet(self, settings):
        """
        
        """
        generator = SheetDataGenerator()
        sheet = generator.data(settings, self._machine_type, "A")

        return sheet
    
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
    
    def _sheet_str(self, permutation, sheet):
        """
        
        """
        sheet_str = f"{permutation}\n\n"

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
                sheet_str += f" {self._rs}{ring_setting} "
            sheet_str += "\n"
        
        return sheet_str