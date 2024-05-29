from enigma_core.validators.scrambler_validators.scrambler_validators import ScramblerValidators, PermutationError
from zygalski_sheets.sheet_data import SheetDataGenerator
from zygalski_sheets.zygalski_sheets_svg.svg_sheet import SVGZygalskiSheet
from zygalski_sheets.zygalski_sheets_svg.svg_sheet_short import SVGZygalskiSheetShort
from argparse import ArgumentError


class SvgSheetCli:

    def __init__(self, parser):
        self._parser = parser
        self._add_parser_arguments()

    def process_args(self, args):
        perm_str = args["permutation"]
        short = args["short"]

        try:
            perm_dict = ScramblerValidators.valid_permutation_string(self._machine_type, perm_str, rs_flag=True, group_flag=False)
        except PermutationError as e:
            raise e
        else:
            settings = {
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
            for group in ["G1","G2","G3"]:
                sheet_id = f"{perm_str}_{group}"
                if not short:
                    svg_sheet_generator = SVGZygalskiSheet(sheet_data, sheet_id, group)
                else:
                    svg_sheet_generator = SVGZygalskiSheetShort(sheet_data, sheet_id, group)
                svg_sheet = svg_sheet_generator.render_svg_sheet()
                with open(f"{perm_str}_{group}.svg", "w") as f:
                    f.write(svg_sheet)

    def _add_parser_arguments(self):
        self._parser.add_argument('machine_type', type=self._valid_machine_type, help='Machine type "WEHRMACHT early" or "WEHRMACHT late"')
        self._parser.add_argument(
            "permutation", 
            help=f"provide a permutation in form 'A_UKW-B_III_II_I'. "
            f"returns svg zygalski sheets.")
        self._parser.add_argument(
            "-s","--short",
            action="store_true",
            help=f"will return a single quadrant of the zygalski sheet")
        
    def _valid_machine_type(self, machine_type):
        valid_machines = ["WEHRMACHT early","WEHRMACHT late"]

        for _machine_type in valid_machines:
            if machine_type.upper() == _machine_type.upper():
                self._machine_type = _machine_type
                return _machine_type
        raise ArgumentError(f"{machine_type} is not a valid enigma machine. Must be 'WEHRMACHT early' or 'WEHRMACHT late'")
    