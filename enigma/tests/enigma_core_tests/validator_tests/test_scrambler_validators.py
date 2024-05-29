import unittest
from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.validators.scrambler_validators import ScramblerValidators as SV
from enigma_core.validators.scrambler_validators import (ReflectorTypeError,
                                                         RotorTypesStringError,
                                                         RotorSettingsStringError,
                                                         RingSettingsStringError,
                                                         RotorTypesDictError,
                                                         RotorSettingsDictError,
                                                         RingSettingsDictError,
                                                         RingCharacterError,
                                                         PermutationError)


class TestScramblerValidators(unittest.TestCase):

    def test_valid_reflector_type(self):
        """
        Takes a reflector type string and returns the EQUIPMENT_DICT
        repressentation if valid. If not valid raises ReflectorTypeError.
        """
        passing_tests = [
            ["WEHRMACHT_early","ukw-a","UKW-A"],
            ["WEHRMACHT_late","ukw-b","UKW-B"],
            ["Kriegsmarine_M3","ukw-b","UKW-B"],
            ["Kriegsmarine_M4","ukw-c","UKW-C"]
        ]

        failing_tests = [
            ["WEHRMACHT_early","UKW-B"],
            ["WEHRMACHT_late","UKW-A"]
        ]

        for data in passing_tests:
            machine_type, reflector_string, output = data
            self.assertEqual(SV.valid_reflector_type(machine_type, reflector_string), output)

        for data in failing_tests:
            machine_type, reflector_string = data
            self.assertRaises(ReflectorTypeError, SV.valid_reflector_type, machine_type, reflector_string)

    def test_valid_rotor_types_string(self):
        """
        Takes a rotor types string in the format "III II I" or "Beta,III,II,I".
        Can be space or comma seperated. Returns a rotor types dictionary with
        unique rotor types that are valid and compatible for its corresponding
        rotor position. If not valid raises RotorTypesStringError.
        """
        passing_tests = [
            [
                "WEHRMACHT_early",
                "iii,ii,i",
                {"RS":"III","RM":"II","RF":"I"}
            ],
            [
                "WEHRMACHT_late",
                "iv,v,ii",
                {"RS":"IV","RM":"V","RF":"II"}
            ],
            [
                "Kriegsmarine_M3",
                "iv v i",
                {"RS":"IV","RM":"V","RF":"I"}
            ],
            [
                "Kriegsmarine_M4",
                "beta iv v iii",
                {"R4":"Beta","RS":"IV","RM":"V","RF":"III"}
            ]
        ]

        failing_tests = [
            ["WEHRMACHT_early","iv,v,i"],
            ["WEHRMACHT_late","iiii,ii,i"],
            ["WEHRMACHT_late","iii,iii,i"]
            ["Kriegsmarine_M3","zeno,iii,ii,i"],
            ["Kriegsmarine_M4","i,gamma,ii,i"]
        ]

        for data in passing_tests:
            machine_type, rotor_types_string, output = data
            self.assertEqual(SV.valid_rotor_types_string(machine_type, rotor_types_string), output)
        
        for data in failing_tests:
            machine_type, rotor_types_string = data
            self.assertRaises(RotorTypesStringError, SV.valid_rotor_types_string, machine_type, rotor_types_string)

    def test_valid_rotor_settings_string(self):
        """
        Takes a rotor settings string in the format "AAA" or "A A A" or "01,01,01".
        Can be space or comma seperated. Returns a rotor settings dictionary with
        valid rotor settings for each rotor position required by the number of
        positions provided.
        """
        passing_tests = [
            ["ABC","L",3,{"RS":"A","RM":"B","RF":"C"}],
            ["a b c","L",None,{"RS":"A","RM":"B","RF":"C"}],
            ["a b","L",None,{"RM":"A","RF":"B"}],
            ["a","L",None,{"RF":"A"}],
            ["a,b,c,d","L",None,{"R4":"A","RS":"B","RM":"C","RF":"D"}],
            ["A,B,C","L",3,{"RS":"A","RM":"B","RF":"C"}],
            ["A,B,C,D","L",4,{"R4":"A","RS":"B","RM":"C","RF":"D"}],
            ["01 02 03","N",None,{"RS":"01","RM":"02","RF":"03"}],
            ["01,02,03","N",None,{"RS":"01","RM":"02","RF":"03"}],
            ["01,02,03,04","N",4,{"R4":"01","RS":"02","RM":"03","RF":"04"}],
            ["1 2 3","N",None,{"RS":"01","RM":"02","RF":"03"}]
        ]

        failing_tests = [
            ["a,b,1","L",None],
            ["01 02 03","L",None],
            ["A,B,C","L",4],
            ["01,02,C","N",None]
        ]

        for data in passing_tests:
            rotor_settings_string, charset_flag, positions, output = data
            self.assertEqual(SV.valid_rotor_settings_string(rotor_settings_string, charset_flag, positions), output)

        for data in failing_tests:
            rotor_settings_string, charset_flag, positions = data
            self.assertRaises(RotorSettingsStringError, SV.valid_rotor_settings_string, rotor_settings_string, charset_flag)

    def test_valid_ring_settings_string(self):
        """
        Takes a ring settings string in the form "AAA" or "A A A" or "01,01,01".
        Can be space or comma seperated. Returns a ring settings dictionary with
        valid ring settings for each rotor position required by the number of
        positions provided.
        """
        passing_tests = [
            ["ABC","L",3,{"RS":"A","RM":"B","RF":"C"}],
            ["a b c","L",None,{"RS":"A","RM":"B","RF":"C"}],
            ["a b","L",None,{"RM":"A","RF":"B"}],
            ["a","L",None,{"RF":"A"}],
            ["a,b,c,d","L",None,{"R4":"A","RS":"B","RM":"C","RF":"D"}],
            ["A,B,C","L",3,{"RS":"A","RM":"B","RF":"C"}],
            ["A,B,C,D","L",4,{"R4":"A","RS":"B","RM":"C","RF":"D"}],
            ["01 02 03","N",None,{"RS":"01","RM":"02","RF":"03"}],
            ["01,02,03","N",None,{"RS":"01","RM":"02","RF":"03"}],
            ["01,02,03,04","N",4,{"R4":"01","RS":"02","RM":"03","RF":"04"}],
            ["1 2 3","N",None,{"RS":"01","RM":"02","RF":"03"}]
        ]

        failing_tests = [
            ["a,b,1","L",None],
            ["01 02 03","L",None],
            ["A,B,C","L",4],
            ["01,02,C","N",None]
        ]

        for data in passing_tests:
            ring_settings_string, charset_flag, positions, output = data
            self.assertEqual(SV.valid_ring_settings_string(ring_settings_string, charset_flag, positions), output)

        for data in failing_tests:
            ring_settings_string, charset_flag, positions = data
            self.assertRaises(RingSettingsStringError, SV.valid_ring_settings_string, ring_settings_string, charset_flag)

    def test_valid_rotor_types_dict(self):
        """
        Takes a rotor types dict in format {"R4":"Beta","RS":"III","RM":"II","RF":"I"}.
        Returns a rotor types dictionary where the rotor types have been checked at each
        position in check_positions.
        """
        passing_tests = [
            [
                "WEHRMACHT_early",
                {"RS":"iii","RM":"ii","RF":"i"},
                None,
                {"RS":"III","RM":"II","RF":"I"}
            ],
            [
                "WEHRMACHT_late",
                {"RS":"v","RM":"iv","RF":"iii"},
                None,
                {"RS":"V","RM":"IV","RF":"III"}
            ],
            [
                "Kriegsmarine_M3",
                {"RS":"v","RM":"iv","RF":"iii"},
                ["rs","rm","rf"],
                {"RS":"V","RM":"IV","RF":"III"}
            ],
            [
                "Kriegsmarine_M4",
                {"R4":"beta","RS":"iv","RM":"v","RF":"iii"},
                ["R4","RS","RM","RF"],
                {"R4":"Beta","RS":"IV","RM":"V","RF":"III"}
            ],
            [
                "Kriegsmarine_M4",
                {"R4":"","RS":"iv","RM":"v","RF":"iii"},
                ["RS","RM","RF"],
                {"R4":"","RS":"IV","RM":"V","RF":"III"}
            ],
            [
                "Kriegsmarine_M4",
                {"RS":"iv","RM":"v","RF":"iii"},
                ["RS","RM","RF"],
                {"R4":"","RS":"IV","RM":"V","RF":"III"}
            ],
            [
                "Kriegsmarine_M4",
                {"R4":"Beta"},
                None,
                {"R4":"Beta","RS":"","RM":"","RF":""}
            ]
        ]

        failing_tests = [
            [
                "WEHRMACHT_early",
                {"RS":"III","RM":"II","RF":""},
                None
            ],
            [
                "WEHRMACHT_late",
                {"RS":"III","RM":"II","RF":""},
                ["RM","RF"]
            ],
            [
                "Kriegsmarine_M3",
                {"RX":"III","RM":"II","RF":"I"},
                ["RM","RF"]
            ],
            [
                "Kriegsmarine_M4",
                {"R4":"III","RS":"Beta","RM":"II","RF":"I"},
                ["R4","RS","RM","RF"]
            ]
        ]

        for data in passing_tests:
            machine_type, rotor_types_dict, check_positions, output = data
            self.assertEqual(SV.valid_rotor_types_dict(machine_type, rotor_types_dict, check_positions), output)

        for data in failing_tests:
            machine_type, rotor_types_dict, check_positions = data
            self.assertRaises(RotorTypesDictError, SV.valid_rotor_types_dict, machine_type, rotor_types_dict, check_positions)

    def test_valid_rotor_settings_dict(self):
        """
        Takes a rotor settings dict in format {"R4":"A","RS":"A","RM":"A","RF":"A"}.
        Returns a rotor settings dictionary where the rotor settings have been checked at
        each required position. If a machine type is provided then all the rotor positions
        in the rotor settings dict must conform with that machine type. If a machine type and
        check positions is provided then all rotor positions in the check positions must
        conform with that machine type. If not valid raises a RotorSettingsDictError.
        """
        passing_tests = [
            [
                {"RS":"A","RM":"B","RF":"C"},
                "L",
                "WEHRMACHT_early",
                None,
                {"RS":"A","RM":"B","RF":"C"}
            ],
            [
                {"RS":"","RM":"02","RF":"03"},
                "N",
                None,
                ["RM","RF"],
                {"RS":"","RM":"02","RF":"03"}
            ],
            [
                {"RS":"01","RM":"01","RF":"01"},
                "N",
                None,
                None,
                {"RS":"01","RM":"01","RF":"01"}
            ],
            [
                {"R4":"A","RS":"B","RM":"C","RF":"D"},
                "L",
                "Kriegsmarine_M4",
                ["R4","RS","RM","RF"],
                {"R4":"A","RS":"B","RM":"C","RF":"D"}
            ]
        ]

        failing_tests = [
            [
                {"RS":"01","RM":"A","RF":"A"},
                "L",
                None,
                None
            ],
            [
                {"RS":"","RM":"A","RF":"A"},
                "L",
                None,
                None
            ],
            [
                {"R4":"A","RS":"A","RM":"A","RF":"A"},
                "L",
                "Kriegsmarine_M3",
                None
            ],
            [
                {"RX":"A","RM":"A","RF":"A"},
                "L",
                None,
                None
            ]
        ]

        for data in passing_tests:
            settings_dict, charset_flag, machine_type, check_positions, output = data
            self.assertEqual(SV.valid_rotor_settings_dict(settings_dict, charset_flag, machine_type, check_positions), output)

        for data in failing_tests:
            settings_dict, charset_flag, machine_type, check_positions = data
            self.assertRaises(RotorSettingsDictError, SV.valid_rotor_settings_dict, settings_dict, charset_flag, machine_type, check_positions)

    def test_valid_ring_settings_dict(self):
        """
        Takes a ring settings dict in format {"R4":"A","RS":"A","RM":"A","RF":"A"}.
        Returns a ring settings dictionary where the ring settings have been checked at
        each required position. If a machine type is provided then all the rotor positions
        in the ring settings dict must conform with that machine type. If a machine type and
        check positions is provided then all rotor positions in the check positions must
        conform with that machine type. If not valid raises a RingSettingsDictError.
        """
        passing_tests = [
            [
                {"RS":"A","RM":"B","RF":"C"},
                "L",
                "WEHRMACHT_early",
                None,
                {"RS":"A","RM":"B","RF":"C"}
            ],
            [
                {"RS":"","RM":"02","RF":"03"},
                "N",
                None,
                ["RM","RF"],
                {"RS":"","RM":"02","RF":"03"}
            ],
            [
                {"RS":"01","RM":"01","RF":"01"},
                "N",
                None,
                None,
                {"RS":"01","RM":"01","RF":"01"}
            ],
            [
                {"R4":"A","RS":"B","RM":"C","RF":"D"},
                "L",
                "Kriegsmarine_M4",
                ["R4","RS","RM","RF"],
                {"R4":"A","RS":"B","RM":"C","RF":"D"}
            ]
        ]

        failing_tests = [
            [
                {"RS":"01","RM":"A","RF":"A"},
                "L",
                None,
                None
            ],
            [
                {"RS":"","RM":"A","RF":"A"},
                "L",
                None,
                None
            ],
            [
                {"R4":"A","RS":"A","RM":"A","RF":"A"},
                "L",
                "Kriegsmarine_M3",
                None
            ],
            [
                {"RX":"A","RM":"A","RF":"A"},
                "L",
                None,
                None
            ]
        ]

        for data in passing_tests:
            settings_dict, charset_flag, machine_type, check_positions, output = data
            self.assertEqual(SV.valid_ring_settings_dict(settings_dict, charset_flag, machine_type, check_positions), output)

        for data in failing_tests:
            settings_dict, charset_flag, machine_type, check_positions = data
            self.assertRaises(RingSettingsDictError, SV.valid_ring_settings_dict, settings_dict, charset_flag, machine_type, check_positions)

    def test_valid_ring_character(self):
        """
        Takes a ring character and checks that it is valid for the charset flag provided. If
        not valid raises a RingCharacterError.
        """
        passing_tests = [
            ["a","L","A"],
            ["A","L","A"],
            ["01","N","01"],
            ["1","N","01"]
        ]

        failing_tests = [
            ["01","L"],
            ["A","N"],
            ["#","L"],
            ["#","N"]
        ]

        for data in passing_tests:
            ring_character, charset_flag, output = data
            self.assertEqual(SV.valid_ring_character(ring_character, charset_flag), output)

        for data in failing_tests:
            ring_character, charset_flag = data
            self.assertRaises(RingCharacterError, SV.valid_ring_character, ring_character, charset_flag)

    def test_valid_permutation_string(self):
        """
        Takes a permutation string. Checks that the permutation string is valid and conforms
        the provided flags. If a machine type is provided will check that the permutation
        string conforms to that machine type. Returns a permutation dictionary if valid.
        If not valid raises a PermutationError.        
        """
        passing_tests = [
            [
                "A_UKW-A_III_II_I_G1",
                "WEHRMACHT_early",
                True,
                True,
                {
                    "RS":"A",
                    "REFLECTOR":"UKW-A",
                    "ROTOR_TYPES":{"RS":"III","RM":"II","RF":"I"},
                    "GROUP":"G1"
                }
            ],
            [
                "A_UKW-B_IV_V_I_G2",
                "WEHRMACHT_late",
                True,
                True,
                {
                    "RS":"A",
                    "REFLECTOR":"UKW-B",
                    "ROTOR_TYPES":{"RS":"","RM":"","RF":""},
                    "GROUP":"G2"
                }
            ],
            [
                "UKW-C_IV_V_I_G3",
                "WEHRMACHT_late",
                False,
                True,
                {
                    "RS":None,
                    "REFLECTOR":"UKW-C",
                    "ROTOR_TYPES":{"RS":"","RM":"","RF":""},
                    "GROUP":"G3"
                }
            ],
            [
                "B_UKW-C_IV_V_I",
                "WEHRMACHT_late",
                True,
                False,
                {
                    "RS":"B",
                    "REFLECTOR":"UKW-C",
                    "ROTOR_TYPES":{"RS":"","RM":"","RF":""},
                    "GROUP":None
                }
            ]
        ]

        failing_tests = [
            ["A_UKW-A_III_II_I_G1","WEHRMACHT_early",True,False],
            ["A_UKW-A_III_II_II_G1","WEHRMACHT_early",False,True],
            ["UKW-A_III_II_I",None,True,True],
            ["Z_UKW-C_IV_II_I_G3","WEHRMACHT_early",True,True]
        ]

        for data in passing_tests:
            permutation_string, machine_type, rs_flag, group_flag, output = data
            self.assertEqual(SV.valid_permutation_string(permutation_string, machine_type, rs_flag, group_flag), output)

        for data in failing_tests:
            permutation_string, machine_type, rs_flag, group_flag = data
            self.assertRaises(PermutationError, SV.valid_permutation_string(permutation_string, machine_type, rs_flag, group_flag))
