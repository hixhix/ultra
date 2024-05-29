import unittest
from enigma_core.settings.settings import EQUIPMENT_DICT, LETTERS, NUMBERS
from enigma_core.validators.plugboard_validators import PlugboardValidators as PBV
from enigma_core.validators.plugboard_validators import (SteckerPBSettingsStringError,
                                                         UhrBoxPBSettingsStringError,
                                                         SteckerPBSettingsDictError,
                                                         UhrBoxPBSettingsDictError,
                                                         PBSocketIDError,
                                                         UhrBoxPlugIDError)


class TestPlugboardValidators(unittest.TestCase):

    def test_valid_stecker_pb_settings_string(self):

        passing_tests = [
            [
                "ab,cd,ef,gh,ij,kl,mn,op,qr,st", "L",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "A":"B","B":"A","C":"D","D":"C",
                        "E":"F","F":"E","G":"H","H":"G",
                        "I":"J","J":"I","K":"L","L":"K",
                        "M":"N","N":"M","O":"P","P":"O",
                        "Q":"R","R":"Q","S":"T","T":"S",
                        "U":"U","V":"V","W":"W","X":"X",
                        "Y":"Y","Z":"Z"
                    },
                   "PLUGBOARD_MODE":"S",
                   "PLUGBOARD_CHARSET_FLAG":"L"
                }
            ],
            [
                "AB CD EF GH IJ KL MN OP QR ST", "L",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "A":"B","B":"A","C":"D","D":"C",
                        "E":"F","F":"E","G":"H","H":"G",
                        "I":"J","J":"I","K":"L","L":"K",
                        "M":"N","N":"M","O":"P","P":"O",
                        "Q":"R","R":"Q","S":"T","T":"S",
                        "U":"U","V":"V","W":"W","X":"X",
                        "Y":"Y","Z":"Z"
                    },
                   "PLUGBOARD_MODE":"S",
                   "PLUGBOARD_CHARSET_FLAG":"L"    
                }
            ],
            [
                "ab cd,ef,gh ij kl mn;op qr st", "L",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "A":"B","B":"A","C":"D","D":"C",
                        "E":"F","F":"E","G":"H","H":"G",
                        "I":"J","J":"I","K":"L","L":"K",
                        "M":"N","N":"M","O":"P","P":"O",
                        "Q":"R","R":"Q","S":"T","T":"S",
                        "U":"U","V":"V","W":"W","X":"X",
                        "Y":"Y","Z":"Z"
                    },
                   "PLUGBOARD_MODE":"S",
                   "PLUGBOARD_CHARSET_FLAG":"L"    
                }
            ],
            [
                "1,2 3,4 5,6 7,8 9,10 11,12 13,14 15,16 17,18 19,20", "N",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01":"02","02":"01","03":"04","04":"03",
                        "05":"06","06":"05","07":"08","08":"07",
                        "09":"10","10":"09","11":"12","12":"11",
                        "13":"14","14":"13","15":"16","16":"15",
                        "17":"18","18":"17","19":"20","20":"19",
                        "21":"21","22":"22","23":"23","24":"24",
                        "25":"25","26":"26"
                    },
                   "PLUGBOARD_MODE":"S",
                   "PLUGBOARD_CHARSET_FLAG":"N"
                }
            ],
            [
                "01,02 03,04 05,06 07,08 09,10", "N",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01":"02","02":"01","03":"04","04":"03",
                        "05":"06","06":"05","07":"08","08":"07",
                        "09":"10","10":"09","11":"11","12":"12",
                        "13":"13","14":"14","15":"15","16":"16",
                        "17":"17","18":"18","19":"19","20":"20",
                        "21":"21","22":"22","23":"23","24":"24",
                        "25":"25","26":"26"
                    },
                   "PLUGBOARD_MODE":"S",
                   "PLUGBOARD_CHARSET_FLAG":"N"
                }
            ]
        ]

        failing_tests = [
            ["ABCD EF GH IJ KL MN OP QR ST", "L"], # no seperator
            ["AB CZ ZF GH IJ KL MN OP QR ST", "L"], # contradiction
            ["AB 1D EF GH IJ KL MN OP QR ST", "L"], # non alphabetic character
            ["0102 03,04 05,06 07,08 09,10", "N"], # missing seperator
            ["01,02 03,04 05,03 07,08 09,10", "N"] # contradiction
        ]

        for string_data in passing_tests:
            string, charset_flag, output = string_data
            self.assertEqual(PBV.valid_stecker_pb_settings_string(string, charset_flag), output)

        for string_data in failing_tests:
            string, charset_flag = string_data
            self.assertRaises(SteckerPBSettingsStringError, PBV.valid_stecker_pb_settings_string, string, charset_flag)

    def test_valid_uhr_box_pb_group_settings(self):

        passing_tests = [
            [
                "A B C D E F G H I J","L","A",None,
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01B":"A","02B":"B",
                        "03B":"C","04B":"D",
                        "05B":"E","06B":"F",
                        "07B":"G","08B":"H",
                        "09B":"I","10B":"J"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L",
                    "GROUP":"A"
                }
            ],
            [
                "ABCDEFGHIJK","L","A",None,
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01B":"A","02B":"B",
                        "03B":"C","04B":"D",
                        "05B":"E","06B":"F",
                        "07B":"G","08B":"H",
                        "09B":"I","10B":"J"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L",
                    "GROUP":"A"
                }
            ],
            [
                "1 2 3 4 5 6 7 8 9 10","N","A",None,
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"01","02A":"02",
                        "03A":"03","04A":"04",
                        "05A":"05","06A":"06",
                        "07A":"07","08A":"08",
                        "09A":"09","10A":"10"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"N",
                    "GROUP":"A"
                }
            ],
            [
                "01 02 03 04 05 06 07 08 09 10","N","A",None,
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"01","02A":"02",
                        "03A":"03","04A":"04",
                        "05A":"05","06A":"06",
                        "07A":"07","08A":"08",
                        "09A":"09","10A":"10"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"N",
                    "GROUP":"A"
                }
            ],
            [
                "K L M N O P Q R S T","L","B",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"A","02A":"B",
                        "03A":"C","04A":"D",
                        "05A":"E","06A":"F",
                        "07A":"G","08A":"H",
                        "09A":"I","10A":"J"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L",
                    "GROUP":"A"
                },
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01B":"K","02B":"L",
                        "03B":"M","04B":"N",
                        "05B":"O","06B":"P",
                        "07B":"Q","08B":"R",
                        "09B":"S","10B":"JT"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L",
                    "GROUP":"B"
                }
            ],
            [
                "11,12,13,14,15,16,17,18,19,20","N","B",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"11","02A":"12",
                        "03A":"13","04A":"14",
                        "05A":"15","06A":"16",
                        "07A":"17","08A":"18",
                        "09A":"19","10A":"20"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L",
                    "GROUP":"A"
                },
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01B":"11","02B":"12",
                        "03B":"13","04B":"14",
                        "05B":"15","06B":"16",
                        "07B":"17","08B":"18",
                        "09B":"19","10B":"20"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L",
                    "GROUP":"B"
                },
            ]
        ]

        failing_tests = [
            ["0102 03 04 05 06 07 08 09 10","N","A",None], # missing seperator
            ["01 02 03 04 05 06 07 08 09 10","L","A",None], # incorrect charset flag
            [
                "11 12 13 14 15 16 17 18 19 20","N","B",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"11","02A":"02",
                        "03A":"03","04A":"04",
                        "05A":"05","06A":"06",
                        "07A":"07","08A":"08",
                        "09A":"09","10A":"10"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L",
                    "GROUP":"B"
                }
            ], # contradiction
            ["1 B C D E F G H I J","L","A",None] # non alphabet character
        ]

        for string_data in passing_tests:
            string, charset_flag, group, previous, output = string_data
            self.assertEqual(PBV.valid_uhr_box_pb_group_settings(string, charset_flag, group, previous), output)

        for string_data in failing_tests:
            string, charset_flag, group, previous = string_data
            self.assertRaises(UhrBoxPBSettingsStringError, PBV.valid_uhr_box_pb_group_settings, string, charset_flag, group, previous)

    def test_valid_uhr_box_pb_settings(self):
        
        passing_tests = [
            [
                "A=[A B C D E F G H I J] B=[K L M N O P Q R S T]","L",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"A","02A":"B",
                        "03A":"C","04A":"D",
                        "05A":"E","06A":"F",
                        "07A":"G","08A":"H",
                        "09A":"I","10A":"J",
                        "01B":"K","02B":"L",
                        "03B":"M","04B":"N",
                        "05B":"O","06B":"P",
                        "07B":"Q","08B":"R",
                        "09B":"S","10B":"T"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                }
            ],
            [
                "A=[ABCDEFGHIJ] B=[KLMNOPQRST]","L",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"A","02A":"B",
                        "03A":"C","04A":"D",
                        "05A":"E","06A":"F",
                        "07A":"G","08A":"H",
                        "09A":"I","10A":"J",
                        "01B":"K","02B":"L",
                        "03B":"M","04B":"N",
                        "05B":"O","06B":"P",
                        "07B":"Q","08B":"R",
                        "09B":"S","10B":"T"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                }
            ],
            [
                "A=[1 2 3 4 5 6 7 8 9 10] B=[11 12 13 14 15 16 17 18 19 20]","N",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"01","02A":"02",
                        "03A":"03","04A":"04",
                        "05A":"05","06A":"06",
                        "07A":"07","08A":"08",
                        "09A":"09","10A":"10",
                        "01B":"11","02B":"12",
                        "03B":"13","04B":"14",
                        "05B":"15","06B":"16",
                        "07B":"17","08B":"18",
                        "09B":"19","10B":"20"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                }
            ],
            [
                "A=[01 02 03 04 05 06 07 08 09 10] B=[11 12 13 14 15 16 17 18 19 20]","N",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"01","02A":"02",
                        "03A":"03","04A":"04",
                        "05A":"05","06A":"06",
                        "07A":"07","08A":"08",
                        "09A":"09","10A":"10",
                        "01B":"11","02B":"12",
                        "03B":"13","04B":"14",
                        "05B":"15","06B":"16",
                        "07B":"17","08B":"18",
                        "09B":"19","10B":"20"
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                }
            ]
        ]

        failing_tests = [
            ["A=[01 02 03 04 05 06 07 08 09 10] B=[11 12 13 14 15 16 17 18 19 20]","L"], # incorrect charset flag
            ["A=[0102 03 04 05 06 07 08 09 10] B=[11 12 13 14 15 16 17 18 19 20]","N"], # missing seperator
            ["A=[01 02 03 04 05 06 07 08 09 10] B=[01 12 13 14 15 16 17 18 19 20]","N"], # contradiction
            ["A=[01 02 03 04 05 06 07 08 09 10] A=[11 12 13 14 15 16 17 18 19 20]","N"], # two group ids are same
            ["A=[01 02 03 04 05 06 07 08 09 10] C=[11 12 13 14 15 16 17 18 19 20]","N",] # incorrect group type
        ]

        for string_data in passing_tests:
            string, charset_flag, output = string_data
            self.assertEqual(PBV.valid_uhr_box_pb_settings(string, charset_flag), output)

        for string_data in failing_tests:
            string, charset_flag
            self.assertRaises(UhrBoxPBSettingsStringError, PBV.valid_uhr_box_pb_group_settings, string, charset_flag)

    def test_pb_valid_socket_id(self):
        passing_tests = [
            ["A","L","A"],
            ["a","L","A"],
            ["1","N","01"],
            ["01","N","01"]
        ]

        failing_tests = [
            ["A","N"],
            ["01","L"]
        ]

        for string_data in passing_tests:
            pb_socket_id, charset_flag, output = string_data
            self.assertEqual(PBV.valid_pb_socket_id(pb_socket_id, charset_flag), output)
        
        for string_data in failing_tests:
            pb_socket_id, charset_flag = string_data
            self.assertRaises(PBSocketIDError, PBV.valid_pb_socket_id, pb_socket_id, charset_flag)

    def test_valid_uhr_box_plug_id(self):
        passing_tests = [
            ["01A","01A"]
            ["01B","01B"]
            ["1A","01A"]
            ["1B","01B"]
            ["01a","01A"]
            ["01b","01B"]
            ["1a","01A"]
            ["1b","01B"]
        ]

        failing_tests = [
            "01C",
            "A",
            "B",
            "11A",
            "11B"
        ]

        for string_data in passing_tests:
            uhr_plug_id, output = string_data
            self.assertEqual(PBV.valid_uhr_box_plug_id(uhr_plug_id), output)

        for uhr_plug_id in failing_tests:
            self.assertRaises(UhrBoxPlugIDError, PBV.valid_uhr_box_plug_id, uhr_plug_id)

    def test_valid_stecker_pb_dict(self):
        passing_tests = [
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "A":"A","B":"B","C":"C","D":"D",
                        "E":"E","F":"F","G":"G","H":"H",
                        "I":"I","J":"J","K":"K","L":"L",
                        "M":"M","N":"N","O":"O","P":"P",
                        "Q":"Q","R":"R","S":"S","T":"T"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                },"L",None,
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "A":"A","B":"B","C":"C","D":"D",
                        "E":"E","F":"F","G":"G","H":"H",
                        "I":"I","J":"J","K":"K","L":"L",
                        "M":"M","N":"N","O":"O","P":"P",
                        "Q":"Q","R":"R","S":"S","T":"T",
                        "U":"U","V":"V","W":"W","X":"X",
                        "Y":"Y","Z":"Z"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                },"L",None,
            ],
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "a":"a","b":"b","c":"c","d":"d",
                        "e":"e","f":"f","g":"g","h":"h",
                        "i":"i","j":"j","k":"k","l":"l",
                        "m":"m","n":"n","o":"o","p":"p",
                        "q":"q","r":"r","s":"s","t":"t"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                },"L",None,
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "A":"A","B":"B","C":"C","D":"D",
                        "E":"E","F":"F","G":"G","H":"H",
                        "I":"I","J":"J","K":"K","L":"L",
                        "M":"M","N":"N","O":"O","P":"P",
                        "Q":"Q","R":"R","S":"S","T":"T",
                        "U":"U","V":"V","W":"W","X":"X",
                        "Y":"Y","Z":"Z"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                },"L",None,
            ],
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01":"01","02":"02","03":"03","04":"04",
                        "05":"05","06":"06","07":"07","08":"08",
                        "09":"09","10":"10","11":"11","12":"12",
                        "13":"13","14":"14","15":"15","16":"16",
                        "17":"17","18":"18","19":"19","20":"20"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                },"N",None,
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01":"01","02":"02","03":"03","04":"04",
                        "05":"05","06":"06","07":"07","08":"08",
                        "09":"09","10":"10","11":"11","12":"12",
                        "13":"13","14":"14","15":"15","16":"16",
                        "17":"17","18":"18","19":"19","20":"20",
                        "21":"21","22":"22","23":"23","24":"24",
                        "25":"25","26":"26"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                }
            ],
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "1":"1","2":"2","3":"3","4":"4",
                        "5":"5","6":"6","7":"7","8":"8",
                        "9":"9","10":"10","11":"11","12":"12",
                        "13":"13","14":"14","15":"15","16":"16",
                        "17":"17","18":"18","19":"19","20":"20"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                },"N",None,
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01":"01","02":"02","03":"03","04":"04",
                        "05":"05","06":"06","07":"07","08":"08",
                        "09":"09","10":"10","11":"11","12":"12",
                        "13":"13","14":"14","15":"15","16":"16",
                        "17":"17","18":"18","19":"19","20":"20",
                        "21":"21","22":"22","23":"23","24":"24",
                        "25":"25","26":"26"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                }
            ],
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "A":"B","B":"A","C":"D","D":"C",
                        "E":"F","F":"E","G":"H","H":"G",
                        "I":"J","J":"I","K":"L","L":"K",
                        "M":"N","N":"M","O":"P","P":"O",
                        "Q":"R","R":"Q","S":"T","T":"S"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                },"L",None,
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "A":"B","B":"A","C":"D","D":"C",
                        "E":"F","F":"E","G":"H","H":"G",
                        "I":"J","J":"I","K":"L","L":"K",
                        "M":"N","N":"M","O":"P","P":"O",
                        "Q":"R","R":"Q","S":"T","T":"S",
                        "U":"U","V":"V","W":"W","X":"X",
                        "Y":"Y","Z":"Z"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                }
            ],
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01":"02","02":"01","03":"04","04":"03",
                        "05":"06","06":"05","07":"08","08":"07",
                        "09":"10","10":"09","11":"12","12":"11",
                        "13":"14","14":"13","15":"16","16":"15",
                        "17":"18","18":"17","19":"20","20":"19"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                },"N",None,
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01":"02","02":"01","03":"04","04":"03",
                        "05":"06","06":"05","07":"08","08":"07",
                        "09":"10","10":"09","11":"12","12":"11",
                        "13":"14","14":"13","15":"16","16":"15",
                        "17":"18","18":"17","19":"20","20":"19",
                        "21":"21","22":"22","23":"23","24":"24",
                        "25":"25","26":"26"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                }
            ]
        ]

        failing_tests = [
            {
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01":"02","02":"02","03":"03","04":"04",
                        "05":"05","06":"06","07":"07","08":"08",
                        "09":"09","10":"10","11":"11","12":"12",
                        "13":"13","14":"14","15":"15","16":"16",
                        "17":"17","18":"18","19":"19","20":"20",
                        "21":"21","22":"22","23":"23","24":"24",
                        "25":"25","26":"26"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                },"N",None
            },
            {
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "A":"B","B":"B","C":"C","D":"D",
                        "E":"E","F":"F","G":"G","H":"H",
                        "I":"I","J":"J","K":"K","L":"L",
                        "M":"M","N":"N","O":"O","P":"P",
                        "Q":"Q","R":"R","S":"S","T":"T",
                        "U":"U","V":"V","W":"W","X":"X",
                        "Y":"Y","Z":"Z"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                },"L",None
            },
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "A":"A","B":"B","C":"C","D":"D",
                        "E":"E","F":"F","G":"G","H":"H",
                        "I":"I","J":"J","K":"K","L":"L",
                        "M":"M","N":"N","O":"O","P":"P",
                        "Q":"Q","R":"R","S":"S","T":"T",
                        "U":"U","V":"V","W":"W","X":"X",
                        "Y":"Y","Z":"Z"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                }
            ],
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01":"01","02":"02","03":"03","04":"04",
                        "05":"05","06":"06","07":"07","08":"08",
                        "09":"09","10":"10","11":"11","12":"12",
                        "13":"13","14":"14","15":"15","16":"16",
                        "17":"17","18":"18","19":"19","20":"20",
                        "21":"21","22":"22","23":"23","24":"24",
                        "25":"25","26":"26"
                    },
                    "PLUGBOARD_MODE":"S",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                }
            ]
        ]

        for data in passing_tests:
            settings_dict, charset_flag, positions, output_dict = data
            self.assertEqual(PBV.valid_stecker_pb_dict(settings_dict, charset_flag, positions), output_dict)
        
        for data in failing_tests:
            settings_dict, charset_flag, positions = data
            self.assertRaises(SteckerPBSettingsDictError, PBV.valid_stecker_pb_dict, settings_dict, charset_flag, positions)

    def test_valid_uhr_box_pb_dict(self):
        passing_tests = [
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "1a":"a","2a":"b",
                        "3a":"c","4a":"d",
                        "5a":"e","6a":"f",
                        "7a":"g","8a":"h",
                        "9a":"i","10a":"j",
                        "1b":"k","2b":"l",
                        "3b":"m","4b":"n",
                        "5b":"o","6b":"p",
                        "7b":"q","8b":"r",
                        "9b":"s","10b":"t",
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                },"L",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"A","02A":"B",
                        "03A":"C","04A":"D",
                        "05A":"E","06A":"F",
                        "07A":"G","08A":"H",
                        "09A":"I","10A":"J",
                        "01B":"K","02B":"L",
                        "03B":"M","04B":"N",
                        "05B":"O","06B":"P",
                        "07B":"Q","08B":"R",
                        "09B":"S","10B":"T",
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                }
            ],
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "1a":"1","2a":"2",
                        "3a":"3","4a":"4",
                        "5a":"5","6a":"6",
                        "7a":"7","8a":"8",
                        "9a":"9","10a":"10",
                        "1b":"11","2b":"12",
                        "3b":"13","4b":"14",
                        "5b":"15","6b":"16",
                        "7b":"17","8b":"18",
                        "9b":"19","10b":"20",
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                },"L",
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"01","02A":"02",
                        "03A":"03","04A":"04",
                        "05A":"05","06A":"06",
                        "07A":"07","08A":"08",
                        "09A":"09","10A":"10",
                        "01B":"11","02B":"12",
                        "03B":"13","04B":"14",
                        "05B":"15","06B":"16",
                        "07B":"17","08B":"18",
                        "09B":"19","10B":"20",
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                }
            ]
        ]

        failing_tests = [
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01C":"A","02A":"B",
                        "03A":"C","04A":"D",
                        "05A":"E","06A":"F",
                        "07A":"G","08A":"H",
                        "09A":"I","10A":"J",
                        "01B":"K","02B":"L",
                        "03B":"M","04B":"N",
                        "05B":"O","06B":"P",
                        "07B":"Q","08B":"R",
                        "09B":"S","10B":"T",
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                },
                "L"
            ],
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"1","02A":"B",
                        "03A":"C","04A":"D",
                        "05A":"E","06A":"F",
                        "07A":"G","08A":"H",
                        "09A":"I","10A":"J",
                        "01B":"K","02B":"L",
                        "03B":"M","04B":"N",
                        "05B":"O","06B":"P",
                        "07B":"Q","08B":"R",
                        "09B":"S","10B":"T",
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                },
                "L"
            ],
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"A","02A":"A",
                        "03A":"C","04A":"D",
                        "05A":"E","06A":"F",
                        "07A":"G","08A":"H",
                        "09A":"I","10A":"J",
                        "01B":"K","02B":"L",
                        "03B":"M","04B":"N",
                        "05B":"O","06B":"P",
                        "07B":"Q","08B":"R",
                        "09B":"S","10B":"T",
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"L"
                },
                "L"
            ],
            [
                {
                    "PLUGBOARD_CONNECTIONS":{
                        "01A":"A","02A":"02",
                        "03A":"03","04A":"04",
                        "05A":"05","06A":"06",
                        "07A":"07","08A":"08",
                        "09A":"09","10A":"10",
                        "01B":"11","02B":"12",
                        "03B":"13","04B":"14",
                        "05B":"15","06B":"16",
                        "07B":"17","08B":"18",
                        "09B":"19","10B":"20",
                    },
                    "PLUGBOARD_MODE":"U",
                    "PLUGBOARD_CHARSET_FLAG":"N"
                },
                "N"
            ]
        ]

        for data in passing_tests:
            settings_dict, charset_flag, output_dict = data
            self.assertEqual(PBV.valid_uhr_box_pb_dict(settings_dict, charset_flag), output_dict)
        
        for data in failing_tests:
            settings_dict, charset_flag = data
            self.assertRaises(UhrBoxPBSettingsDictError, PBV.valid_uhr_box_pb_dict, settings_dict, charset_flag)
