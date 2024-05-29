from itertools import permutations, combinations
from collections import namedtuple


def scrambler_perms(reflectors, rotors_dynamic, rotors_static=None):
    rotor_dynamic_perms = list(permutations(rotors_dynamic, 3))
    settings = []
    if rotors_static:
        Setting = namedtuple("Setting", ["REF","R4","RS","RM","RF"])
        for reflector in reflectors:
            for rotor in rotors_static:
                for perm in rotor_dynamic_perms:
                    settings.append(Setting(reflector, rotor, *perm))
    else:
        Setting = namedtuple("Setting", ["REF","RS","RM","RF"])
        for reflector in reflectors:
            for perm in rotor_dynamic_perms:
                settings.append(Setting(reflector, *perm))
    return settings


class RotorSettings:
    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f'{i}'.rjust(2, '0') for i in range(1, 27)]

    def __init__(self, char_flag='L', positions=3, stop=True):
        self.char_flag = char_flag
        self.positions = positions
        self.stop = stop
        self.char_set = self.LETTERS if self.char_flag == 'L' else self.NUMBERS
        self.value = 0

    @property
    def settings(self):
        settings = {}
        positions = ["RF","RM","RS","R4"]

        for i in range(self.positions):
            position = i+1
            settings[positions[i]] = self._setting(position)

        return settings

    @settings.setter
    def settings(self, settings):
        value = 0
        positions = ["RF","RM","RS","R4"]
        for i in range(len(self.positions)):
            position = positions[i]
            try:
                setting = settings[position]
                setting = self._valid_setting(setting)
            except KeyError as e:
                raise e
            else:
                n = (self.char_set.index(setting) + 1)
                value += (n**i)
        self.value = value

    def inc(self):
        self.value += 1
        if self.value >= 26**self.positions:
            if self.stop:
                raise StopIteration()
            self.value = 0

    def dec(self):
        self.value -= 1
        if self.value < 0:
            if self.stop:
                raise StopIteration()
            self.value = (26**self.positions)-1

    def reset(self):
        self.value = 0

    def _valid_setting(self, setting):
        if setting not in self.char_set:
            raise Exception(f"{setting} is not a valid setting. Must be in {self.char_set}")
        else:
            return setting.upper()

    def _setting(self, position):
        #position 1-4
        return self.char_set[(self.value//(26**(position-1)))%26]

