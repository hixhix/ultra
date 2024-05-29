from cyclometer.make_catalog import Cyclometer


class MakeCatalogCli:

    def __init__(self, parser):
        """
        
        """
        self._parser = parser
        self._add_parser_arguments()

    def process_args(self, args):
        """
        
        """
        cyclometer = Cyclometer()

        print(args)

        if args["make_catalog"]:
            cyclometer.make_cyclometer_catalogs()
        elif args["check_catalog"]:
            cyclometer.check_cyclometer_catalog_exists()
        elif args["force_catalog"]:
            cyclometer.make_cyclometer_catalogs()

    def _add_parser_arguments(self):
        """
        
        """
        group = self._parser.add_mutually_exclusive_group()
        group.add_argument('-m', '--make-catalog', action='store_true', help='Make catalog')
        group.add_argument('-c', '--check-catalog', action='store_true', help='Check catalog exists')
        group.add_argument('-f', '--force-catalog', action='store_true', help='Force make catalog')
        group.required = True
