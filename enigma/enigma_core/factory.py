from enigma_core.enigma_core.enigma import Enigma
from enigma_core.settings.settings import EQUIPMENT_DICT

def make_machine(machine_type, settings=None):
    """

    """
    settings = settings or {}
    try:
        EQUIPMENT_DICT[machine_type]
    except KeyError:
        raise ValueError(f"{machine_type} is not a valid machine type")
    else:
        enigma = Enigma(machine_type)

        if settings:
            enigma.settings = settings
        return enigma

def machine_list():
    """

    """
    return list(EQUIPMENT_DICT.keys())
