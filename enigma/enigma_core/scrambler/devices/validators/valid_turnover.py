from enigma_core.settings.settings import LETTERS


class TurnoverListError(Exception):

    def __init__(self, msg):
        """

        """
        super().__init__(msg)


class TurnoverListDescriptor(object):

    def __set_name__(self, owner, name):
        """

        """
        self.private_name = '_' + name

    def __get__(self, obj, objtype =None):
        """

        """
        return getattr(obj, self.private_name)

    def __set__(self, obj, val):
        """

        """
        for char in val:
           if char not in LETTERS:
               raise TurnoverListError(f"")
        turnovers = [LETTERS.index(c) for c in val]
        setattr(obj, self.private_name, turnovers)
