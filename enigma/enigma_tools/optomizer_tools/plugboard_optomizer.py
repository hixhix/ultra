



class PlugboardOptomizer:

    def __init__(self):
        pass

    def optomize(self, cipher_text, plain_text, intermediary_text):
        # get unconnected
        # get best connections
        _cipher_text = ""
        _plain_text = ""
        _intermediary_text = ""
        unconnected = []
        possible_pairs = []
        result_dict = {}

        for i in range(len(cipher_text)):
            if plain_text[i] == intermediary_text[i]:
                unconnected.append(plain_text[i])

        unconnected = list(set(unconnected))
        unconnected = sorted(unconnected)

        for i in range(len(cipher_text)):
            c1 = plain_text[i]
            c2 = intermediary_text[i]
            if c1 != c2 and c1 not in unconnected and c2 not in unconnected:
                pair = [c1,c2]
                possible_pairs.append(sorted(pair))

        possible_pairs_dict = {}

        for pair in possible_pairs:
            pair_str = f"{pair[0]}{pair[1]}"
            if pair_str not in possible_pairs_dict.keys():
                possible_pairs_dict[pair_str] = possible_pairs.count(pair)

        for i in range(len(cipher_text)):
            c1 = plain_text[i]
            c2 = intermediary_text[i]
            if c1 == c2:
                _cipher_text += cipher_text[i]
                _plain_text += plain_text[i]
                _intermediary_text += intermediary_text[i]
            elif c1 != c2:
                _cipher_text += cipher_text[i].lower()
                _plain_text += plain_text[i].lower()
                _intermediary_text += intermediary_text[i].lower()

        connected = sorted([[p,c] for p,c in possible_pairs_dict.items()])

        connected = sorted(connected, key=lambda x: x[1], reverse=True)

        result_dict["CIPHER_TEXT"] = _cipher_text
        result_dict["PLAIN_TEXT"] = _plain_text
        result_dict["INTERMEDIARY_TEXT"] = _intermediary_text
        result_dict["PROBABLY_UNCONNECTED"] = unconnected
        result_dict["POSSIBLY_CONNECTED"] = connected

        return result_dict