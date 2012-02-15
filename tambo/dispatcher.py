

class Transport(object):
    """
    This class recieves the ``sys.argv`` list and will call the dictionary
    mappings when they match the subcommands.

    :param arguments: Should be the *exact* list of arguments coming from ``sys.argv``
    :keyword mapper: A dictionary of mapped subcommands to classes
    """


    def __init__(self, arguments, mapper=None):
        self.arguments = arguments
        self.mapper = mapper or {}


    def dispatch(self):
        mapper_keys = self.mapper.keys()
        for arg in self.arguments:
            if arg in mapper_keys:
                instance = self.mapper.get(arg)(self.arguments)
                return instance.parse_args()
