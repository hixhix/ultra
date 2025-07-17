from enigma_cli.zygalski_sheets_cli.svg_sheet_cli import SvgSheetCli
from enigma_cli.zygalski_sheets_cli.text_sheet_cli import TextSheetCli



class ZygalskiSheetCli:

    def __init__(self, parser):
        self._parser = parser
        self._add_description()
        self._add_parser_arguments()

    def process_args(self, args):
        """

        """
        if args["zygalski_sheets"] == 'svg_sheet':
            self._svg_zygalski_sheet_cli.process_args(args)
        elif args["zygalski_sheets"] == 'text_sheet':
            self._text_zygalski_sheet_cli.process_args(args)

    def _add_description(self):
        """

        """
        self._parser.description = "Provides an option to generate a zygalski sheet in text or svg format.\n\n"

    def _add_parser_arguments(self):
        """

        """
        subparsers = self._parser.add_subparsers(dest='zygalski_sheets')
        subparsers.required = True

        svg_zygalski_sheet = subparsers.add_parser(
            'svg_sheet',
            help='Create a zygalski sheet in svg format')
        self._svg_zygalski_sheet_cli = SvgSheetCli(svg_zygalski_sheet)

        text_zygalski_sheet = subparsers.add_parser(
            'text_sheet',
            help='Creates a zygalski sheet in text format')
        self._text_zygalski_sheet_cli = TextSheetCli(text_zygalski_sheet)
