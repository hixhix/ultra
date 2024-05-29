from zygalski_sheets.create_catalog import ZygalskiSheetCatalog



class SheetCatalogCli:

    # make catalog
    # check catalog exists
    # force make catalog

    def __init__(self, parser):
        self._parser = parser
        self._add_sub_parsers()

    def process_args(self, args):

        catalog_generator = ZygalskiSheetCatalog()

        if args["make_catalog"]:
            status = catalog_generator.make_catalog()
            print(status)
        elif args["check_catalog"]:
            exists = catalog_generator.check_catalog()
            if exists:
                print("Zygalski sheet catalog exists.")
            else:
                print("Zygalski sheet catalog does not exist.")
        elif args["force_catalog"]:
            menu_str = (f"Enter a number to select an option.\n"
                        f"1. To create the zygalski catalog.\n"
                        f"2. Quit.\n")
            
            while True:
                inpt = input(menu_str)

                if inpt == "1":
                    catalog_generator.force_make_catalog()                    
                elif inpt =="2":
                    break
                else:
                    print("Invalid input!. Try again.")

    def _add_sub_parsers(self):
        """
        
        """
        group = self._parser.add_mutually_exclusive_group()
        group.add_argument('-m', '--make-catalog', action='store_true', help='Make catalog')
        group.add_argument('-c', '--check-catalog', action='store_true', help='Check catalog exists')
        group.add_argument('-f', '--force-catalog', action='store_true', help='Force make catalog')
        group.required = True
