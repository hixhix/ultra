from enigma_cli.zygalski_sheets_cli.zygalski_svg_sheet_solution_cli import ZygalskiSheetSVGSolutionCli
from enigma_cli.zygalski_sheets_cli.zygalski_text_sheet_solution_cli import ZygalskiSheetTextSolutionCli
from argparse import RawTextHelpFormatter



class ZygalskiSheetSolutionCli:

    def __init__(self, parser):
        self._parser = parser
        self._add_description()
        self._add_parser_arguments()

    def process_args(self, args):
        """

        """
        if args["sheet_solution"] == "svg":
            self._svg_solution_cli.process_args(args)
        elif args["sheet_solution"] == "text":
            self._text_solution_cli.process_args(args)

    def _add_description(self):
        """

        """
        self._parser.formatter_class = RawTextHelpFormatter
        self._parser.description = (f"Provides an option to generate a zygalski sheet solution in text or svg format.\n\n")

    def _add_parser_arguments(self):
        """

        """
        subparsers = self._parser.add_subparsers(dest='sheet_solution')
        subparsers.required = True

        svg_solution = subparsers.add_parser(
            'svg',
            help='Create an svg sheet solution')
        self._svg_solution_cli = ZygalskiSheetSVGSolutionCli(svg_solution)

        text_solution = subparsers.add_parser(
            'text',
            help='Create a text sheet solution')
        self._text_solution_cli = ZygalskiSheetTextSolutionCli(text_solution)
