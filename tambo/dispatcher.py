from tambo import Parse

class Transport(Parse):
    """
    This class inherits from the ``Parse`` object that provides the engine
    to parse arguments from the command line, and it extends the functionality
    to be able to dispatch on mapped objects to subcommands.

    :param arguments: Should be the *exact* list of arguments coming from ``sys.argv``
    :keyword mapper: A dictionary of mapped subcommands to classes
    """


    def dispatch(self, mapper=None):
        mapper = mapper or {}
        mapper_keys = mapper.keys()
        for arg in self.arguments:
            if arg in mapper_keys:
                instance = mapper.get(arg)(self.arguments)
                return instance.parse_args()
