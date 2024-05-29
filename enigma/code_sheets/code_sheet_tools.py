"""

FIELDS

Id field
Msg id
Days field
Reflector type field
Reflector wiring for dora
Rotor types field
Ring settings field
Rotor settings field
Uhr box setting field
Plugboard settings field
Kengruppen field
"""
from enigma_core.settings.settings import LETTERS, NUMBERS


class CodeSheetTools:

    def id_header(lines=1):
        header_elems = []

        for l in range(lines):
            if l == 0:
                header_elems.append(" ID  ")
            elif l > 0:
                header_elems.append("     ")

        return header_elems

    def id_field(id_list, lines=1):
        field_elems = []

        for id in id_list:
            for l in range(lines):
                if l == 0:
                    field_elems.append(f" {id} ")
                elif l > 0:
                    field_elems.append("     ")

        return field_elems

    def msg_id_header(lines=1):
        header_elems = []

        for l in range(lines):
            if l == 0:
                header_elems.append(" MSG ID ")
            elif l > 0:
                header_elems.append("        ")

        return header_elems

    def msg_id_field(msg_id_list, lines=1):
        field_elems = []

        for id in msg_id_list:
            for l in range(lines):
                if l == 0:
                    field_elems.append(f"  {id}   ")
                elif l > 0:
                    field_elems.append("        ")

        return field_elems

    def days_header(lines=1):
        header_elems = []

        for l in range(lines):
            if l == 0:
                header_elems.append(" DAY ")
            elif l > 0:
                header_elems.append("     ")

        return header_elems

    def days_field(days, lines=1):
        field_elems = []

        for d in range(days,0,-1):
            for l in range(lines):
                if l == 0:
                    day = f"{d}".rjust(2,"0")
                    field_elems.append(f" {day}".ljust(5," "))
                elif l > 0:
                    field_elems.append("     ")

        return field_elems

    def reflector_header(lines=1, abreviate=False):
        header_elems = []

        for l in range(lines):
            if l == 0 and abreviate == True:
                header_elems.append(" UKW ")
            elif l == 0 and abreviate == False:
                header_elems.append("  UKW  ")
            elif l > 0:
                header_elems.append("     ")
            elif l > 0 and abreviate == False:
                header_elems.append("       ")

        return header_elems

    def reflector_field(reflector_list, lines=1, abreviate=False):
        field_elems = []

        for d in range(len(reflector_list)):
            for l in range(lines):
                if l == 0:
                    reflector = reflector_list.pop()
                    if abreviate == True:
                        field_elems.append(f"  {reflector[-1]}  ")
                    elif abreviate == False:
                        field_elems.append(f" {reflector} ")

                if l > 0 and abreviate == True:
                    field_elems.append("     ")
                elif l > 0 and abreviate == False:
                    field_elems.append("       ")

        return field_elems

    def reflector_wiring_header(charset_flag, lines=1):
        """
        " REF WIRE "
        "  AB  CD  "

        "  REF WIRE   "
        " 01/02 03/04 " 
        """
        header_elems = []

        if charset_flag == "L":
            header_elems.append(" REF WIRE ")
        elif charset_flag == "N":
            header_elems.append("  REF WIRE   ")

        line_length = len(header_elems[0])

        l = lines - 1

        if l > 0:
            for i in range(l):
                header_elems.append(" "*line_length)

        return header_elems
    
    def reflector_wiring_field(reflector_wiring, charset_flag, lines, days=31):
        """
        28-31
        """
        field_elems = []

        line_length = 10 if charset_flag == "L" else 13

        wiring_elems_lists = []

        for i in range(3):
            wire_elems_list = []
            wire_list = reflector_wiring[i]
            for n in range(6):
                c1,c2 = wire_list.pop(0)
                c3,c4 = wire_list.pop(0)
                if charset_flag == "L":
                    wire_elems_list.append(f"  {c1}{c2}  {c3}{c4}  ")
                elif charset_flag == "N":
                    wire_elems_list.append(f" {c1}/{c2} {c3}/{c4} ")
            wiring_elems_lists.append(wire_elems_list)

        total_lines = days * lines

        remaining_lines = total_lines - 18

        padding_lines = remaining_lines // 6

        for i in range(6):
            if i == 0:
                remaining_lines -= padding_lines
                for n in range(padding_lines):
                    field_elems.append(" "*line_length)
                wire_elems = wiring_elems_lists.pop(0)
                for n in range(6):
                    field_elems.append(wire_elems[n])
            elif i == 1:
                remaining_lines -= padding_lines
                for n in range(padding_lines):
                    field_elems.append(" "*line_length)
            elif i == 2:
                remaining_lines -= padding_lines
                for n in range(padding_lines):
                    field_elems.append(" "*line_length)
                wire_elems = wiring_elems_lists.pop(0)
                for n in range(6):
                    field_elems.append(wire_elems[n])
            elif i == 3:
                remaining_lines -= padding_lines
                for n in range(padding_lines):
                    field_elems.append(" "*line_length)
            elif i == 4:
                remaining_lines -= padding_lines
                for n in range(padding_lines):
                    field_elems.append(" "*line_length)
            elif i == 5:
                wire_elems = wiring_elems_lists.pop(0)
                for n in range(6):
                    field_elems.append(wire_elems[n])
                for n in range(remaining_lines):
                    field_elems.append(" "*line_length)

        return field_elems

    def rotor_types_header(positions, lines=1):
        """
        " RS   RM   RF  "
        " III  III  III "

        " R4    RS    RM    RF  "
        " Gamma III   III   III " 
        """
        header_elems = []

        for l in range(lines):
            if l == 0 and positions == 3:
                header_elems.append("   ROTOR TYPES    ")
                header_elems.append(" RS    RM    RF   ")
            elif l == 0 and positions == 4:
                header_elems.append("      ROTOR TYPES         ")
                header_elems.append(" R4    RS     RM     RF   ")

            if l > 1 and positions == 3:
                header_elems.append("                  ")
            elif l > 1 and positions == 4:
                header_elems.append("                          ")

        return header_elems

    def rotor_types_field(rotor_types_list, positions, lines=1):
        """
        
        """
        field_elems = []

        for rotor_types in rotor_types_list:
            for l in range(lines):
                if l == 0:
                    rs = rotor_types["RS"].ljust(4," ")
                    rm = rotor_types["RM"].ljust(4," ")
                    rf = rotor_types["RF"].ljust(4," ")
                    if positions == 3:
                        field_elems.append(f" {rs}  {rm}  {rf} ")
                    elif positions == 4:
                        r4 = rotor_types["R4"].ljust(5," ")
                        field_elems.append(f" {r4} {rs}   {rm}   {rf} ")
                elif l > 0:
                    if positions == 3:
                        field_elems.append("                  ")
                    elif positions == 4:
                        field_elems.append("                          ")

        return field_elems

    def ring_settings_header(positions, lines=1):
        """
        " RING SETTINGS "
        " RS   RM   RF  "

        " RING SETTINGS  "
        " R4  RS  RM  RF "
        """
        header_elems = []

        for l in range(lines):
            if l == 0 and positions == 3:
                header_elems.append(" RING SETTINGS ")
                header_elems.append(" RS   RM   RF  ")
            elif l == 0 and positions == 4:
                header_elems.append(" RING SETTINGS  ")
                header_elems.append(" R4  RS  RM  RF ")

            if l > 1 and positions == 3:
                header_elems.append("               ")
            elif l > 1 and positions == 4:
                header_elems.append("                ")

        return header_elems

    def ring_settings_field(ring_settings_list, positions, lines=1):
        field_elems = []

        for ring_settings in ring_settings_list:
            for l in range(lines):
                if l == 0:
                    rs = ring_settings["RS"].rjust(2," ")
                    rm = ring_settings["RM"].rjust(2," ")
                    rf = ring_settings["RF"].rjust(2," ")
                    if positions == 3:
                        field_elems.append(f" {rs}   {rm}   {rf}  ")
                    elif positions == 4:
                        r4 = ring_settings["R4"].rjust(2," ")
                        field_elems.append(f" {r4}  {rs}  {rm}  {rf} ")

                if l > 0 and positions == 3:
                    field_elems.append("               ")
                elif l > 0 and positions == 4:
                    field_elems.append("                ")

        return field_elems

    def rotor_settings_header(positions, lines=1):
        """
        " ROTOR SETTINGS "
        "  RS   RM   RF  "

        " ROTOR SETTINGS  "
        " R4  RS  RM  RF  "
        """
        header_elems = []

        for l in range(lines):
            if l == 0 and positions == 3:
                header_elems.append(" ROTOR SETTINGS ")
                header_elems.append("  RS   RM   RF  ")
            elif l == 0 and positions == 4:
                header_elems.append(" ROTOR SETTINGS ")
                header_elems.append(" R4  RS  RM  RF ")

            if l > 1 and positions == 3:
                header_elems.append("                ")
            elif l > 1 and positions == 4:
                header_elems.append("                ")

        return header_elems

    def rotor_settings_field(rotor_settings_list, positions, lines=1):
        field_elems = []

        for rotor_settings in rotor_settings_list:
            for l in range(lines):
                if l == 0:
                    rs = rotor_settings["RS"].rjust(2," ")
                    rm = rotor_settings["RM"].rjust(2," ")
                    rf = rotor_settings["RF"].rjust(2," ")
                    if positions == 3:
                        field_elems.append(f"  {rs}   {rm}   {rf}  ")
                    elif positions == 4:
                        r4 = rotor_settings["R4"].rjust(2," ")
                        field_elems.append(f" {r4}  {rs}  {rm}  {rf} ")

                if l > 0 and positions == 3:
                    field_elems.append("                ")
                elif l > 0 and positions == 4:
                    field_elems.append("                ")

        return field_elems

    def uhr_box_setting_header(lines=1):
        header_elems = []

        for l in range(lines):
            if l == 0:
                header_elems.append(" UHR ")
            elif l > 0:
                header_elems.append("     ")

        return header_elems

    def uhr_box_setting_field(uhr_box_setting_list, lines=1):
        field_elems = []

        for setting in uhr_box_setting_list:
            for l in range(lines):
                if l == 0:
                    setting = f"{setting}".rjust(2,"0")
                    field_elems.append(f" {setting}".ljust(5," "))
                elif l > 0:
                    field_elems.append("     ")

        return field_elems

    def plugboard_settings_header(charset_flag, pb_mode, pb_lines=1, pairs=10, lines=1):
        """
        "      PLUGBOARD SETTINGS       "
        " AB CD EF GH IJ KL MN OP QR ST "

        " PLUGBOARD SETTINGS "
        " AB  CD  EF  GH  IJ "
        " KL  MN  OP  QR  ST "

        " PLUGBOARD SETTINGS "
        "     AB  CD  EF     "
        "     GH  IJ  KL     "

        " PLUGBOARD SETTINGS "
        " AB CD EF GH IJ KL  "

        "                     PLUGBOARD SETTINGS                      "
        " 01/02 03/04 05/06 07/08 09/10 11/12 13/14 15/16 17/18 19/20 "

        "      PLUGBOARD SETTINGS       "
        " 01/02 03/04 05/06 07/08 09/10 "
        " 11/12 13/14 15/16 17/18 19/20 "

        " PLUGBOARD SETTINGS "
        " 01/02 03/04 05/06  "
        " 07/08 09/10 11/12  "

        "         PLUGBOARD SETTINGS          "
        " 01/02 03/04 05/06 07/08 09/10 11/12 "

        "           PLUGBOARD SETTINGS            "
        " 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A "
        " 01B 02B 03B 04B 05B 06B 07B 08B 09B 10B "
        " "
        """
        header_elems = []

        if charset_flag == "L" and pb_mode == "S" and pb_lines == 1 and pairs == 10:
            header_elems.append("      PLUGBOARD SETTINGS       ")
        elif charset_flag == "L" and pb_mode == "S" and pb_lines == 1 and pairs == 6:
            header_elems.append(" PLUGBOARD SETTINGS ")
        elif charset_flag == "L" and pb_mode == "S" and pb_lines == 2 and pairs == 10:
            header_elems.append(" PLUGBOARD SETTINGS ")
        elif charset_flag == "L" and pb_mode == "S" and pb_lines == 2 and pairs == 6:
            header_elems.append(" PLUGBOARD SETTINGS ")
        elif charset_flag == "N" and pb_mode == "S" and pb_lines == 1 and pairs == 10:
            header_elems.append("                     PLUGBOARD SETTINGS                      ")
        elif charset_flag == "N" and pb_mode == "S" and pb_lines == 1 and pairs == 6:
            header_elems.append("          PLUGBOARD SETTINGS          ")
        elif charset_flag == "N" and pb_mode == "S" and pb_lines == 2 and pairs == 10:
            header_elems.append("      PLUGBOARD SETTINGS       ")
        elif charset_flag == "N" and pb_mode == "S" and pb_lines == 2 and pairs == 6:
            header_elems.append(" PLUGBOARD SETTINGS ")
        elif pb_mode == "U":
            header_elems.append("           PLUGBOARD SETTINGS             ")
            header_elems.append(" 01A 02A 03A 04A 05A 06A 07A 08A 09A 10A  ")
            header_elems.append(" 01B 02B 03B 04B 05B 06B 07B 08B 09B 10B  ")

        l = lines - len(header_elems)

        line_length = len(header_elems[0])

        if l > 0:
            for i in range(l):
                header_elems.append(" "*line_length)

        return header_elems

    def plugboard_settings_field(plugboard_connections_list, charset_flag, pb_mode, pb_lines=1, lines=1):

        field_elems = []

        pairs = None

        for plugboard_connections in plugboard_connections_list:
            if pb_mode == "S":
                pairs = len(plugboard_connections)
                if pairs not in [6,10]:
                    err_msg = f""
                    raise Exception(err_msg)
            if charset_flag == "L" and pb_mode == "S" and pb_lines == 1 and pairs == 10:
                conn_str = " "
                for pair in plugboard_connections:
                    c1, c2 = pair
                    conn_str += f"{c1}{c2} "
                field_elems.append(conn_str)
            elif charset_flag == "L" and pb_mode == "S" and pb_lines == 1 and pairs == 6:
                conn_str = " "
                for pair in plugboard_connections:
                    c1, c2 = pair
                    conn_str += f"{c1}{c2} "
                conn_str += " "
                field_elems.append(conn_str)
            elif charset_flag == "L" and pb_mode == "S" and pb_lines == 2 and pairs == 10:
                for i in range(2):
                    conn_str = " "
                    for n in range(5):
                        pair = plugboard_connections.pop()
                        c1, c2 = pair
                        conn_str += f"{c1}{c2} "
                    field_elems.append(conn_str)
            elif charset_flag == "L" and pb_mode == "S" and pb_lines == 2 and pairs == 6:
                for i in range(2):
                    conn_str = "     "
                    for n in range(3):
                        pair = plugboard_connections.pop()
                        c1, c2 = pair
                        conn_str += f"{c1}{c2}  "
                    conn_str += "   "
                    field_elems.append(conn_str)
            elif charset_flag == "N" and pb_mode == "S" and pb_lines == 1 and pairs == 10:
                conn_str = " "
                for pair in plugboard_connections:
                    c1, c2 = pair
                    conn_str += f"{c1}/{c2} "
                field_elems.append(conn_str)
            elif charset_flag == "N" and pb_mode == "S" and pb_lines == 1 and pairs == 6:
                conn_str = " "
                for pair in plugboard_connections:
                    c1, c2 = pair
                    conn_str += f"{c1}/{c2} "
                conn_str += " "
                field_elems.append(conn_str)
            elif charset_flag == "N" and pb_mode == "S" and pb_lines == 2 and pairs == 10:
                for i in range(2):
                    conn_str = " "
                    for n in range(5):
                        pair = plugboard_connections.pop()
                        c1, c2 = pair
                        conn_str += f"{c1}/{c2} "
                    field_elems.append(conn_str)
            elif charset_flag == "N" and pb_mode == "S" and pb_lines == 2 and pairs == 6:
                for i in range(2):
                    conn_str = " "
                    for n in range(3):
                        pair = plugboard_connections.pop()
                        c1, c2 = pair
                        conn_str += f"{c1}{c2}  "
                    conn_str += " "
                    field_elems.append(conn_str)
            elif pb_mode == "U":
                for i in range(2):
                    conn_str = "  "
                    for n in range(10):
                        c = plugboard_connections.pop(0)
                        c = c.ljust(2," ")
                        conn_str += f"{c}  "
                    field_elems.append(conn_str)

            l = lines - pb_lines
            
            line_length = len(field_elems[0])

            if l > 0:
                for i in range(l):
                    field_elems.append(" "*line_length)    

        return field_elems

    def kengruppen_header(charset_flag, group_lines, lines=1):
        """
        "   KENGRUPPEN    "
        " ABC ABC ABC ABC "

        " KENGRUPPEN "
        "  ABC  ABC  "

        "             KENGRUPPEN              "
        " 01/01/01 01/01/01 01/01/01 01/01/01 "

        "    KENGRUPPEN     "
        " 01/01/01 01/01/01 "
        """
        header_elems = []

        if charset_flag == "L" and group_lines == 1:
            header_elems.append("   KENGRUPPEN    ")
        elif charset_flag == "L" and group_lines == 2:
            header_elems.append(" KENGRUPPEN ")
        elif charset_flag == "N" and group_lines == 1:
            header_elems.append("             KENGRUPPEN              ")
        elif charset_flag == "N" and group_lines == 2:
            header_elems.append("    KENGRUPPEN     ")

        l = lines - len(header_elems)

        line_length = len(header_elems[0])

        if l > 0:
            for i in range(l):
                header_elems.append(" "*line_length)
        
        return header_elems

    def kengruppen_field(kengruppen_list, charset_flag, group_lines=1, lines=1):
        """
        "   KENGRUPPEN    "
        " ABC ABC ABC ABC "

        " KENGRUPPEN "
        "  ABC  ABC  "
        "  ABC  ABC  "

        "             KENGRUPPEN              "
        " 01/01/01 01/01/01 01/01/01 01/01/01 "

        "    KENGRUPPEN     "
        " 01/01/01 01/01/01 "
        " 01/01/01 01/01/01 "
        """
        field_elems = []

        for kengruppen in kengruppen_list:
            l = 0
            if charset_flag == "L" and group_lines == 1:
                group_str = " "
                for group in kengruppen:
                    group_str += f"{group} "
                field_elems.append(group_str)
                l += 1
            elif charset_flag == "L" and group_lines == 2:
                for i in range(2):
                    group_str = "  "
                    for n in range(2):
                        group = kengruppen.pop(0)
                        group_str += f"{group}  "
                    field_elems.append(group_str)
                l += 2
            elif charset_flag == "N" and group_lines == 1:
                group_str = " "
                for group in kengruppen:
                    group_str += f"{group} "
                field_elems.append(group_str)
                l += 1
            elif charset_flag == "N" and group_lines == 2:
                for i in range(2):
                    group_str = " "
                    for n in range(2):
                        group = kengruppen.pop(0)
                        group_str += f"{group} "
                    field_elems.append(group_str)
                l += 2
            
            line_length = len(field_elems[0])

            l = lines - l

            if l > 0:
                for i in range(l):
                    field_elems.append(" "*line_length)

        return field_elems
    
    def bigram_table(bigram_dict, charset_flag):
        bigram_table = ""

        charset = LETTERS if charset_flag == "L" else NUMBERS

        for y in range(26):
            bigram_table += ""
            for x in range(13):
                c1 = charset[x]
                c2 = charset[y]
                if charset_flag == "L":
                    p1 = f"{c1}{c2}"
                    p2 = bigram_dict[p1]
                elif charset_flag == "N":
                    p1 = f"{c1}/{c2}"
                    p2 = bigram_dict[p1]
                if charset_flag == "L":
                    if y == 0:
                        bigram_table += f" {p1} = {p2} "
                    else:
                        bigram_table += f"  {c2} = {p2} "
                else:
                    if y == 0:
                        bigram_table += f" {p1}={p2} "
                    else:
                        bigram_table += f"    {c2}={p2} "
            bigram_table += "\n"

        bigram_table += "\n"

        for y in range(26):
            bigram_table += ""
            for x in range(13,26,1):
                c1 = charset[x]
                c2 = charset[y]
                if charset_flag == "L":
                    p1 = f"{c1}{c2}"
                    p2 = bigram_dict[p1]
                elif charset_flag == "N":
                    p1 = f"{c1}/{c2}"
                    p2 = bigram_dict[p1]
                if charset_flag == "L":
                    if y == 0:
                        bigram_table += f" {p1} = {p2} "
                    else:
                        bigram_table += f"  {c2} = {p2} "
                else:
                    if y == 0:
                        bigram_table += f" {p1}={p2} "
                    else:
                        bigram_table += f"    {c2}={p2} "
            bigram_table += "\n"

        return bigram_table