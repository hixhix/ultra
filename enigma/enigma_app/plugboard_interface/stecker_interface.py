from enigma_app.formatting.formatting import EnigmaFormatter as ef
from enigma_core.validators.plugboard_validators.plugboard_validators import *
from enigma_app.clear_terminal.clear_terminal import clear_terminal


class SteckerPlugboardInterface:

    def __init__(self, plugboard_obj):
        """
        
        """
        self._plugboard_obj = plugboard_obj

    def __str__(self):
        """
        
        """
        return ef.center(self._plugboard_obj.__str__())

    def menu(self):
        """
        
        """
        
        while True:
            clear_terminal()
            menu_str = (
                f"{ef.line('STECKER PLUGBOARD')}\n"
                f"\n{self.__str__()}\n\n"
                f"Enter a number to select an option\n"
                f"1. Clear plugboard\n"
                f"2. Connect stecker cables\n"
                f"3. Return to previous menu\n"
                f"{ef.line()}\n"
            )

            inpt = input(menu_str)
            if inpt == "1": self._clear_plugboard()
            elif inpt == "2": self._connect_stecker_cables()
            elif inpt == "3":
                clear_terminal()
                return
            else: print("Invalid input! Try agin")

    def character_set_flag(self, flag):
        """
        
        """
        self._plugboard_obj.character_set_flag = flag

    def _clear_plugboard(self):
        """
        
        """
        menu_str = f"Are you sure you want to clear the plugboard Y/N. "

        inpt = input(menu_str)

        if inpt.upper() == 'Y':
            self._plugboard_obj.clear()
            clear_terminal()
            print("The plugboard has been cleared.")

    def _connect_stecker_cables(self):
        """
        
        """
        def get_connections_str():
            """
            Prompt user to input socket id pairs to connect. Returns the socket
            id string.            
            """
            if charset_flag == "L":
                menu_str = (
                    f"Enter up to 13 space seperated plugboard pairs.\n"
                    f"01 02 03 04 05 06 07 08 09 10 11 12 13\n")
            elif charset_flag == "N":
                menu_str = (
                    f"Enter up to 13 space seperated plug pairs. \n"
                    f"The socket ids in each plug pair being seperated by '-'.\n"
                    f"-001- -002- -003- -004- -005- -006- -007- -008- -009- -010- -011- -012- -013-\n")
            inpt = input(menu_str)

            return inpt
        
        charset_flag = self._plugboard_obj.character_set_flag

        while True:
            clear_terminal()
            conns_str = get_connections_str()

            try:
                conns_dict = PlugboardValidators.valid_stecker_pb_settings_string(conns_str, charset_flag)
            except SteckerPBSettingsStringError as e:
                print(e.__str__())
                continue

            self._plugboard_obj.make_connections(conns_dict["PLUGBOARD_CONNECTIONS"])
            break