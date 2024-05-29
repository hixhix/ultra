from enigma_core.settings.settings import LETTERS, NUMBERS
from code_sheets.code_sheet_data import CodeSheetData
from code_sheets.code_sheet_tools import CodeSheetTools



class CodeSheet:

    def __init__(self, machine_type, sc_char_flag, pb_char_flag, pb_mode, days, rotor_positions, rotor_types_repeat, pb_pairs):
        self.machine_type = machine_type
        self.sheet_string = None
        self.sc_char_flag = sc_char_flag
        self.pb_char_flag = pb_char_flag
        self.pb_mode = pb_mode
        self.days = days
        self.rotor_positions = rotor_positions
        self.non_repeat = rotor_types_repeat
        self.pb_pairs = pb_pairs
        self.args = None
        self._sheet_dict = {}

    def __str__(self):
        return self.sheet_string
    
    def _make_sheet_dict(self):
        for i in range(self.days):
            day = i+1
            self._sheet_dict[day] = {
                "MACHINE_TYPE":self.machine_type,
                "SCRAMBLER_SETTINGS":{"SCRAMBLER_CHAR_FLAG":self.sc_char_flag},
                "PLUGBOARD_SETTINGS":{"PLUGBOARD_CHAR_FLAG":self.pb_char_flag,"PLUGBOARD_MODE":self.pb_mode}
            }

    def _make_msg_inds(self):
        msg_inds = CodeSheetData.msg_id_list(self.days)
        return CodeSheetTools.msg_id_field(msg_inds, self.args["f_lines"])

    def _make_days_elements(self):
        return CodeSheetTools.days_field(self.days, self.args["f_lines"])

    def _make_reflectors_elements(self):
        ref_list = CodeSheetData.reflector_types_list(self.machine_type,self.days)
        self._record_reflector_types(ref_list)
        return CodeSheetTools.reflector_field(ref_list,self.args["f_lines"],True)

    def _make_rotor_types_elements(self):
        rotor_type_list = CodeSheetData.rotor_types_list(self.machine_type,self.days,self.non_repeat)
        self._record_rotor_types(rotor_type_list)
        return CodeSheetTools.rotor_types_field(rotor_type_list,self.rotor_positions,self.args["f_lines"])

    def _make_ring_settings_elements(self):
        ring_settings_list = CodeSheetData.ring_settings_list(self.sc_char_flag,self.days,self.rotor_positions)
        self._record_ring_settings(ring_settings_list)
        return CodeSheetTools.ring_settings_field(ring_settings_list,self.rotor_positions,self.args["f_lines"])
    
    def _make_rotor_settings_elements(self):
        rotor_settings_list = CodeSheetData.rotor_settings_list(self.sc_char_flag,self.days,self.rotor_positions)
        self._record_rotor_settings(rotor_settings_list)
        return CodeSheetTools.rotor_settings_field(rotor_settings_list,self.rotor_positions,self.args["f_lines"])
    
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
            pb_connections_list = CodeSheetData.stecker_plugboard_connections(self.pb_char_flag,self.days,self.pb_pairs)
            self._record_stecker_pb_settings(pb_connections_list)
        elif self.pb_mode == "U":
            pb_connections_list = CodeSheetData.uhr_box_plugboard_connections(self.pb_char_flag,self.days)
            self._record_uhr_box_pb_settings(pb_connections_list)
        return CodeSheetTools.plugboard_settings_field(pb_connections_list,self.pb_char_flag,self.pb_mode,self.args["pb_lines"],self.args["f_lines"])

    def _make_kengruppen_elements(self):
        kengruppen_list = CodeSheetData.kengruppen_list(self.sc_char_flag,self.days)
        return CodeSheetTools.kengruppen_field(kengruppen_list,self.sc_char_flag,self.args["ken_lines"],self.args["f_lines"])
    
    def _make_bigram_table(self):
        bigram_data = CodeSheetData.bigram_dict(self.sc_char_flag)
        return CodeSheetTools.bigram_table(bigram_data, self.sc_char_flag)

    def _record_reflector_types(self, reflector_types_list):
        for i in range(self.days):
            day = self.days - i
            self._sheet_dict[day]["SCRAMBLER_SETTINGS"]["REFLECTOR_TYPE"] = reflector_types_list[i]

    def _record_reflector_wiring(self, reflector_wiring_list):
        dividers = self.dividers[self.days]
        
        converted_wire_lists = []

        for wire_list in reflector_wiring_list:
            wire_list = self._convert_reflector_wiring_list(wire_list)
            converted_wire_lists.append(wire_list)

        for i in range(0,dividers[0]):
            day = self.days - i
            self._sheet_dict[day]["SCRAMBLER_SETTINGS"]["REFLECTOR_WIRING"] = converted_wire_lists[0].copy()

        for i in range(dividers[0], dividers[1]):
            day = self.days - i
            self._sheet_dict[day]["SCRAMBLER_SETTINGS"]["REFLECTOR_WIRING"] = converted_wire_lists[1].copy()

        for i in range(dividers[1], self.days):
            day = self.days - i
            self._sheet_dict[day]["SCRAMBLER_SETTINGS"]["REFLECTOR_WIRING"] = converted_wire_lists[2].copy()

    def _record_rotor_types(self, rotor_types_list):
        for i in range(self.days):
            day = self.days - i
            self._sheet_dict[day]["SCRAMBLER_SETTINGS"]["ROTOR_TYPES"] = rotor_types_list[i]

    def _record_ring_settings(self, ring_settings_list):
        for i in range(self.days):
            day = self.days - i
            self._sheet_dict[day]["SCRAMBLER_SETTINGS"]["RING_SETTINGS"] = ring_settings_list[i]

    def _record_rotor_settings(self, rotor_settings_list):
        for i in range(self.days):
            day = self.days - i
            self._sheet_dict[day]["SCRAMBLER_SETTINGS"]["ROTOR_SETTINGS"] = rotor_settings_list[i]

    def _record_uhr_box_settings(self, uhr_settings_list):
        for i in range(self.days):
            day = self.days - i
            self._sheet_dict[day]["PLUGBOARD_SETTINGS"]["UHR_BOX_SETTING"] = uhr_settings_list[i]

    def _record_stecker_pb_settings(self, pb_connections_list):
        charset = LETTERS if self.pb_char_flag == "L" else NUMBERS
        for i in range(self.days):
            day = self.days - i
            conn_list = pb_connections_list[i]
            connections_dict = {c : c for c in charset}
            for pair in conn_list:
                c1, c2 = pair
                connections_dict[c1] = c2
                connections_dict[c2] = c1
            self._sheet_dict[day]["PLUGBOARD_SETTINGS"]["PLUGBOARD_CONNECTIONS"] = connections_dict

    def _record_uhr_box_pb_settings(self, pb_connections_list):
        plug_ids = [
            "01A","02A","03A","04A","05A",
            "06A","07A","08A","09A","10A",
            "01B","02B","03B","04B","05B",
            "06B","07B","08B","09B","10B"
        ]
        for i in range(self.days):
            day = self.days - i
            conn_list = pb_connections_list[i]
            connections_dict = {}
            for n in range(20):
                plug_id = plug_ids[n]
                conn = conn_list[n]
                connections_dict[plug_id] = conn
            self._sheet_dict[day]["PLUGBOARD_SETTINGS"]["PLUGBOARD_CONNECTIONS"] = connections_dict

    def _convert_reflector_wiring_list(self, reflector_wiring):
        charset = LETTERS if self.sc_char_flag == "L" else NUMBERS

        wire_list = [None for i in range(26)]

        for pair in reflector_wiring:
            c1, c2 = pair
            ind1 = charset.index(c1)
            ind2 = charset.index(c2)
            wire_list[ind1] = c2
            wire_list[ind2] = c1

        return wire_list
