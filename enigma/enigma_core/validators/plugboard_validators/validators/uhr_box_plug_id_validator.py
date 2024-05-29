

class UhrBoxPlugIDError(Exception):

    def __init__(self, err_msg):
        """
        Takes an error message string.
        """
        super().__init__(err_msg)


def valid_uhr_box_plug_id(plug_id, group=None):
        """
        Takes an uhr box plug id and checks that it belongs to the provided group.
        Returns a formated plug id. If not valid raises an UhrBoxPlugIDError.
        """
        if group:
            group = group.upper()
            if group not in ["A","B"]:
                err_msg = f""
                raise Exception(err_msg)

        group_a_plugs = [
            "01A","02A","03A","04A","05A",
            "06A","07A","08A","09A","10A"
        ]

        group_b_plugs = [
            "01B","02B","03B","04B","05B",
            "06B","07B","08B","09B","10B"
        ]

        plug_id = plug_id.upper()

        err_msg = None

        if not group and (plug_id not in group_a_plugs and plug_id not in group_b_plugs):
            err_msg = f"{plug_id} is not a valid uhr box plug id."
        elif group == "A" and plug_id not in group_a_plugs:
            err_msg = f"{plug_id} is not a valid uhr box plug id for group 'A' uhr box plugs."
        elif group == "B" and plug_id not in group_b_plugs:
            err_msg = f"{plug_id} is not a valid uhr box plug id for group 'B' uhr box plugs."

        if err_msg:
            raise UhrBoxPlugIDError(err_msg)
        else:
            return plug_id
