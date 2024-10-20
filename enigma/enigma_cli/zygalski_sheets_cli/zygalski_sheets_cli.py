from enigma_cli.zygalski_sheets_cli.zygalski_sheet_solution_cli import ZygalskiSheetSolutionCli
from enigma_cli.zygalski_sheets_cli.indicators_generator_cli import IndicatorsGeneratorCli
from enigma_cli.zygalski_sheets_cli.herivel_square_cli import HerivelSquareCli
from enigma_cli.zygalski_sheets_cli.ceaser_cipher_shift_cli import CeaserCipherShiftCli
from enigma_cli.zygalski_sheets_cli.zygalski_sheet_cli import ZygalskiSheetCli
from enigma_cli.zygalski_sheets_cli.permutation_filter_cli import PermutationsFilterCli
from enigma_cli.zygalski_sheets_cli.sheet_catalog_cli import SheetCatalogCli

# zygalski sheets
    #    svg zygalsi sheets
    #    svg zygalski sheets solution
    #    text zygalski sheets
    #    indicators generator
    #    permutations filter
    #    wehrmacht catalog

class ZygalskiSheetsCli:

    def __init__(self, parser):
        self.parser = parser
        self._add_sub_parsers()

    def process_args(self, args):
        """

        """
        if args['sheets'] == 'indicators':
            self._indicators_generator_cli.process_args(args)

        elif args['sheets'] == 'herivel_square':
            self._herivel_square_cli.process_args(args)

        elif args['sheets'] == 'permutation_filter':
            self._permutation_filter_cli.process_args(args)

        elif args['sheets'] == 'ceaser_cipher_shift':
            self._ceaser_shift_cli.process_args(args)

        elif args['sheets'] == 'zygalski_sheet':
            self._zygalski_sheet_cli.process_args(args)

        elif args['sheets'] == 'sheet_solution':
            self._zygalski_sheet_solution_cli.process_args(args)

        elif args['sheets'] == 'zygalski_catalog':
            self._wehrmacht_catalog_cli.process_args(args)

    def _add_sub_parsers(self):
        """

        """
        subparsers = self.parser.add_subparsers(dest='sheets')
        subparsers.required = True

        indicators_generator = subparsers.add_parser(
            'indicators',
            help='Generate and filter enigma indicators')
        self._indicators_generator_cli = IndicatorsGeneratorCli(indicators_generator)

        herivel_square = subparsers.add_parser(
            'herivel_square',
            help='Generates a herivel square of the indicators')
        self._herivel_square_cli = HerivelSquareCli(herivel_square)

        permutation_filter = subparsers.add_parser(
            'permutation_filter',
            help='Filters permutations')
        self._permutation_filter_cli = PermutationsFilterCli(permutation_filter)

        ceaser_shift = subparsers.add_parser(
            'ceaser_cipher_shift',
            help='Perform a ceaser cipher shift on a character string')
        self._ceaser_shift_cli = CeaserCipherShiftCli(ceaser_shift)

        zygalski_sheet = subparsers.add_parser(
            'zygalski_sheet',
            help='Zygalski sheet menu')
        self._zygalski_sheet_cli = ZygalskiSheetCli(zygalski_sheet)

        zygalski_sheet_solution = subparsers.add_parser(
            'sheet_solution',
            help='Creates a svg zygalski sheet solution on a lightboard')
        self._zygalski_sheet_solution_cli = ZygalskiSheetSolutionCli(zygalski_sheet_solution)

        wehrmacht_catalog = subparsers.add_parser(
            'zygalski_catalog',
            help='Create the wehrmacht zygalski sheets catalog')
        self._wehrmacht_catalog_cli = SheetCatalogCli(wehrmacht_catalog)
