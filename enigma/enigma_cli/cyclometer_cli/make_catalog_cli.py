from cyclometer.make_catalog import Cyclometer, CatalogError


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

        if args["make_catalog"]:
            try:
                cyclometer.check_catalog()
            except CatalogError as e:
                cyclometer.make_cyclometer_catalogs()
            else:
                print("Catalog already exists.")
        elif args["check_catalog"]:
            try:
                cyclometer.check_catalog()
            except CatalogError as e:
                print(e)
                print("Catalog may be corrupted. Recommended remaking the catalog.")
            else:
                print("Catalog exists and is valid.")
        elif args["force_catalog"]:
            menu_str = (f"Enter a number to select an option.\n"
                        f"1. To create the zygalski catalog.\n"
                        f"2. Quit.\n")
            
            while True:
                inpt = input(menu_str)

                if inpt == "1":
                    cyclometer.make_cyclometer_catalogs()                    
                elif inpt =="2":
                    break
                else:
                    print("Invalid input!. Try again.")

    def _add_parser_arguments(self):
        """
        
        """
        group = self._parser.add_mutually_exclusive_group()
        group.add_argument('-m', '--make-catalog', action='store_true', help='Make catalog')
        group.add_argument('-c', '--check-catalog', action='store_true', help='Check catalog exists')
        group.add_argument('-f', '--force-catalog', action='store_true', help='Force make catalog')
        group.required = True
