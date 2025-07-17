from enigma_core.settings.settings import EQUIPMENT_DICT
from enigma_tools.optomizer_tools.ring_settings_optomizer import RingSettingsOptomizer
from enigma_core.validators.plugboard_validators.plugboard_validators import PlugboardValidators
from enigma_core.validators.scrambler_validators.scrambler_validators import ScramblerValidators, PermutationError
from enigma_core.factory import machine_list
from pprint import pprint


class RingSettingsOptomizerCli:

    LETTERS = [chr(i) for i in range(65,91)]

    def __init__(self, parser):
        self._parser = parser
        self._add_parser_description()
        self._add_parser_arguments()

    def process_args(self, args):
        permutation = args["permutation"]
        machine_type = args["machine_type"]
        start_core_positions = args["start_positions"]
        plugboard_settings = args["plugboard_settings"]
        cipher_text_fpath = args["cipher_text_file"]

        machine_type = self._valid_machine(machine_type)

        perm = self._valid_permutation(permutation, machine_type)

        positions = len(EQUIPMENT_DICT[machine_type]["CELLS_MAP"].keys()) -1

        start_core_positions = ScramblerValidators.valid_rotor_settings_string(start_core_positions, "L", positions)

        plugboard_settings = PlugboardValidators.valid_stecker_pb_settings_string(plugboard_settings, "L")

        with open(cipher_text_fpath, "r") as f:
            cipher_text = f.read()

        pb_conns = []

        for c1 in self.LETTERS:
            c2 = plugboard_settings[c1]
            if c1 != c2 and (c2,c1) not in pb_conns:
                pb_conns.append((c1,c2))

        perm_dict = perm[1]

        settings = {
            "reflector":perm_dict["REF"],
            "rotor_types":{
                "RS":perm_dict["ROT_RS"],
                "RM":perm_dict["ROT_RM"],
                "RF":perm_dict["ROT_RF"]
            },
            "plugboard_mode":"S",
            "plugboard_connections":pb_conns
        }

        optomizer = RingSettingsOptomizer(cipher_text, settings, start_core_positions)
        ring_settings = optomizer.solve()

        add_newline = False

        settings_str = "ROTOR_SETTINGS  RING_SETTINGS   IOC     BIGRAM_COUNT    TRIGRAM_COUNT\n"
        settings_str += "RS RM RF        RS RM RF\n"

        for result in ring_settings:
            if add_newline:
                settings_str += "\n"
            add_newline = True
            settings = result[0]
            rot_sets = settings["rotor_settings"]
            settings_str += f"{rot_sets['RS']}  {rot_sets['RM']}  {rot_sets['RF']}"
            rng_sets = settings["ring_settings"]
            settings_str += f"         {rng_sets['RS']}  {rng_sets['RM']}  {rng_sets['RF']} "
            ioc = settings["index_of_coincidence"]
            settings_str += f"        {ioc:.3f} "
            bigram_count = settings["bigram_count"]
            settings_str += f"      {bigram_count:8d} "
            trigram_count = settings["trigram_count"]
            settings_str += f"        {trigram_count:8d} "

        print(settings_str)

    @staticmethod
    def _valid_machine(machine_type):
        """

        """
        machines_list = machine_list()

        if machine_type not in machines_list:
            raise Exception(f"{machine_type} is not a valid enigma machine")

    @staticmethod
    def _valid_permutation(permutation, machine_type):
        """

        """
        try:
            perm = ScramblerValidators.valid_permutation_string(machine_type, permutation, rs_flag=True, group_flag=True)
            return perm
        except PermutationError:
            pass
        try:
            perm = ScramblerValidators.valid_permutation_string(machine_type, permutation, rs_flag=False, group_flag=True)
            return perm
        except PermutationError:
            pass
        try:
            perm = ScramblerValidators.valid_permutation_string(machine_type, permutation, rs_flag=False, group_flag=False)
            return perm
        except PermutationError:
            err_msg = f"Permutation {permutation} is not a valid permutation."
            raise PermutationError(err_msg)

    def _add_parser_description(self):
        """

        """
        _str = "The ring optomizer module optomizes the ring settings based on bigram, trigram count and index of coincidence."

        self._parser.description = _str

    def _add_parser_arguments(self):
        # permutation start_core_positions plugboard_settings cipher_text_file
        self._parser.add_argument('permutation',type=str,help='The scrambler permutation in format "A UKW-B III II I G3"')
        self._parser.add_argument('machine',type=str,help='The enigma machine type ( WEHRMACHT early | WEHRMACHT late | LUFTWAFFE | Kriegsmarine M3 | Kriegsmarine M4 )')
        self._parser.add_argument('start_positions',type=str,help='Rotor start positions in format "RS,RM,RF"')
        self._parser.add_argument('plugboard_settings',type=str,help='Plugboard settings in format "AB,CD,EF,GH,IJ,KL,MN,OP,QR,ST"')
        self._parser.add_argument('cipher_text_file',type=str,help='Cipher text file path')
