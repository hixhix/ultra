from bombe_machines.filter_cribs import FilterCribs
from argparse import RawTextHelpFormatter
import os


class FilterCribsCli:

    LETTERS = [chr(i) for i in range(65, 91)]
    NUMBERS = [f"{i+1}".rjust(2, '0') for i in range(26)]

    def __init__(self, parser):
        self._parser = parser
        self._add_description()
        self._add_parser_arguments()

    def process_args(self, args):
        cipher_text_filepath = args["cipher_text_filepath"]
        plain_text = args["plain_text"]

        if not os.path.isfile(cipher_text_filepath):
            raise Exception(f"{cipher_text_filepath} is not a valid file path")

        with open(cipher_text_filepath, "r") as f:
            cipher_text = f.read()

        crib_filter = FilterCribs()
        results = crib_filter.filter_cribs(cipher_text, plain_text)

        cipher_text = results["cipher_text"]
        plain_text = results["plain_text"]
        crib_string = results["crib_string"]
        cribs = results["cribs"]

        results_str = ""

        formatted_crib_string = "CIPHER TEXT: UPPERCASE WHERE VALID CRIB IS PRESENT\n\n"

        line_len = len(plain_text) + 14

        while True:
            if len(crib_string) > line_len:
                formatted_crib_string += f"{crib_string[0:line_len]}\n"
                crib_string = crib_string[line_len::]
            else:
                formatted_crib_string += crib_string
                break

        results_str += f"{formatted_crib_string}\n\n"

        results_str += f"PLAIN TEXT:\n\n{plain_text}\n\n"

        results_str += f"CRIBS{' '*(len(plain_text)-4)} START  END\n\n"

        for crib in cribs:
            results_str += f"{crib[0]}  {crib[1] :0>5}  {crib[2] :0>5}\n"

        print(results_str)

    def _add_description(self):
        self._parser.formatter_class = RawTextHelpFormatter
        self._parser.description = (f"The plain text string will be alligned with each position in the cipher string and will filter the parts\n"
                                    f"of the cipher text where none of the characters in the plain text are the same as there alligned characters in the plain text.\n"
                                    f"The filtered parts of the cipher text would later be used to create menus for the bombe machines.\n"
                                    f"The cipher text must be longer than the plain text.\n\n")

    def _add_parser_arguments(self):
        """

        """
        self._parser.add_argument('cipher_text_filepath', type=str, help='The cipher text')
        self._parser.add_argument('plain_text', type=str, help='The plain text to find the cribs')
