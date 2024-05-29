

class FilterCribs:

    LETTERS = [chr(i) for i in range(65,91)]

    def __init__(self):
        """
        
        """
        self._cipher_text = None
        self._plain_text = None

    def filter_cribs(self, cipher_text, plain_text):
        """
        
        """
        self._cipher_text = self._clean_text(cipher_text)
        self._plain_text = self._clean_text(plain_text)

        results = {}
        
        cribs = []
        indexes = []

        for i in range((len(cipher_text) - len(plain_text))):
            crib_text = self._cipher_text[i:(i+len(self._plain_text))]
            if self._is_crib(crib_text, self._plain_text):
                cribs.append([crib_text, i, i+len(self._plain_text)])
                for ind in range(i, i+len(self._plain_text)):
                    if ind not in indexes:
                        indexes.append(ind)

        outp = ""

        for i in range(len(self._cipher_text)):
            c = self._cipher_text[i]
            if i in indexes:
                outp += c
            else:
                outp += c.lower()

        results["cipher_text"] = self._cipher_text
        results["plain_text"] = self._plain_text
        results["crib_string"] = outp
        results["cribs"] = cribs

        return results

    def _is_crib(self, crib_text, plain_text):
        """
        
        """
        for i in range(len(crib_text)):
            if crib_text[i] == plain_text[i]:
                return False
        return True

    def _clean_text(self, text):
        """
        
        """
        clean_text = ""

        text = text.upper()

        for c in text:
            if c in self.LETTERS:
                clean_text += c

        return clean_text
    
    def _valid_text_strings(self, cipher_text, plain_text):
        """
        
        """
        if len(cipher_text) < len(plain_text):
            raise Exception("Cipher text must be longer than plain text.")
