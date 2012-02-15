

class Transport(object):
    """
    This class recieves the ``sys.argv`` list and will call the dictionary 
    mappings when they match the subcommands.

    :param arguments: Should be the *exact* list of arguments coming from ``sys.argv``
    :keyword mapper: A dictionary of mapped subcommands to classes
    """


    def __init__(self, arguments, mapper=None):
        self.arguments = arguments
        self.mapper = mapper


    def dispatch(self):
        pass
