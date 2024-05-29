from argparse import ArgumentError


class CeaserCipherShiftCli:

    def __init__(self, parser):
        self._parser = parser
        self._add_parser_arguments()

    def process_args(self, args):

        ceaser_cipher_str = f"CHARACTER STRING  {self._character_string}\n\n"

        for i in range(26):
            #ceaser_cipher_str += f"CEASER SHIFT {str(i).rjust(2, '0')} "
            ceaser_cipher_str += f"CEASER SHIFT {chr(i+65)}    "

            for c in self._character_string:
                n = ord(c)
                n += i
                if n >= 91:
                    n = n -26
                ceaser_cipher_str += chr(n)
            ceaser_cipher_str += "\n"

        print(ceaser_cipher_str)

    def _add_parser_arguments(self):
        self._parser.add_argument('Characters string', type=self._valid_character_string, help='Characters to perform a ceaser cipher shift on')

    def _valid_character_string(self, character_string):
        letters = [chr(i) for i in range(65, 91)]

        character_string = character_string.upper()

        for c in character_string:
            if c not in letters:
                raise ArgumentError(f"{c} is not a valid character. Must be in range A-Z.")
            
        self._character_string = character_string