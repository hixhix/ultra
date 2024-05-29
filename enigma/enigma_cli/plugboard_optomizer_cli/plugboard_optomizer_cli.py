from enigma_tools.optomizer_tools.plugboard_optomizer import PlugboardOptomizer
from argparse import ArgumentError
import json
import os


class PlugboardOptomizerCli:

    def __init__(self, parser):
        self._parser = parser
        self._add_parser_arguments()

    def process_args(self, args):

        with open(self._file_path, "r") as f:
            text_data = json.loads(f.read())

        plain_text = text_data["PLAIN_TEXT"]
        cipher_text = text_data["CIPHER_TEXT"]
        intermediary_text = text_data["INTERMEDIARY_TEXT"]

        result_dict = PlugboardOptomizer().optomize(cipher_text, plain_text, intermediary_text)

        optomizer_str = "CIPHER TEXT".ljust(22, " ")

        optomizer_str += result_dict["CIPHER_TEXT"]

        optomizer_str += "\n"

        optomizer_str += "INTERMEDIARY TEXT".ljust(22, " ")

        optomizer_str += result_dict["INTERMEDIARY_TEXT"]

        optomizer_str += "\n"

        optomizer_str += "PLAIN TEXT".ljust(22, " ")

        optomizer_str += result_dict["PLAIN_TEXT"]

        optomizer_str += "\n"

        unconnected = result_dict["PROBABLY_UNCONNECTED"]

        optomizer_str += "\n"

        optomizer_str += "PROBABLY UNCONNECTED  "

        for c in unconnected:
            optomizer_str += f"{c} "

        connected = result_dict["POSSIBLY_CONNECTED"]

        optomizer_str += "\n\nPOSSIBLY CONNECTED    "

        for conn in connected:
            p, c = conn
            optomizer_str += f"{p} {c}  "

        print(optomizer_str)

    def _add_parser_arguments(self):
        self._parser.add_argument('text_file',type=self._valid_file_path,help='The file path for the data file')

    def _valid_file_path(self, file_path):
        """
        
        """
        if os.path.isfile(file_path):
            self._file_path = file_path
        else:
            raise ArgumentError(f"{file_path} is not a valid input file path.")