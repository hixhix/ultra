

class PBSocketIDError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)



def valid_pb_socket_id(socket_id, charset_flag):
        """
        Takes a plugboard socket and checks if it conforms to the provided charset flag.
        Returns a formated socket id. If not valid raises PBSocketIDError.
        """
        LETTERS = [chr(i) for i in range(65, 91)]
        NUMBERS = [f"{i+1}".rjust(2,'0') for i in range(26)]

        charset_flag = charset_flag.upper()
        if charset_flag not in ["L","N"]:
            raise Exception(f"{charset_flag} is not a valid charset_flag. Must be 'L' or 'N'.")

        err_msg = None

        if charset_flag == "L" and socket_id not in LETTERS:
            err_msg = f"{socket_id} is not a valid plugboard socket id. Must be letter A-Z."
        elif charset_flag == "N" and socket_id not in NUMBERS:
            err_msg = f"{socket_id} is not a valid plugboard socket id. Must be number 01-26."

        if err_msg:
            raise PBSocketIDError(err_msg)
