import sys


class BaseCommandline(dict):

    help          = ['-h', '--h', '--help', 'help']
    version       = ['--version', 'version']
    catch_help    = None
    catch_version = None


    def catches_help(self):
        if self.catch_help and self.check_help:
            if [i for i in self.arguments if i in self.help]:
                self.print_help()
            return False


    def print_help(self):
        self.writer.write(self.catch_help+'\n')
        self.exit()


    def print_version(self):
        self.writer.write(self.catch_version+'\n')
        self.exit()


    def catches_version(self):
        if self.catch_version and self.check_version:
            if [i for i in self.arguments if i in self.version]:
                self.print_version()
            return False




class Parse(BaseCommandline):


    def __init__(self, arguments, mapper=None, options=None, check_help=True, check_version=True):
        self.arguments     = arguments[1:]
        self.mapper        = mapper or {}
        self.options       = options or []
        self.check_help    = check_help
        self.check_version = check_version
        self._arg_count    = {}
        self._count_arg    = {}
        self.writer        = sys.stdout
        self.exit          = sys.exit


    def _build(self):
        for opt in self.options:
            if type(opt) == list:
                value = self._single_value_from_list(opt)
                if value:
                    for v in opt:
                        self[v] = value
                continue
            value = self._get_value(opt)
            if value:
                self[opt] = self._get_value(opt)



    def _single_value_from_list(self, _list):
        for value in _list:
            v = self._get_value(value)
            if v:
                return v


    def parse_args(self):
        # Help and Version:
        self.catches_help()
        self.catches_version()

        for count, argument in enumerate(self.arguments):
            self._arg_count[argument] = count
            self._count_arg[count]    = argument

        # construct the dictionary
        self._build()


    def _get_value(self, opt):
        count = self._arg_count.get(opt)
        if count == None:
            return None
        value = self._count_arg.get(count+1)

        return value


    def has(self, opt):
        if type(opt) == list:
            for i in opt:
                if i in self._arg_count.keys():
                    return True
            return False
        if opt in self._arg_count.keys():
            return True
        return False
