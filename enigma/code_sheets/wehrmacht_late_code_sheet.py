"""

SCF == L  PCF == L  PBM == S

| DAY | UKW |   ROTORS    | RING SETTINGS |      PLUGBOARD SETTINGS       |    KENGRUPPEN    |
|     |     | RS  RM  RF  |  RS  RM  RF   |                               |                  |
| 31  |  C  | III II  I   |  A   A   A    | AB CD EF GH IJ KL MN OP QR ST |  LDF HUX WNY SUR |

SCF == L  PCF == N  PBM == S

| DAY | UKW |   ROTORS    | RING SETTINGS |      PLUGBOARD SETTINGS       | KENGRUPPEN |
|     |     | RS  RM  RF  |  RS  RM  RF   |                               |            |
| 31  |  C  | III II  I   |  A   A   A    | 01/02 03/04 05/06 07/08 09/10 |  LDF  HUX  |
|     |     |             |               | 11/12 13/14 15/16 17/18 19/20 |  WNY  SUR  |

SCF == N  PCF == L  PBM == S

| DAY | UKW |   ROTORS    | RING SETTINGS |      PLUGBOARD SETTINGS       |     KENGRUPPEN      |
|     |     | RS  RM  RF  |  RS  RM  RF   |                               |                     |
| 31  |  C  | III II  I   |  01  01  01   | AB CD EF GH IJ KL MN OP QR ST |  01/02/03 04/05/06  |
|     |     |             |               |                               |  07/08/09 10/11/12  |

SCF == N  PCF == N  PBM == S

| DAY | UKW |   ROTORS    | RING SETTINGS |      PLUGBOARD SETTINGS       |     KENGRUPPEN      |
|     |     | RS  RM  RF  |  RS  RM  RF   |                               |                     |
| 31  |  C  | III II  I   |  01  01  01   | 01/02 03/04 05/06 07/08 09/10 |  01/02/03 04/05/06  |
|     |     |             |               | 11/12 13/14 15/16 17/18 19/20 |  07/08/09 10/11/12  |

SCF == L  PCF == L  PBM == u

| DAY | UKW |   ROTORS    | RING SETTINGS | UHR |           PLUGBOARD SETTINGS            | KENGRUPPEN |
|     |     | RS  RM  RF  |  RS  RM  RF   |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
|     |     |             |               |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
| 31  |  C  | III II  I   |  A   A   A    | 20  |  A   B   C   D   E   F   G   H   I   J  |  LDF HUX   |
|     |     |             |               |     |  K   L   M   N   O   P   Q   R   S   T  |  WNY SUR   |

SCF == L  PCF == N  PBM == U

| DAY | UKW |   ROTORS    | RING SETTINGS | UHR |           PLUGBOARD SETTINGS            | KENGRUPPEN |
|     |     | RS  RM  RF  |  RS  RM  RF   |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
|     |     |             |               |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
| 31  |  C  | III II  I   |  A   A   A    | 20  |  01  02  03  04  05  06  07  08  09  10 |  LDF HUX   |
|     |     |             |               |     |  11  12  13  14  15  16  17  18  19  20 |  WNY SUR   |

SCF == N  PCF == L  PBM == U

| DAY | UKW |   ROTORS    | RING SETTINGS | UHR |           PLUGBOARD SETTINGS            |     KENGRUPPEN      |
|     |     | RS  RM  RF  |  RS  RM  RF   |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                     |
|     |     |             |               |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                     |
| 31  |  C  | III II  I   |  01  01  01   | 20  |  A   B   C   D   E   F   G   H   I   J  |  01/02/03 04/05/06  |
|     |     |             |               |     |  K   L   M   N   O   P   Q   R   S   T  |  07/08/09 10/11/12  |

SCF == N  PCF == N  PBM == U

| DAY | UKW |   ROTORS    | RING SETTINGS | UHR |           PLUGBOARD SETTINGS            |     KENGRUPPEN      |
|     |     | RS  RM  RF  |  RS  RM  RF   |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                     |
|     |     |             |               |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                     |
| 31  |  C  | III II  I   |  01  01  01   | 20  |  01  02  03  04  05  06  07  08  09  10 |  01/02/03 04/05/06  |
|     |     |             |               |     |  11  12  13  14  15  16  17  18  19  20 |  07/08/09 10/11/12  |

Wheel order has to be non repeating for the entire month.
"""
from code_sheets.code_sheet import CodeSheet
from code_sheets.code_sheet_tools import CodeSheetTools


