from enigma_core.factory import machine_list, make_machine
from enigma_app.enigma_interface.enigma_interface import EnigmaInterface
from enigma_app.clear_terminal.clear_terminal import clear_terminal


def make_enigma(machine):
    """

    """
    machines = machine_list()

    if machine not in machine_list():
        msg = (f"{machine} is not a valid enigma machine. "
               f"Must be one of the following {machines}.")
        raise ValueError(msg)
    else:
        enigma_obj = make_machine(machine)
        enigma_app = EnigmaInterface(enigma_obj)
        clear_terminal()
        enigma_app.menu()

def enigma_app():
    """

    """
    clear_terminal()

    machines = machine_list()

    menu_str = (
        f"Provides accurate interactive simulation of a selection of enigma machines.\n"
        f"Although not historicaly accurate the following functionality is provided to all enigma machine types.\n"
        f"It is possible to seperatly configure the scrambler and plugboard to use letters or numbers.\n"
        f"The plugboard can be configured as a standard plugboard that uses stecker cables or alternativly to use an uhr box attachment.\n"
        f"\n"
        f"A setup procedure is provided for each unique enigma machine type.\n"
        f"\n"
        f"Additional functionality includes a code sheet feature that can be used to setup the enigma machine.\n"
        f"The code sheets configuration reflects the enigma machines current configuration such as alpha numeric settings and plugboard mode.\n"
        f"\n"
        f"\n"
        f"Enter a number to select a machine."
    )

    while True:

        print(menu_str)

        for index, machine in enumerate(machines, start=1):
            print(f"{index}. {machine}.")

        print(f"{len(machines)+1}. Quit.")

        try:
            inpt = int(input())
        except ValueError:
            pass
        else:
            if 1 <= inpt <= len(machines):
                machine = machines[inpt-1]
                make_enigma(machine)
            elif inpt == len(machines)+1:
                break
            else:
                print("Invalid input!. Try again.")
