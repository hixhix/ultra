

def filter_females(indicators, groups=None):
    """
    
    """
    valid_groups = ["G1","G2","G3"]

    if groups:
        for group in groups:
            if group not in valid_groups:
                msg = f"{group} is not a valid group. Must be in 'G1','G2','G3'."
                raise ValueError(msg)

    females = []

    groups = groups or valid_groups

    for i in indicators:
        indicator = i.split(' ')
        match = None
        outp = indicator[1]
        if ("G1" in groups) and (outp[0] == outp[3]):
            match = outp
        if ("G2" in groups) and (outp[1] == outp[4]):
            match = outp
        if ("G3" in groups) and (outp[2] == outp[5]):
            match = outp
        if match:
            females.append(f"{indicator[0]} {match}")

    unique_females = list(set(females))

    return unique_females