class WehrmachtLateCodeSheet(CodeSheet):

    def __init__(self, scrambler_char_flag, pb_char_flag, pb_mode, days):
        super().__init__("WEHRMACHT late",scrambler_char_flag, pb_char_flag, pb_mode, days, 3, True, 10)
        self._make_sheet_dict()
        self._make_key_sheet()

    def __str__(self):
        return self.sheet_string

    def sheet(self):

        return self.sheet_string
    
    def sheet_dict(self):

        return self._sheet_dict

    def _make_key_sheet(self):
        self._make_sheet_header()
        self._make_sheet_fields()

    def _make_sheet_header(self):

        if self.sc_char_flag == "L" and self.pb_char_flag == "L" and self.pb_mode == "S":
            self.args = {"h_lines":2,"f_lines":1,"pb_lines":1,"ken_lines":1}
        if self.sc_char_flag == "L" and self.pb_char_flag == "N" and self.pb_mode == "S":
            self.args = {"h_lines":2,"f_lines":2,"pb_lines":2,"ken_lines":2}
        if self.sc_char_flag == "N" and self.pb_char_flag == "L" and self.pb_mode == "S":
            self.args = {"h_lines":2,"f_lines":2,"pb_lines":1,"ken_lines":2}
        if self.sc_char_flag == "N" and self.pb_char_flag == "N" and self.pb_mode == "S":
            self.args = {"h_lines":2,"f_lines":2,"pb_lines":2,"ken_lines":2}
        if self.sc_char_flag == "L" and self.pb_char_flag == "L" and self.pb_mode == "U":
            self.args = {"h_lines":3,"f_lines":2,"pb_lines":2,"ken_lines":2}
        if self.sc_char_flag == "L" and self.pb_char_flag == "N" and self.pb_mode == "U":
            self.args = {"h_lines":3,"f_lines":2,"pb_lines":2,"ken_lines":2}
        if self.sc_char_flag == "N" and self.pb_char_flag == "L" and self.pb_mode == "U":
            self.args = {"h_lines":3,"f_lines":2,"pb_lines":2,"ken_lines":2}
        if self.sc_char_flag == "N" and self.pb_char_flag == "N" and self.pb_mode == "U":
            self.args = {"h_lines":3,"f_lines":2,"pb_lines":2,"ken_lines":2}

        days_header = CodeSheetTools.days_header(self.args["h_lines"])
        ref_header = CodeSheetTools.reflector_header(self.args["h_lines"],True)
        rotor_type_header = CodeSheetTools.rotor_types_header(3,self.args["h_lines"])
        ring_settings_header = CodeSheetTools.ring_settings_header(3,self.args["h_lines"])
        if self.pb_mode == "U":
            uhr_settings_header = CodeSheetTools.uhr_box_setting_header(self.args["h_lines"])
        pb_settings_header = CodeSheetTools.plugboard_settings_header(self.pb_char_flag,self.pb_mode,self.args["pb_lines"],10,self.args["h_lines"])
        kengruppen_header = CodeSheetTools.kengruppen_header(self.sc_char_flag,self.args["ken_lines"],self.args["h_lines"])

        self.sheet_string = ""

        for i in range(len(days_header)):
            self.sheet_string += "|"
            self.sheet_string += days_header[i]
            self.sheet_string += "|"
            self.sheet_string += ref_header[i]
            self.sheet_string += "|"
            self.sheet_string += rotor_type_header[i]
            self.sheet_string += "|"
            self.sheet_string += ring_settings_header[i]
            self.sheet_string += "|"
            if self.pb_mode == "U":
                self.sheet_string += uhr_settings_header[i]
                self.sheet_string += "|"
            self.sheet_string += pb_settings_header[i]
            self.sheet_string += "|"
            self.sheet_string += kengruppen_header[i]
            self.sheet_string += "|\n"

    def _make_sheet_fields(self):
        days_elems = self._make_days_elements()
        ref_elems = self._make_reflectors_elements()
        rotor_type_elems = self._make_rotor_types_elements()
        ring_settings_elems = self._make_ring_settings_elements()
        if self.pb_mode == "U":
            uhr_settings_elems = self._make_uhr_box_settings()
        pb_settings_elems = self._make_plugboard_settings_elements()
        kengruppen_elems = self._make_kengruppen_elements()

        for i in range(len(days_elems)):
            self.sheet_string += "|"
            self.sheet_string += days_elems[i]
            self.sheet_string += "|"
            self.sheet_string += ref_elems[i]
            self.sheet_string += "|"
            self.sheet_string += rotor_type_elems[i]
            self.sheet_string += "|"
            self.sheet_string += ring_settings_elems[i]
            if self.pb_mode == "U":
                self.sheet_string += "|"
                self.sheet_string += uhr_settings_elems[i]
            self.sheet_string += "|"
            self.sheet_string += pb_settings_elems[i]
            self.sheet_string += "|"
            self.sheet_string += kengruppen_elems[i]
            self.sheet_string += "|\n"

