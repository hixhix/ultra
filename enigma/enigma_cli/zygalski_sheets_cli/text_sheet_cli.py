from enigma_core.validators.scrambler_validators.scrambler_validators import ScramblerValidators, PermutationError
from zygalski_sheets.sheet_data import SheetDataGenerator
from zygalski_sheets.zygalski_sheets_text.text_sheet import TextZygalskiSheet
from argparse import ArgumentError, RawTextHelpFormatter
import re


class TextSheetCli:

    def __init__(self, parser):
        self._parser = parser
        self._add_description()
        self._add_arguments()

    def process_args(self, args):
        """

        """
        perm_str = args["permutation"]

        try:
            perm_dict = ScramblerValidators.valid_permutation_string(self._machine_type, perm_str, rs_flag=True, group_flag=False)
        except PermutationError as e:
            raise e
        else:
            settings = {
                "MACHINE_TYPE":self._machine_type,
                "SCRAMBLER_SETTINGS":{
                    "REFLECTOR_TYPE":perm_dict["REFLECTOR"],
                    "ROTOR_TYPES":{
                        "RS":perm_dict["RS_TYPE"],
                        "RM":perm_dict["RM_TYPE"],
                        "RF":perm_dict["RF_TYPE"]
                    },
                    "ROTOR_SETTINGS":{
                        "RS":perm_dict["RS_SETTING"],
                        "RM":"A",
                        "RF":"A"
                    },
                    "RING_SETTINGS":{"RS":"A","RM":"A","RF":"A"}
                }
            }
            sheet_data_generator = SheetDataGenerator()
            sheet_data = sheet_data_generator.data(settings, self._machine_type, "A")

            text_sheet_generator = TextZygalskiSheet(settings, sheet_data)
            groups = args["groups"]

            if groups:
                p = re.compile("[123]")
                groups = re.findall(p, groups)
                groups = [int(i) for i in groups]
            else:
                groups = [1,2,3]
            charset = None
            if args["l"] == True:
                charset = "L"
            elif args["n"]:
                charset = "N"
            text_sheet = text_sheet_generator.text_sheet(groups, "N", charset, sheet_data, True)
            print(text_sheet)

    def _add_description(self):
        self._parser.formatter_class = RawTextHelpFormatter
        self._parser.description = (f"Produces a zygalski sheet in text format using the provided enigma machine type and scrambler permutation.\n"
                                    f"The optional groups argument allows control over the numerical value to be displayed in the zygalski sheet.\n"
                                    f"The numerical value that appears at each position in the zygalski sheet is the sum of numbers that repressent\n"
                                    f"each group.\n"
                                    f"\n"
                                    f"Group   Number\n"
                                    f"1       1\n"
                                    f"2       2\n"
                                    f"3       4\n"
                                    f"\n"
                                    f"Groups  Sum\n"
                                    f"1       1\n"
                                    f"2       2\n"
                                    f"12      3\n"
                                    f"3       4\n"
                                    f"13      5\n"
                                    f"23      6\n"
                                    f"123     7\n\n")

    def _add_arguments(self):
        """

        """
        self._parser.add_argument('machine_type', type=self._valid_machine_type, help='Machine type "WEHRMACHT early" or "WEHRMACHT late"')
        self._parser.add_argument(
            "permutation", 
            help=f"provide a permutation in form 'A_UKW-B_III_II_I'. "
            f"returns a text zygalski sheet.")
        self._parser.add_argument(
            "--groups",
            help=f"enter the groups of females you want '1,2,3'. "
            f"defaults to all groups."
        )

        group = self._parser.add_mutually_exclusive_group()
        group.add_argument("-l", action="store_true", help="alpha output")
        group.add_argument("-n", action="store_true", help="numeric output")
        group.required = True

    def _valid_machine_type(self, machine_type):
        valid_machines = ["WEHRMACHT early","WEHRMACHT late"]

        for _machine_type in valid_machines:
            if machine_type.upper() == _machine_type.upper():
                self._machine_type = _machine_type
                return _machine_type
        raise ArgumentError(f"{machine_type} is not a valid enigma machine. Must be 'WEHRMACHT early' or 'WEHRMACHT late'")
