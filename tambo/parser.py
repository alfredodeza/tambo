import sys


class BaseCommandline(dict):

    help          = ('-h', '--h', '--help', 'help')
    version       = ('--version', 'version')
    catch_help    = ''
    catch_version = ''

    def catches_help(self, force=True):
        if self.catch_help:
            if self.check_help or force:
                if [i for i in self.arguments if i in self.help]:
                    self.print_help()
            return False

    def print_help(self):
        self.writer.write(self.catch_help+'\n')
        self.exit()

    def print_version(self):
        self.writer.write(self.catch_version+'\n')
        self.exit()

    def catches_version(self, force=True):
        if self.catch_version:
            if self.check_version or force:
                if [i for i in self.arguments if i in self.version]:
                    self.print_version()
            return False


class Parse(BaseCommandline):

    def __init__(self, arguments, mapper=None, options=None,
                 check_help=True, check_version=True, writer=None):
        self.arguments     = arguments[1:]
        self.mapper        = mapper or {}
        self.options       = options or []
        self.check_help    = check_help
        self.check_version = check_version
        self._arg_count    = {}
        self._count_arg    = {}
        self.writer        = writer or sys.stdout
        self.exit          = sys.exit
        self.unknown_commands = []

    def _build(self):
        extra_args = [i for i in self.arguments]
        for opt in self.options:
            if isinstance(opt, (tuple, list)):
                value = self._single_value_from_list(opt)
                if value:
                    for v in opt:
                        self._remove_item(v, extra_args)
                        self._remove_item(value, extra_args)
                        self[v] = value
                continue
            value = self._get_value(opt)
            if value:
                self._remove_item(value, extra_args)
                self[opt] = self._get_value(opt)
            self._remove_item(opt, extra_args)
        self._remove_cli_helpers(extra_args)
        self.unknown_commands = extra_args

    def _remove_cli_helpers(self, _list):
        if self.catch_help:
            for arg in self.help:
                self._remove_item(arg, _list)
        if self.catch_version:
            for arg in self.version:
                self._remove_item(arg, _list)

    def _remove_item(self, item, _list):
        for index, i in enumerate(_list):
            if item == i:
                _list.pop(index)
        return _list

    def _single_value_from_list(self, _list):
        for value in _list:
            v = self._get_value(value)
            if v:
                return v

    def parse_args(self):
        # Help and Version:
        self.catches_help(force=False)
        self.catches_version(force=False)

        for count, argument in enumerate(self.arguments):
            self._arg_count[argument] = count
            self._count_arg[count]    = argument

        # construct the dictionary
        self._build()

    def _get_value(self, opt):
        count = self._arg_count.get(opt)
        if count == None:
            # is it possible we got --option=value ?
            flag_equals = "%s=" % opt
            for argument in self.arguments:
                if argument.startswith(flag_equals):
                    return argument.split(flag_equals)[-1]
            return None
        value = self._count_arg.get(count+1)

        return value

    def has(self, opt):
        if isinstance(opt, (tuple, list)):
            for i in opt:
                if i in self._arg_count.keys():
                    return True
            return False
        if opt in self._arg_count.keys():
            return True
        return False
