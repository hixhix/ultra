"""

SCF == L  PCF == L  PBM == S  REF != D

| ID  | DAY | UKW |   ROTORS    | RING SETTINGS |      PLUGBOARD SETTINGS       |   KENGRUPPEN    |
|     |     |     | RS  RM  RF  |  RS  RM  RF   |                               |                 |
| TGA | 31  |  C  | III II  I   |  A   A   A    | AB CD EF GH IJ KL MN OP QR ST | LDF HUX WNY SUR |

SCF == L  PCF == N  PBM == S  REF != D

| ID  | DAY | UKW |   ROTORS    | RING SETTINGS |      PLUGBOARD SETTINGS       | KENGRUPPEN |
|     |     |     | RS  RM  RF  |  RS  RM  RF   |                               |            |
| TGA | 31  |  C  | III II  I   |  A   A   A    | 01/02 03/04 05/06 07/08 09/10 |  LDF  HUX  |
|     |     |     |             |               | 11/12 13/14 15/16 17/18 19/20 |  WNY  SUR  |

SCF == N  PCF == L  PBM == S  REF != D

| ID  | DAY | UKW |   ROTORS    | RING SETTINGS |      PLUGBOARD SETTINGS       |    KENGRUPPEN     |
|     |     |     | RS  RM  RF  |  RS  RM  RF   |                               |                   |
| TGA | 31  |  C  | III II  I   |  01  01  01   | AB CD EF GH IJ KL MN OP QR ST | 01/02/03 04/05/06 |
|     |     |     |             |               |                               | 07/08/09 10/11/12 |

SCF == N  PCF == N  PBM == S  REF != D

| ID  | DAY | UKW |   ROTORS    | RING SETTINGS |      PLUGBOARD SETTINGS       |    KENGRUPPEN     |
|     |     |     | RS  RM  RF  |  RS  RM  RF   |                               |                   |
| TGA | 31  |  C  | III II  I   |  01  01  01   | 01/02 03/04 05/06 07/08 09/10 | 01/02/03 04/05/06 |
|     |     |     |             |               | 11/12 13/14 15/16 17/18 19/20 | 07/08/09 10/11/12 |

SCF == L  PCF == L  PBM == u  REF != D

| ID  | DAY | UKW |   ROTORS    | RING SETTINGS | UHR |           PLUGBOARD SETTINGS            | KENGRUPPEN |
|     |     |     | RS  RM  RF  |  RS  RM  RF   |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
|     |     |     |             |               |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
| TGA | 31  |  C  | III II  I   |  A   A   A    | 20  |  A   B   C   D   E   F   G   H   I   J  |  LDF HUX   |
|     |     |     |             |               |     |  K   L   M   N   O   P   Q   R   S   T  |  WNY SUR   |

SCF == L  PCF == N  PBM == U  REF != D

| ID  | DAY | UKW |   ROTORS    | RING SETTINGS | UHR |           PLUGBOARD SETTINGS            | KENGRUPPEN |
|     |     |     | RS  RM  RF  |  RS  RM  RF   |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
|     |     |     |             |               |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
| TGA | 31  |  C  | III II  I   |  A   A   A    | 20  |  01  02  03  04  05  06  07  08  09  10 |  LDF HUX   |
|     |     |     |             |               |     |  11  12  13  14  15  16  17  18  19  20 |  WNY SUR   |

SCF == N  PCF == L  PBM == U  REF != D

| ID  | DAY | UKW |   ROTORS    | RING SETTINGS | UHR |           PLUGBOARD SETTINGS            |    KENGRUPPEN     |
|     |     |     | RS  RM  RF  |  RS  RM  RF   |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                   |
|     |     |     |             |               |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                   |
| TGA | 31  |  C  | III II  I   |  01  01  01   | 20  |  A   B   C   D   E   F   G   H   I   J  | 01/02/03 04/05/06 |
|     |     |     |             |               |     |  K   L   M   N   O   P   Q   R   S   T  | 07/08/09 10/11/12 |

SCF == N  PCF == N  PBM == U  REF != D

| ID  | DAY | UKW |   ROTORS    | RING SETTINGS | UHR |           PLUGBOARD SETTINGS            |    KENGRUPPEN     |
|     |     |     | RS  RM  RF  |  RS  RM  RF   |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                   |
|     |     |     |             |               |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                   |
| TGA | 31  |  C  | III II  I   |  01  01  01   | 20  |  01  02  03  04  05  06  07  08  09  10 | 01/02/03 04/05/06 |
|     |     |     |             |               |     |  11  12  13  14  15  16  17  18  19  20 | 07/08/09 10/11/12 |




SCF == L  PCF == L  PBM == S  REF == D

| DAY | UKW |   ROTORS    | RING SETTINGS | REF WIRE |      PLUGBOARD SETTINGS       |   KENGRUPPEN    |
|     |     | RS  RM  RF  |  RS  RM  RF   |          |                               |                 |
| 31  |  C  | III II  I   |  A   A   A    |  AB  CD  | AB CD EF GH IJ KL MN OP QR ST | LDF HUX WNY SUR |

SCF == L  PCF == N  PBM == S  REF == D

| DAY | UKW |   ROTORS    | RING SETTINGS | REF WIRE |      PLUGBOARD SETTINGS       | KENGRUPPEN |
|     |     | RS  RM  RF  |  RS  RM  RF   |          |                               |            |
| 31  |  C  | III II  I   |  A   A   A    |  AB  CD  | 01/02 03/04 05/06 07/08 09/10 |  LDF  HUX  |
|     |     |             |               |          | 11/12 13/14 15/16 17/18 19/20 |  WNY  SUR  |

SCF == N  PCF == L  PBM == S  REF == D

| DAY | UKW |   ROTORS    | RING SETTINGS | REF WIRE |      PLUGBOARD SETTINGS       |    KENGRUPPEN     |
|     |     | RS  RM  RF  |  RS  RM  RF   |          |                               |                   |
| 31  |  C  | III II  I   |  01  01  01   |  AB  CD  | AB CD EF GH IJ KL MN OP QR ST | 01/02/03 04/05/06 |
|     |     |             |               |          |                               | 07/08/09 10/11/12 |

SCF == N  PCF == N  PBM == S  REF == D

| DAY | UKW |   ROTORS    | RING SETTINGS | REF WIRE |      PLUGBOARD SETTINGS       |    KENGRUPPEN     |
|     |     | RS  RM  RF  |  RS  RM  RF   |          |                               |                   |
| 31  |  C  | III II  I   |  01  01  01   |  AB  CD  | 01/02 03/04 05/06 07/08 09/10 | 01/02/03 04/05/06 |
|     |     |             |               |          | 11/12 13/14 15/16 17/18 19/20 | 07/08/09 10/11/12 |

SCF == L  PCF == L  PBM == u  REF == D

| DAY | UKW |   ROTORS    | RING SETTINGS | REF WIRE | UHR |           PLUGBOARD SETTINGS            | KENGRUPPEN |
|     |     | RS  RM  RF  |  RS  RM  RF   |          |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
|     |     |             |               |          |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
| 31  |  C  | III II  I   |  A   A   A    |  AB  CD  | 20  |  A   B   C   D   E   F   G   H   I   J  |  LDF HUX   |
|     |     |             |               |          |     |  K   L   M   N   O   P   Q   R   S   T  |  WNY SUR   |

SCF == L  PCF == N  PBM == U  REF == D

| DAY | UKW |   ROTORS    | RING SETTINGS | REF WIRE | UHR |           PLUGBOARD SETTINGS            | KENGRUPPEN |
|     |     | RS  RM  RF  |  RS  RM  RF   |          |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
|     |     |             |               |          |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |            |
| 31  |  C  | III II  I   |  A   A   A    |  AB  CD  | 20  |  01  02  03  04  05  06  07  08  09  10 |  LDF HUX   |
|     |     |             |               |          |     |  11  12  13  14  15  16  17  18  19  20 |  WNY SUR   |

SCF == N  PCF == L  PBM == U  REF == D

| DAY | UKW |   ROTORS    | RING SETTINGS | REF WIRE | UHR |           PLUGBOARD SETTINGS            |    KENGRUPPEN     |
|     |     | RS  RM  RF  |  RS  RM  RF   |          |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                   |
|     |     |             |               |          |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                   |
| 31  |  C  | III II  I   |  01  01  01   |  AB  CD  | 20  |  A   B   C   D   E   F   G   H   I   J  | 01/02/03 04/05/06 |
|     |     |             |               |          |     |  K   L   M   N   O   P   Q   R   S   T  | 07/08/09 10/11/12 |

SCF == N  PCF == N  PBM == U  REF == D

| DAY | UKW |   ROTORS    | RING SETTINGS | REF WIRE | UHR |           PLUGBOARD SETTINGS            |    KENGRUPPEN     |
|     |     | RS  RM  RF  |  RS  RM  RF   |          |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                   |
|     |     |             |               |          |     | 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A |                   |
| 31  |  C  | III II  I   |  01  01  01   |  AB  CD  | 20  |  01  02  03  04  05  06  07  08  09  10 | 01/02/03 04/05/06 |
|     |     |             |               |          |     |  11  12  13  14  15  16  17  18  19  20 | 07/08/09 10/11/12 |

Consecutive steckers are not allowed in luftwaffe key sheets.
The same rotor type can not be used in the same position on two consecutive days.
At least one new rotor type must be introduced each day.
"""
from code_sheets.code_sheet import CodeSheet
from enigma_core.settings.settings import LETTERS, NUMBERS
from code_sheets.code_sheet_data import CodeSheetData
from code_sheets.code_sheet_tools import CodeSheetTools
from pprint import pprint


