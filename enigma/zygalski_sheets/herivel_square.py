

def herivel_square(indicators):
    """
    
    """
    LETTERS = [chr(i) for i in range(65, 91)]

    square_dict = {f"{rs}{rm}":" " for rs in LETTERS for rm in LETTERS}

    for indicator in indicators:
        rs = indicator[0]
        rm = indicator[1]
        rf = indicator[2]
        square_dict[f"{rs}{rm}"] = rf

    square_str = (f"            SLOW ROTOR          \n"
                  f"    ABCDEFGHIJKLMNOPQRSTUVWXYZ  \n"
                  f"    ||||||||||||||||||||||||||  \n")
    
    side_title = "       MIDDLE ROTOR            "

    line = 0

    for rm in LETTERS:
        square_str += f"{side_title[line]} "
        line += 1
        for rs in LETTERS:
            if rs == "A":
                square_str += f"{rm}-"
                square_str += square_dict[f"{rs}{rm}"]
            elif rs == "Z":
                square_str += square_dict[f"{rs}{rm}"]
                square_str += f"-{rm}\n"
            else:    
                square_str += square_dict[f"{rs}{rm}"]

    square_str += (f"    ||||||||||||||||||||||||||  \n"
                   f"    ABCDEFGHIJKLMNOPQRSTUVWXYZ  ")

    return square_str