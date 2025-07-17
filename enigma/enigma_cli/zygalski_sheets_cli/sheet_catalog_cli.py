from zygalski_sheets.create_catalog import ZygalskiSheetCatalog, CatalogError
from argparse import RawTextHelpFormatter


class SheetCatalogCli:

    # make catalog
    # check catalog exists
    # force make catalog

    def __init__(self, parser):
        self._parser = parser
        self._add_description()
        self._add_sub_parsers()

    def process_args(self, args):

        catalog_generator = ZygalskiSheetCatalog()

        if args["make_catalog"]:
            try:
                catalog_generator.check_catalog()
            except CatalogError as e:
                catalog_generator.make_catalog()
            else:
                print("Catalog already exists.")
        elif args["check_catalog"]:
            try:
                catalog_generator.check_catalog()
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
                    catalog_generator.make_catalog()
                elif inpt =="2":
                    break
                else:
                    print("Invalid input!. Try again.")

    def _add_description(self):
        self._parser.formatter_class = RawTextHelpFormatter
        self._parser.description = (f"Allows for the zygalski sheet catalog to be created and for an existing catalog to be checked for integrity.\n"
                                    f"If the existing catalog is invalid then a forced recreation of the catalog can be performed.\n\n")

    def _add_sub_parsers(self):
        """

        """
        group = self._parser.add_mutually_exclusive_group()
        group.add_argument('-m', '--make-catalog', action='store_true', help='Make catalog')
        group.add_argument('-c', '--check-catalog', action='store_true', help='Check catalog exists')
        group.add_argument('-f', '--force-catalog', action='store_true', help='Force make catalog')
        group.required = True