class LuftwaffeCodeSheet(CodeSheet):

    def __init__(self, scrambler_char_flag, pb_char_flag, pb_mode, days, dora_flag=False):
        super().__init__("LUFTWAFFE",scrambler_char_flag, pb_char_flag, pb_mode, days, 3, True, 10)
        self.dora = dora_flag
        self.dividers = {28:[8,16],29:[8,16],30:[10,20],31:[10,20]}
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
        dora_settings_header = CodeSheetTools.reflector_wiring_header(self.sc_char_flag,self.args["h_lines"])
        if self.pb_mode == "U":
            uhr_settings_header = CodeSheetTools.uhr_box_setting_header(self.args["h_lines"])
        pb_settings_header = CodeSheetTools.plugboard_settings_header(self.pb_char_flag,self.pb_mode,self.args["pb_lines"],10,self.args["h_lines"])
        kengruppen_header = CodeSheetTools.kengruppen_header(self.sc_char_flag,self.args["ken_lines"],self.args["h_lines"])

        self.sheet_string = ""

        for i in range(len(days_header)):
            self.sheet_string += "|"
            self.sheet_string += days_header[i]
            self.sheet_string += "|"
            if self.dora == False:
                self.sheet_string += ref_header[i]
                self.sheet_string += "|"
            self.sheet_string += rotor_type_header[i]
            self.sheet_string += "|"
            self.sheet_string += ring_settings_header[i]
            if self.dora == True:
                self.sheet_string += "|"
                self.sheet_string += dora_settings_header[i]
            self.sheet_string += "|"
            if self.pb_mode == "U":
                self.sheet_string += uhr_settings_header[i]
                self.sheet_string += "|"
            self.sheet_string += pb_settings_header[i]
            self.sheet_string += "|"
            self.sheet_string += kengruppen_header[i]
            self.sheet_string += "|\n"

    def _make_sheet_fields(self):
        self.days_elems = self._make_days_elements()
        self.ref_elems = self._make_reflectors_elements()
        self.rotor_type_elems = self._make_rotor_types_elements()
        self.ring_settings_elems = self._make_ring_settings_elements()
        self.dora_settings_elems = self._make_reflector_wiring_elems()
        if self.pb_mode == "U":
            self.uhr_settings_elems = self._make_uhr_box_settings()
        self.pb_settings_elems = self._make_plugboard_settings_elements()
        self.kengruppen_elems = self._make_kengruppen_elements()

        for i in range(len(self.days_elems)):
            if self.dora == True:
                self._insert_divider(i)
            self.sheet_string += "|"
            self.sheet_string += self.days_elems[i]
            if self.dora == False:
                self.sheet_string += "|"
                self.sheet_string += self.ref_elems[i]
            self.sheet_string += "|"
            self.sheet_string += self.rotor_type_elems[i]
            self.sheet_string += "|"
            self.sheet_string += self.ring_settings_elems[i]
            if self.dora == True:
                self.sheet_string += "|"
                self.sheet_string += self.dora_settings_elems[i]
            if self.pb_mode == "U":
                self.sheet_string += "|"
                self.sheet_string += self.uhr_settings_elems[i]
            self.sheet_string += "|"
            self.sheet_string += self.pb_settings_elems[i]
            self.sheet_string += "|"
            self.sheet_string += self.kengruppen_elems[i]
            self.sheet_string += "|\n"

    def _make_days_elements(self):
        return CodeSheetTools.days_field(self.days, self.args["f_lines"])

    def _make_reflectors_elements(self):
        if not self.dora:
            ref_list = CodeSheetData.reflector_types_list("LUFTWAFFE",self.days)
        elif self.dora:
            ref_list = ["UKW-D" for i in range(self.days)]
        self._record_reflector_types(ref_list)
        return CodeSheetTools.reflector_field(ref_list,self.args["f_lines"],True)

    def _make_rotor_types_elements(self):
        rotor_type_list = CodeSheetData.rotor_types_list("LUFTWAFFE",self.days,True)
        self._record_rotor_types(rotor_type_list)
        return CodeSheetTools.rotor_types_field(rotor_type_list,3,self.args["f_lines"])

    def _make_ring_settings_elements(self):
        ring_settings_list = CodeSheetData.ring_settings_list(self.sc_char_flag,self.days,3)
        self._record_ring_settings(ring_settings_list)
        return CodeSheetTools.ring_settings_field(ring_settings_list,3,self.args["f_lines"])
    
    def _make_reflector_wiring_elems(self):
        reflector_wiring = CodeSheetData.reflector_wiring_list(self.sc_char_flag)
        self._record_reflector_wiring(reflector_wiring)
        return CodeSheetTools.reflector_wiring_field(reflector_wiring, self.sc_char_flag, self.args["f_lines"] ,self.days)
    
    def _make_uhr_box_settings(self):
        uhr_settings_list = CodeSheetData.uhr_settings_list(self.days)
        self._record_uhr_box_settings(uhr_settings_list)
        return CodeSheetTools.uhr_box_setting_field(uhr_settings_list, self.args["f_lines"])

    def _make_plugboard_settings_elements(self):
        if self.pb_mode == "S":
            pb_connections_list = CodeSheetData.stecker_plugboard_connections(self.pb_char_flag,self.days,10)
            self._record_stecker_pb_settings(pb_connections_list)
        elif self.pb_mode == "U":
            pb_connections_list = CodeSheetData.uhr_box_plugboard_connections(self.pb_char_flag,self.days)
            self._record_uhr_box_pb_settings(pb_connections_list)
        return CodeSheetTools.plugboard_settings_field(pb_connections_list,self.pb_char_flag,self.pb_mode,self.args["pb_lines"],self.args["f_lines"])

    def _make_kengruppen_elements(self):
        kengruppen_list = CodeSheetData.kengruppen_list(self.sc_char_flag,self.days)
        return CodeSheetTools.kengruppen_field(kengruppen_list,self.sc_char_flag,self.args["ken_lines"],self.args["f_lines"])

    def _insert_divider(self, line_number):
        days_list = self.dividers[self.days]

        if (line_number // self.args["f_lines"] in days_list) and (line_number % self.args["f_lines"] == 0):
            self.sheet_string += "|"
            self.sheet_string += "-" * len(self.days_elems[0])
            self.sheet_string += "|"
            self.sheet_string += "-" * len(self.rotor_type_elems[0])
            self.sheet_string += "|"
            self.sheet_string += "-" * len(self.ring_settings_elems[0])
            self.sheet_string += "|"
            self.sheet_string += "-" * len(self.dora_settings_elems[0])
            if self.pb_mode == "U":
                self.sheet_string += "|"
                self.sheet_string +=  "-" * len(self.uhr_settings_elems[0])
            self.sheet_string += "|"
            self.sheet_string += "-" * len(self.pb_settings_elems[0])
            self.sheet_string += "|"
            self.sheet_string += "-" * len(self.kengruppen_elems[0])
            self.sheet_string += "|\n"
