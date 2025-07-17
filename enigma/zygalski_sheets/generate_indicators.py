from enigma_core.factory import make_machine
from collections import deque
import random


def generate_indicators(machine_type, settings, number, herivel=False):
    """

    """
    LETTERS = [chr(i) for i in range(65, 91)]

    machine = make_machine(machine_type, settings)

    herivel_tips_number = number//100

    settings["SCRAMBLER_SETTINGS"]["SCRAMBLER_CHARSET_FLAG"] = 'L'
    settings["PLUGBOARD_SETTINGS"]["PLUGBOARD_MODE"] = 'S'

    ring_settings = settings["SCRAMBLER_SETTINGS"]["RING_SETTINGS"]
    ring_settings_list = list(ring_settings.values())
    ring_settings_list.reverse()

    indicators = []

    choices = [1,2,2,3,3,3,4,4,4,4,5,5,5,5,5,6,6,7,7,7]

    for n in range(number):

        rot_settings = ""

        choice = random.choice(choices)

        if herivel and n <= herivel_tips_number and choice == 1:
            rot_settings = "".join(ring_settings_list)
        elif herivel and n > herivel_tips_number and choice in [2,3,4,5,6]:
            for i in range(0,3,1):
                direction = random.choice(["U","D"])
                rotor_ring = deque(LETTERS)
                rotor_ring.rotate(-LETTERS.index(ring_settings_list[i]))
                if direction == "U":
                    rotor_ring.rotate(random.randrange(0,choice,1))
                elif direction == "D":
                    rotor_ring.rotate(random.randrange(0,-choice,-1))
                rot_settings += rotor_ring[0]
        else:
            for r in range(3):
                rot_settings += random.choice(LETTERS)

        rotor_settings = {
            "RS":rot_settings[0],
            "RM":rot_settings[1],
            "RF":rot_settings[2]
        }

        settings["SCRAMBLER_SETTINGS"]["ROTOR_SETTINGS"] = rotor_settings

        machine.settings = settings

        inpt = ""

        letters = LETTERS.copy()
        random.shuffle(letters)

        for i in range(3):
            inpt += random.choice(letters)

        indicator = inpt*2

        output = ""

        for c in indicator:
            output += machine.character_input(c)

        indicators.append(f"{rot_settings} {output}")

    random.shuffle(indicators)

    return indicators
