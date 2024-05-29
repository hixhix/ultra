"""

| MSG IND | DAY |                           PLUGBOARD                         |    ROTOR SETTINGS    |
|   MPV   | 31  | 01/02 03/04 05/06 07/08 09/10 11/12 13/14 15/16 17/18 19/20 |    E   N   T   W     |

| MSG IND | DAY | UKW |    ROTOR TYPES    | RING SETTINGS |
|   MPV   | 31  |  B  | Beta III II_ I__  |  A  C  X  O   |

 AA => BS    BA => PV    CA => JC
  B => HH     B => PD     B => LO


SCF == L  PCF == L  PBM == S

| MSG IND | DAY |   ROTOR TYPES    | RING SETTINGS | ROTOR SETTINGS |      PLUGBOARD SETTINGS       |
|   MPV   | 31  | Beta III II  I   |  A  B  C  D   | A   B   C   D  | AB CD EF GH IJ KL MN OP QR ST |  

SCF == L  PCF == N  PBM == S

| MSG IND | DAY |   ROTOR TYPES    | RING SETTINGS | ROTOR SETTINGS |      PLUGBOARD SETTINGS       |
|   MPV   | 31  | Beta III II  I   |  A  B  C  D   | A   B   C   D  | 01/02 03/04 05/06 07/08 09/10 |
|         |     |                  |               |                | 11/12 13/14 15/16 17/18 19/20 |

SCF == N  PCF == L  PBM == S

| MSG IND | DAY |   ROTOR TYPES    | RING SETTINGS | ROTOR SETTINGS |      PLUGBOARD SETTINGS       |
|   MPV   | 31  | Beta III II  I   |  01 01 01 01  | 01  01  01  01 | AB CD EF GH IJ KL MN OP QR ST |

SCF == N  PCF == N  PBM == S

| MSG IND | DAY |   ROTOR TYPES    | RING SETTINGS | ROTOR SETTINGS |      PLUGBOARD SETTINGS       |
|   MPV   | 31  | Beta III II  I   |  01 01 01 01  | 01  01  01  01 | 01/02 03/04 05/06 07/08 09/10 |
|         |     |                  |               |                | 11/12 13/14 15/16 17/18 19/20 |

SCF == L  PCF == L  PBM == u

| MSG IND | DAY |   ROTOR TYPES    | RING SETTINGS | ROTOR SETTINGS |           PLUGBOARD SETTINGS            |
|         |     |                  |               |                | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |
|         |     |                  |               |                | 01B 02B 03B 04B 05B 06B 07B 08B 09B 10B |
|   MPV   | 31  | Beta III II  I   |  A  B  C  D   | A   B   C   D  |  A   B   C   D   E   F   G   H   I   J  |
|         |     |                  |               |                |  K   L   M   N   O   P   Q   R   S   T  |

SCF == L  PCF == N  PBM == U

| MSG IND | DAY |   ROTOR TYPES    | RING SETTINGS | ROTOR SETTINGS |           PLUGBOARD SETTINGS            |
|         |     |                  |               |                | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |
|         |     |                  |               |                | 01B 02B 03B 04B 05B 06B 07B 08B 09B 10B |
|   MPV   | 31  | Beta III II  I   |  A  B  C  D   | A   B   C   D  | 01  02  03  04  05  06  07  08  09  10  |
|         |     |                  |               |                | 11  12  13  14  15  16  17  18  19  20  |

SCF == N  PCF == L  PBM == U

| MSG IND | DAY |   ROTOR TYPES    | RING SETTINGS | ROTOR SETTINGS |           PLUGBOARD SETTINGS            |
|         |     |                  |               |                | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |
|         |     |                  |               |                | 01B 02B 03B 04B 05B 06B 07B 08B 09B 10B |
|   MPV   | 31  | Beta III II  I   |  01 01 01 01  | 01  01  01  01 |  A   B   C   D   E   F   G   H   I   J  |
|         |     |                  |               |                |  K   L   M   N   O   P   Q   R   S   T  |

SCF == N  PCF == N  PBM == U

| MSG IND | DAY |   ROTOR TYPES    | RING SETTINGS | ROTOR SETTINGS |           PLUGBOARD SETTINGS            |
|         |     |                  |               |                | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |
|         |     |                  |               |                | 01B 02B 03B 04B 05B 06B 07B 08B 09B 10B |
|   MPV   | 31  | Beta III II  I   |  01 01 01 01  | 01  01  01  01 | 01  02  03  04  05  06  07  08  09  10  |
|         |     |                  |               |                | 11  12  13  14  15  16  17  18  19  20  |
"""
from code_sheets.code_sheet import CodeSheet
from code_sheets.code_sheet_tools import CodeSheetTools


