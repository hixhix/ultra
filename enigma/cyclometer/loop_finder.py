



class LoopFinder:

    LETTERS = [chr(i) for i in range(65, 91)]

    def __init__(self):
        """

        """
        self.indicators = None

    def find_all_loops(self, indicators):
        """

        """
        self.indicators = indicators

        loops_dict = {}

        groups = ["G1","G2","G3"]

        for group in groups:
            loops = self.find_loops(group)
            loops = sorted(loops, key=len)
            loops.reverse()
            loop_str = ""
            for loop in loops:
                loop_str += f"({len(loop)})"
            loops_dict[group] = loop_str

        return loops_dict

    def find_loops(self, group):
        """

        """
        offsets = {"G1":0,"G2":1,"G3":2}

        offset = offsets[group]

        pairs_dict = {}

        for indicator in self.indicators:
            c1 = indicator[offset]
            c2 = indicator[offset+3]
            if c1 in pairs_dict.keys() and pairs_dict[c1] != c2:
                c3 = pairs_dict[c1]
                err_msg = f"{c1} already associated with {c2} but also {c3}"
                raise Exception(err_msg)
            else:
                pairs_dict[c1] = c2

        for l in self.LETTERS:
            if l not in pairs_dict.keys():
                keys = pairs_dict.keys()
                err_msg = f"{l} not in {keys}"
                raise Exception(err_msg)

        used = []

        loops = []

        for l in self.LETTERS:
            if l not in used:
                loop = self.find_loop(l, "", used, pairs_dict)
                loops.append(loop)
        return loops

    def find_loop(self, c1, loop_str, used, pairs_dict):
        """

        """
        used.append(c1)
        c2 = pairs_dict[c1]
        # new string c1 and c2 same
        if len(loop_str) == 0 and c1 == c2:
            loop_str = c1
        # c2 is equal to first char in loop
        elif len(loop_str) != 0 and c2 == loop_str[0]:
            loop_str = loop_str + c1
        else:
            loop_str = loop_str + c1
            loop_str = self.find_loop(c2, loop_str, used, pairs_dict)
        return loop_str