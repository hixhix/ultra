from enigma_app.formatting.formatting import EnigmaFormatter as ef
from enigma_core.validators.plugboard_validators.plugboard_validators import *
from enigma_core.plugboard.uhr_box import UhrBox
from enigma_app.clear_terminal.clear_terminal import clear_terminal


class UhrBoxPlugboardInterface:

    def __init__(self, plugboard_obj):
        """
        Takes an uhr box plugboard object to provide an interface for.        
        """
        self._plugboard_obj = plugboard_obj

    def __str__(self):
        """
        Returns the string repressentation of the uhr box plugboard.
        """
        return ef.center(self._plugboard_obj.__str__())


    def menu(self):
        """
        Provides the uhr box plugboard menu.
        """
        
        while True:
            clear_terminal()
            menu_str = (
                f"{ef.line('UHR BOX PLUGBOARD')}\n"
                f"\n{self.__str__()}\n"
                f"Enter a number to select an option\n"
                f"1. Clear plugboard\n"
                f"2. Connect uhr box plugs\n"
                f"3. Set uhr box setting\n"
                f"4. Return to previous menu\n"
                f"{ef.line()}\n"
            )

            inpt = input(menu_str)
            if inpt == "1": self._clear_plugboard()
            elif inpt == "2": self._connect_uhr_box_plugs()
            elif inpt == "3": self._set_uhr_box_setting()
            elif inpt == "4": return
            else: print("Invalid input! Try agin")

    def character_set_flag(self, flag):
        """
        Sets the plugboard character set to the character set flag provided.
        """
        self._plugboard_obj.character_set_flag = flag

    def _clear_plugboard(self):
        """
        Prompts the user to enter Y/N to confirm if the user wants to clear the
        plugboard. 
        """
        menu_str = f"Are you sure you want to clear the plugboard Y/N. "

        inpt = input(menu_str)

        if inpt.upper() == 'Y':
            self._plugboard_obj.clear()
            clear_terminal()
            print("The plugboard has been cleared.")

    def _connect_uhr_box_plugs(self):
        """
        Prompts the user to input socket ids to connect the uhr box plugs to.
        """
        def get_socket_str(group):
            """
            Takes a uhr box group id. Prompts the user to input socket ids for
            the uhr box plugs in that group.
            """
            if group not in ['A','B']:
                raise ValueError(f"{group} is not a valid group. Must be 'A' or 'B'")
            
            if group == 'A':
                plugs_list = UhrBox.PLUG_A_IDS
            elif group == 'B':
                plugs_list = UhrBox.PLUG_B_IDS

            plug_str = ' '.join(plugs_list)

            msg = (
                f"Enter 10 space seperated socket ids to connect uhr plugs 01{group}-10{group}.\n"
                f"Use rule provided to assign a socket id to an uhr box plug.\n"
                f"{plug_str}\n"
            )

            clear_terminal()
            inpt = input(msg)

            return inpt
        
        def get_group_dict(charset_flag, group, previous=None):
            """
            Takes an uhr box plug group id and plugboard character set. Returns
            a valid socket id list.
            """
            while True:
                settings_str = get_socket_str(group)

                try:
                    group_dict = PlugboardValidators.valid_uhr_box_pb_group_settings(settings_str, charset_flag, group, previous)
                except UhrBoxPBSettingsStringError as e:
                    print(e.__str__())
                else:
                    return group_dict
        
        charset_flag = self._plugboard_obj.character_set_flag

        while True:
            socket_a_dict = get_group_dict(charset_flag, 'A', None)
            socket_b_dict = get_group_dict(charset_flag, 'B', socket_a_dict)
            break

        connections_dict = {**socket_a_dict["PLUGBOARD_CONNECTIONS"], **socket_b_dict["PLUGBOARD_CONNECTIONS"]}
        self._plugboard_obj.make_connections(connections_dict)

    def _set_uhr_box_setting(self):
        """
        Prompts the user to input a rotor setting for the uhr box.        
        """
        menu_str = f"Enter an uhr box rotor setting in the range 0-39. "

        while True:
            clear_terminal()
            try:
                inpt = int(input(menu_str))
            except ValueError:
                print("Invalid input!. Try again.")
            else:
                if 0 <= inpt <= 39:
                    self._plugboard_obj.rotor_setting = inpt
                    break
                else:
                    print("Invalid input!. Try again.")

