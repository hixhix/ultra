from enigma_cli.cyclometer_cli.generate_indicators_cli import GenerateIndicatorsCli
from enigma_cli.cyclometer_cli.find_loops_cli import FindLoopsCli
from enigma_cli.cyclometer_cli.filter_permutations_cli import FilterPermutationsCli
from enigma_cli.cyclometer_cli.make_catalog_cli import MakeCatalogCli

class CyclometerCli:

    def __init__(self, parser):
        """
        
        """
        self._parser = parser
        self._add_parser_arguments()

    def process_args(self, args):
        """
        
        """
        if args['cyclometer'] == 'generate_indicators':
            self._generate_indicators_cli.process_args(args)
        elif args['cyclometer'] == 'find_loops':
            self._find_loops_cli.process_args(args)
        elif args['cyclometer'] == 'filter_perms':
            self._filter_permutations_cli.process_args(args)
        elif args['cyclometer'] == 'catalog_menu':
            self._catalog_cli.process_args(args)

    def _add_parser_arguments(self):
        subparsers = self._parser.add_subparsers(dest='cyclometer')
        subparsers.required = True

        generate_indicators = subparsers.add_parser(
            'generate_indicators',
            help='generate indicators')
        self._generate_indicators_cli = GenerateIndicatorsCli(generate_indicators)

        find_loops = subparsers.add_parser(
            'find_loops',
            help='find loops')
        self._find_loops_cli = FindLoopsCli(find_loops)

        filter_perms = subparsers.add_parser(
            'filter_perms',
            help='filter permutations')
        self._filter_permutations_cli = FilterPermutationsCli(filter_perms)

        catalog = subparsers.add_parser(
            'catalog_menu',
            help='catalog menu')
        self._catalog_cli = MakeCatalogCli(catalog)
