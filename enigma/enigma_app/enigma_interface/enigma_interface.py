from enigma_app.formatting.formatting import EnigmaFormatter as ef
from enigma_app.scrambler_interface.scrambler_interface import ScramblerInterface
from enigma_app.plugboard_interface.stecker_interface import SteckerPlugboardInterface
from enigma_app.plugboard_interface.uhr_box_interface import UhrBoxPlugboardInterface
from enigma_core.plugboard.stecker_plugboard import SteckerPlugboard
from enigma_core.plugboard.uhr_box_plugboard import UhrBoxPlugboard
from enigma_tools.histogram.histogram import Histogram
from code_sheets.wehrmacht_early_code_sheet import WehrmachtEarlyCodeSheet
from code_sheets.wehrmacht_late_code_sheet import WehrmachtLateCodeSheet
from code_sheets.kriegsmarine_m3_code_sheet import KriegsmarineM3CodeSheet
from code_sheets.kriegsmarine_m4_code_sheet import KriegsmarineM4CodeSheet
from code_sheets.luftwaffe_code_sheet import LuftwaffeCodeSheet
from enigma_app.telex.telex import Telex
from enigma_app.clear_terminal.clear_terminal import clear_terminal
import json
import os


class EnigmaInterface:

    def __init__(self, enigma_obj):
        """

        """
        self._enigma_obj = enigma_obj
        self._char_set_flag = 'L'
        self._code_sheet = None
        # init scrambler interface.
        self._scrambler = ScramblerInterface(enigma_obj.machine_type, enigma_obj.scrambler)
        # init plugboard interface.
        if isinstance(enigma_obj.plugboard, SteckerPlugboard):
            self._plugboard = SteckerPlugboardInterface(enigma_obj.plugboard)
        elif isinstance(enigma_obj.plugboard, UhrBoxPlugboard):
            self._plugboard = UhrBoxPlugboardInterface(enigma_obj.plugboard)

    def menu(self):
        """

        """
        menu_str = (
            f"Enter a number to select an option.\n"
            f"1. Character set menu.\n"
            f"2. Scrambler menu.\n"
            f"3. Plugboard menu.\n"
            f"4. Show setup procedure.\n"
            f"5. Code sheet setup.\n"
            f"6. Display machine.\n"
            f"7. User input.\n"
            f"8. Recieve message.\n"
            f"9. Transmit message.\n"
            f"10. Load/save settings.\n"
            f"11 Return to machine menu.\n"
        )

        while True:
            inpt = input(menu_str)
            if inpt == "1":
                clear_terminal()
                self._character_set_menu()
            elif inpt == "2":
                clear_terminal()
                self._scrambler.menu()
            elif inpt == "3":
                clear_terminal()
                self._plugboard_menu()
            elif inpt == "4":
                clear_terminal()
                self._show_procedure()
            elif inpt == "5":
                clear_terminal()
                self._code_sheet_setup()
            elif inpt == "6":
                clear_terminal()
                self._display_machine()
            elif inpt == "7":
                clear_terminal()
                self._enigma_input()
            elif inpt == "8":
                clear_terminal()
                self._recieve_message()
            elif inpt == "9":
                clear_terminal()
                self._transmit_message()
            elif inpt == '10':
                clear_terminal()
                self._load_save_settings()
            elif inpt == "11":
                clear_terminal()
                break
            else:
                print("Invalid input!. Try again.")

    def _plugboard_menu(self):
        """

        """
        menu_str = (
            f"Enter a number to select an option.\n"
            f"1. Select plugboard mode.\n"
            f"2. Plugboard setup.\n"
            f"3. Return to previous menu.\n"
        )

        while True:
            clear_terminal()
            inpt = input(menu_str)
            if inpt == "1": self._select_plugboard_mode()
            elif inpt == "2": self._plugboard.menu()
            elif inpt == "3":
                clear_terminal()
                break
            else:
                print("Invalid input!. Try again.")

    def _select_plugboard_mode(self):
        """

        """
        menu_str = (
            f"Enter a number to select an option.\n"
            f"1. Stecker plugboard.\n"
            f"2. Uhr box plugboard.\n"
            f"3. Return to previous menu.\n"
        )

        while True:
            clear_terminal()
            inpt = input(menu_str)
            if inpt == "1":
                self._enigma_obj.set_plugboard_mode('S', self._char_set_flag)
                self._plugboard = SteckerPlugboardInterface(self._enigma_obj.plugboard)
                break
            elif inpt == "2":
                self._enigma_obj.set_plugboard_mode('U', self._char_set_flag)
                self._plugboard = UhrBoxPlugboardInterface(self._enigma_obj.plugboard)
                break
            elif inpt == "3":
                break
            else:
                print("Invalid input!. Try again.")

    def _code_sheet_setup(self):
        # machine type determines sheet
        # use current scrambler and plugboard charset flags
        # use current plugboard mode
        # if reflector UKW-D available prompt for UKW-D or standard reflectors
        # generate sheet object
        # get sheet dict
        # prompt user to select day
        # set machine settings to that days settings
        # once code sheet is generated retain that code sheet
        sc_char_flag = self._enigma_obj.scrambler.character_set_flag
        pb_char_flag = self._enigma_obj.plugboard.character_set_flag
        pb_mode = self._plugboard_mode()

        if self._enigma_obj.machine_type == "LUFTWAFFE":
            if self._code_sheet:
                if self._code_sheet.sc_char_flag != sc_char_flag or self._code_sheet.pb_char_flag != pb_char_flag or self._code_sheet.pb_mode != pb_mode:
                    self._make_code_sheet()

            menu_str = (f"Enter a number to select the reflector mode.\n"
                        f"1. Standard reflector mode.\n"
                        f"2. Rewireable reflector UKW-D.\n")

            while True:
                clear_terminal()
                inpt = input(menu_str)

                if inpt == "1":
                    self._make_code_sheet(dora_flag=False)
                    clear_terminal()
                    break
                elif inpt == "2":
                    self._make_code_sheet(dora_flag=True)
                    clear_terminal()
                    break
                else:
                    print("Invalid input!. Try again.")

        elif self._code_sheet:
            if self._code_sheet.sc_char_flag != sc_char_flag or self._code_sheet.pb_char_flag != pb_char_flag or self._code_sheet.pb_mode != pb_mode:
                self._make_code_sheet()
        elif not self._code_sheet:
            self._make_code_sheet()

        menu_str = "Enter the day to set the machine settings to or q to quit.\n"

        loop = False

        while True:
            clear_terminal()
            print(self._code_sheet)

            if loop:
                print("Invalid input!. Try again.")
            loop = True

            inpt = input(menu_str)

            if inpt.upper() == "Q":
                clear_terminal()
                break

            try:
                inpt = int(inpt)
            except ValueError:
                print("Invalid input!. Try again.")
            else:
                if inpt in self._code_sheet.sheet_dict().keys():
                    settings = self._code_sheet.sheet_dict()[inpt]
                    self._enigma_obj.clear_enigma()
                    self._enigma_obj.settings = settings
                    clear_terminal()
                    break

    def _show_procedure(self):
        """

        """
        if self._enigma_obj.machine_type == "WEHRMACHT early":
            procedure_fname = "wehrmacht_early.txt"
        elif self._enigma_obj.machine_type == "WEHRMACHT late":
            procedure_fname = "wehrmacht_late.txt"
        elif self._enigma_obj.machine_type == "Kriegsmarine M3":
            procedure_fname = "kriegsmarine_m3.txt"
        elif self._enigma_obj.machine_type == "Kriegsmarine M4":
            procedure_fname = "kriegsmarine_m4.txt"
        elif self._enigma_obj.machine_type == "LUFTWAFFE":
            procedure_fname = "luftwaffe.txt"

        dir = os.path.dirname(__file__)
        dir = os.path.dirname(dir)
        dir = os.path.dirname(dir)
        dir = os.path.join(dir, "enigma_procedures")
        fpath = os.path.join(dir, procedure_fname)

        with open(fpath, "r") as f:
            procedure = f.read()

        while True:
            print(procedure)

            input("\nPress enter to exit.")
            clear_terminal()
            break

    def _make_code_sheet(self, dora_flag=False):
        """

        """
        sc_char_flag = self._enigma_obj.scrambler.character_set_flag
        pb_char_flag = self._enigma_obj.plugboard.character_set_flag
        pb_mode = self._plugboard_mode()
        days = 31

        if self._enigma_obj.machine_type == "WEHRMACHT early":
            self._code_sheet = WehrmachtEarlyCodeSheet(sc_char_flag, pb_char_flag, pb_mode, days)
        elif self._enigma_obj.machine_type == "WEHRMACHT late":
            self._code_sheet = WehrmachtLateCodeSheet(sc_char_flag, pb_char_flag, pb_mode, days)
        elif self._enigma_obj.machine_type == "Kriegsmarine M3":
            self._code_sheet = KriegsmarineM3CodeSheet(sc_char_flag, pb_char_flag, pb_mode, days)
        elif self._enigma_obj.machine_type == "Kriegsmarine M4":
            self._code_sheet = KriegsmarineM4CodeSheet(sc_char_flag, pb_char_flag, pb_mode, days)
        elif self._enigma_obj.machine_type == "LUFTWAFFE":
            self._code_sheet = LuftwaffeCodeSheet(sc_char_flag, pb_char_flag, pb_mode, 31, dora_flag)

    def _character_set_menu(self):
        """

        """
        menu_str1 = (
            f"Enter a numer to select an option.\n"
            f"1. Change scrambler character set.\n"
            f"2. Change plugboard character set.\n"
            f"3. Return to previous menu.\n"
        )

        menu_str2 = (
            f"Enter a number to select an option.\n"
            f"1. Character set A-Z.\n"
            f"2. Character set 01-26.\n"
            f"3. Return to previous menu.\n"
        )

        while True:
           clear_terminal()
           inpt = input(menu_str1)
           if inpt == "1":
                while True:
                    clear_terminal()
                    inpt = input(menu_str2)
                    if inpt == "1":
                        self._char_set_flag = 'L'
                        self._scrambler.character_set_flag('L')
                        print("Enigma machine character set is set to alpha.")
                        clear_terminal()
                        break
                    elif inpt == "2":
                        self._char_set_flag = 'N'
                        self._scrambler.character_set_flag('N')
                        print("Enigma machine character set is set to numerical.")
                        clear_terminal()
                        break
                    elif inpt == "3":
                        clear_terminal()
                        break
                    else:
                        print("Invalid input!. Try again.")
           elif inpt == "2":
                while True:
                    clear_terminal()
                    inpt = input(menu_str2)
                    if inpt == "1":
                        self._char_set_flag = 'L'
                        self._plugboard.character_set_flag('L')
                        print("Enigma machine character set is set to alpha.")
                        clear_terminal()
                        break
                    elif inpt == "2":
                        self._char_set_flag = 'N'
                        self._plugboard.character_set_flag('N')
                        print("Enigma machine character set is set to numerical.")
                        clear_terminal()
                        break
                    elif inpt == "3":
                        clear_terminal()
                        break
                    else:
                        print("Invalid input!. Try again.")
           elif inpt == "3":
               clear_terminal()
               break
           else:
               print("Invalid input!. Try again.")

    def _display_machine(self) -> None:
        """

        """
        print(self._enigma_obj.scrambler.collection)
        print(ef.line("SCRAMBLER"))
        print(f"\n{self._scrambler}\n")
        print(ef.line("PLUGBOARD"))
        print(f"\n{self._plugboard}\n")
        print(ef.line())

    def _enigma_input(self):
        """

        """
        if not self._enigma_obj.valid_enigma():
            clear_terminal()
            print("Enigma setup is not complete. "
                  "Cannot accept input until setup is complete.")
        else:
            inpt = self._get_user_input()
            if inpt:
                outp = self._convert_input(inpt)
                print(outp)

    def _get_user_input(self):
        """

        """
        clear_terminal()
        menu_str = (f"Enter a number to select an option.\n"
                    f"1. User input from terminal.\n"
                    f"2. user input from text file.\n"
                    f"3. Return to previous menu.\n")

        input_text = None

        while True:
            inpt = input(menu_str)

            if inpt == "1":
                input_text = self._get_terminal_input()
                break
            elif inpt == "2":
                input_text = self._get_text_file_input()
                break
            elif inpt == "3":
                break
            else:
                print("Invalid input!. Try again.")

        clear_terminal()
        return input_text

    def _get_terminal_input(self):
        """

        """
        clear_terminal()
        inpt = input("Enter text to be converted.\n")

        return inpt.upper()

    def _get_text_file_input(self):
        """

        """
        clear_terminal()

        while True:
            fpath = input("Enter the input text file name.\n")

            if not os.path.isfile(fpath):
                print(f"{fpath} is not a valid file name.")
                break
            else:
                with open(fpath, "r") as f:
                    text = f.read()
                return text.upper()

    def _recieve_message(self):
        """

        """
        # check enigma object is valid.
        # prompt for ip address.
        # prompt for a port number.
        # listen for message.
        # decrypt message.
        if not self._enigma_obj.valid_enigma():
            clear_terminal()
            print("Enigma setup is not complete. "
                  "Cannot accept input until setup is complete.")
        else:
            ip_address = Telex.get_ip_address()
            port_number = Telex.get_port_number()
            clear_terminal()
            print(f"Recieving on IP address {ip_address} port number {port_number}.")
            message = Telex.recieve(ip_address, port_number)
            message = self._convert_input(message)
            print(message)

    def _transmit_message(self):
        """

        """
        # check enigma is valid.
        # prompt for ip address.
        # prompt for port number.
        # prompt for input.
        # encrypt input.
        # transmit input.
        if not self._enigma_obj.valid_enigma():
            clear_terminal()
            print("Enigma setup is not complete. "
                  "Cannot accept input until setup is complete.")
        else:
            ip_address = Telex.get_ip_address()
            port_number = Telex.get_port_number()
            clear_terminal()
            print(f"Transmit on IP address {ip_address} port number {port_number}.")
            message = self._get_user_input()
            message = self._encrypt_input(message)
            Telex.transmit(message, ip_address, port_number)

    def _load_save_settings(self):
        """

        """
        menu_str = (
            f"Enter a number to select an option.\n"
            f"1. Save settings.\n"
            f"2. Load settings.\n"
            f"3. Return to previous menu.\n"
        )

        while True:
            clear_terminal()
            inpt = input(menu_str)

            if inpt == '1':
                if self._enigma_obj.valid_enigma():
                    settings = self._enigma_obj.settings
                    machine_type = self._enigma_obj.machine_type
                    settings["machine_type"] = machine_type
                    dirpath = os.path.dirname(__file__)
                    fpath = os.path.join(dirpath, "machine_settings.json")

                    with open(fpath, "w+") as f:
                        json.dump(settings, f)

                    print("Settings have been saved.")
                else:
                    print("The machine setup is not complete")
                break
            elif inpt == '2':
                dirpath = os.path.dirname(__file__)
                fpath = os.path.join(dirpath, "machine_settings.json")

                if os.path.isfile(fpath):
                    with open(fpath, "r") as f:
                        settings = json.load(f)

                    if settings["machine_type"] == self._enigma_obj.machine_type:
                        self._enigma_obj.scrambler.clear_scrambler()
                        self._enigma_obj.plugboard.clear()
                        self._enigma_obj.settings = settings
                        print("Settings have been loaded.")
                    else:
                        print("There are no saved settings for this enigma machine.")
                else:
                    print("There are no saved settings for this enigma machine.")
                break
            elif inpt == '3':
                break
            else:
                print("Invalid input!. Try again.")

    def _encrypt_input(self, inpt):
        """

        """
        clean_inpt = self._enigma_obj.keyboard.clean_input_string(inpt)
        outp = ""
        for char in clean_inpt:
            outp += self._enigma_obj.character_input(char)
        return outp

    def _convert_input(self, inpt: str) -> None:
        """

        """
        clean_inpt = self._enigma_obj.keyboard.clean_input_string(inpt)
        outp = ""
        for char in clean_inpt:
            outp += self._enigma_obj.character_input(char)
        hist = Histogram(clean_inpt, outp).__str__()
        _str = ef.line("HISTOGRAM")
        _str += '\n'
        _str += ef.center(hist)
        _str += '\n'
        _str += ef.line()
        _str += '\n'
        _str += ef.line("INPUT TEXT")
        _str += '\n\n'
        _str += ef.wrap_string(inpt, 6)
        _str += '\n\n'
        _str += ef.line()
        _str += '\n'
        _str += ef.line("CLEANED INPUT TEXT")
        _str += '\n\n'
        _str += ef.group_string(clean_inpt, 4)
        _str += '\n\n'
        _str += ef.line()
        _str += '\n'
        _str += ef.line("OUTPUT TEXT")
        _str += '\n\n'
        _str += ef.group_string(outp, 4)
        _str += '\n\n'
        _str += ef.line()
        return _str

    def _plugboard_mode(self):
        if isinstance(self._enigma_obj.plugboard, SteckerPlugboard):
            return "S"
        elif isinstance(self._enigma_obj.plugboard, UhrBoxPlugboard):
            return "U"
