from tambo import Parse

class Transport(Parse):
    """
    This class inherits from the ``Parse`` object that provides the engine
    to parse arguments from the command line, and it extends the functionality
    to be able to dispatch on mapped objects to subcommands.

    :param arguments: Should be the *exact* list of arguments coming from ``sys.argv``
    :keyword mapper: A dictionary of mapped subcommands to classes
    """


    def dispatch(self):
        mapper_keys = self.mapper.keys()
        for arg in self.arguments:
            if arg in mapper_keys:
                instance = self.mapper.get(arg)(self.arguments)
                return instance.parse_args()
        self.parse_args()


    def subhelp(self):
        """
        This method will look at every value of every key in the mapper
        and will output any ``class.help`` possible to return it as a
        string that will be sent to stdout.
        """
        help_text = self._get_all_help_text()

        if help_text:
            return "Available subcommands:\n\n%s\n" % ''.join(help_text)
        return ''

    def _get_all_help_text(self):
        help_text_lines = []
        for key, value in self.mapper.items():
            try:
                help_text = value.help
            except AttributeError:
                continue
            help_text_lines.append("%-24s %s\n" % (key, help_text))
        return help_text_lines