class KriegsmarineM4CodeSheet(CodeSheet):

    def __init__(self, scrambler_char_flag, pb_char_flag, pb_mode, days):
        super().__init__("Kriegsmarine M4",scrambler_char_flag, pb_char_flag, pb_mode, days, 4, True, 10)
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
            self.args = {"h_lines":2,"f_lines":1,"pb_lines":1}
        if self.sc_char_flag == "L" and self.pb_char_flag == "N" and self.pb_mode == "S":
            self.args = {"h_lines":2,"f_lines":2,"pb_lines":2}
        if self.sc_char_flag == "N" and self.pb_char_flag == "L" and self.pb_mode == "S":
            self.args = {"h_lines":2,"f_lines":1,"pb_lines":1}
        if self.sc_char_flag == "N" and self.pb_char_flag == "N" and self.pb_mode == "S":
            self.args = {"h_lines":2,"f_lines":2,"pb_lines":2}
        if self.sc_char_flag == "L" and self.pb_char_flag == "L" and self.pb_mode == "U":
            self.args = {"h_lines":3,"f_lines":2,"pb_lines":2}
        if self.sc_char_flag == "L" and self.pb_char_flag == "N" and self.pb_mode == "U":
            self.args = {"h_lines":3,"f_lines":2,"pb_lines":2}
        if self.sc_char_flag == "N" and self.pb_char_flag == "L" and self.pb_mode == "U":
            self.args = {"h_lines":3,"f_lines":2,"pb_lines":2}
        if self.sc_char_flag == "N" and self.pb_char_flag == "N" and self.pb_mode == "U":
            self.args = {"h_lines":3,"f_lines":2,"pb_lines":2}

        ind_header = CodeSheetTools.msg_id_header(self.args["h_lines"])
        days_header = CodeSheetTools.days_header(self.args["h_lines"])
        ref_header = CodeSheetTools.reflector_header(self.args["h_lines"],True)
        rotor_type_header = CodeSheetTools.rotor_types_header(4,self.args["h_lines"])
        ring_settings_header = CodeSheetTools.ring_settings_header(4,self.args["h_lines"])
        rotor_settings_header = CodeSheetTools.rotor_settings_header(4,self.args["h_lines"])
        if self.pb_mode == "U":
            uhr_settings_header = CodeSheetTools.uhr_box_setting_header(self.args["h_lines"])
        pb_settings_header = CodeSheetTools.plugboard_settings_header(self.pb_char_flag,self.pb_mode,self.args["pb_lines"],self.pb_pairs,self.args["h_lines"])

        self.sheet_string = ""

        for i in range(len(days_header)):
            self.sheet_string += "|"
            self.sheet_string += ind_header[i]
            self.sheet_string += "|"
            self.sheet_string += days_header[i]
            self.sheet_string += "|"
            self.sheet_string += ref_header[i]
            self.sheet_string += "|"
            self.sheet_string += rotor_type_header[i]
            self.sheet_string += "|"
            self.sheet_string += ring_settings_header[i]
            self.sheet_string += "|"
            self.sheet_string += rotor_settings_header[i]
            self.sheet_string += "|"
            if self.pb_mode == "U":
                self.sheet_string += uhr_settings_header[i]
                self.sheet_string += "|"
            self.sheet_string += pb_settings_header[i]
            self.sheet_string += "|\n"
    
    def _make_sheet_fields(self):
        msg_inds = self._make_msg_inds()
        days = self._make_days_elements()
        reflectors = self._make_reflectors_elements()
        rotor_types = self._make_rotor_types_elements()
        ring_settings = self._make_ring_settings_elements()
        rotor_settings = self._make_rotor_settings_elements()
        if self.pb_mode == "U":
            uhr_settings = self._make_uhr_box_settings()
        pb_settings = self._make_plugboard_settings_elements()
        bigram_table = self._make_bigram_table()

        for i in range(len(days)):
            self.sheet_string += "|"
            self.sheet_string += msg_inds[i]
            self.sheet_string += "|"
            self.sheet_string += days[i]
            self.sheet_string += "|"
            self.sheet_string += reflectors[i]
            self.sheet_string += "|"
            self.sheet_string += rotor_types[i]
            self.sheet_string += "|"
            self.sheet_string += ring_settings[i]
            self.sheet_string += "|"
            self.sheet_string += rotor_settings[i]
            self.sheet_string += "|"
            if self.pb_mode == "U":
                self.sheet_string += uhr_settings[i]
                self.sheet_string += "|"
            self.sheet_string += pb_settings[i]
            self.sheet_string += "|\n"
        self.sheet_string += "\n"
        self.sheet_string += bigram_table
