from py.test import raises
from tambo import Parse
import sys
if sys.version < '3':
    from cStringIO import StringIO
else:
    from io import StringIO


class Test_parsing_arguments(object):

    def test_removes_the_first_item_in_the_list_always(self):
        parser = Parse([])
        parser.parse_args()
        assert parser.arguments == []

    def test_matches_an_option_in_arguments(self):
        parser = Parse(['/usr/bin/foo', '--foo'])
        parser.options = ['--foo']
        parser.parse_args()

        assert parser == {} # No key/values
        assert parser.has('--foo') # But it does exist

    def test_matches_arguments_with_no_values(self):
        parser = Parse(['/usr/bin/foo', '--foo'])
        parser.parse_args()
        assert parser._arg_count    == {'--foo' : 0}
        assert parser._count_arg[0] == '--foo'

    def test_matches_arguments_with_values(self):
        parser = Parse(['/usr/bin/foo', '--foo', 'BAR'])
        parser.parse_args()
        assert parser._arg_count['--foo'] == 0
        assert parser._count_arg[1]       == 'BAR'

    def test_matches_valid_configured_options_only(self):
        parser = Parse(['/bin/tambo', '--foo', 'off', '--meh'])
        parser.options = ['--foo']
        parser.parse_args()
        assert parser.has('--foo')
        assert parser.has('--meh')
        assert parser.get('--foo') == 'off'
        assert parser.get('--meh') is None

    def test_matches_mixed_values_and_arguments(self):
        parser = Parse(['/bin/tambo', '--foo', 'FOO', '--bar'])
        parser.parse_args()
        assert parser._arg_count['--foo'] == 0
        assert parser._arg_count['--bar'] == 2
        assert parser._count_arg[1]       == 'FOO'
        assert parser._count_arg.get(3)   == None

    def test_deals_with_lists_of_lists_in_options(self):
        parser = Parse(['/bin/tambo', '--bar'])
        parser.options = ['--foo', ['--bar', 'bar']]
        parser.parse_args()
        assert parser._arg_count['--bar'] == 0
        assert parser.get('--bar') is None

    def test_can_handle_a_tuple_as_options(self):
        parser = Parse(['foo', '--bar', 'baz'])
        parser.options = [('-b', '--bar')]
        parser.parse_args()
        assert parser.get('--bar') == 'baz'

    def test_deals_with_a_tuple_of_tuples_in_options(self):
        parser = Parse(['/bin/tambo', '--bar'])
        parser.options = ('--foo', ('--bar', 'bar'))
        parser.parse_args()
        assert parser._arg_count['--bar'] == 0
        assert parser.get('--bar') is None


class Test_get_values_from_arguments(object):

    def setup(self):
        self.parser = Parse(['/bin/tambo', '--foo', 'BAR', '--bar'])
        self.parser.parse_args()

    def test_returns_a_valid_value_from_a_matching_argument(self):
        assert self.parser._get_value('--foo') == 'BAR'

    def test_returns_None_when_an_argument_does_not_exist(self):
        assert self.parser._get_value('--meh') == None

    def test_returns_None_when_an_argument_does_not_have_a_value(self):
        assert self.parser._get_value('--bar') == None


class Test_has_or_does_not_have_options(object):

    def setup(self):
        self.parser = Parse(['/bin/tambo', '--foo', 'BAR', '--bar'])
        self.parser.parse_args()

    def test_accepts_lists_and_returns_if_one_matches(self):
        opt = ['a', 'b', '--foo']
        assert self.parser.has(opt) == True

    def test_returns_none_if_cannot_match_from_a_list(self):
        opt = ['a', 'b']
        assert self.parser.has(opt) == False

    def test_deals_with_single_items_that_match(self):
        assert self.parser.has('--foo') == True

    def test_returns_False_when_a_single_item_does_not_match(self):
        assert self.parser.has('--asdadfoo') == False


class TestUnkownCommands(object):

    def setup(self):
        self.parser = Parse(['--foo'])
        self.parser.writer = StringIO()

    def test_catch_unkown_flag(self):
        self.parser.arguments = ['--bar']
        self.parser._build()
        assert self.parser.unkown_commands == ['--bar']

    def test_catch_unkown_flag_including_help(self):
        args = ['--bar', '--help', '-h']
        self.parser.arguments = args
        self.parser._build()
        assert self.parser.unkown_commands == args

    def test_catch_unkown_flag_except_help(self):
        args = ['--bar', '--help', '-h']
        self.parser.catch_help = True
        self.parser.arguments = args
        self.parser._build()
        assert self.parser.unkown_commands == ['--bar']

    def test_catch_unkown_flag_including_version(self):
        args = ['--bar', '--version']
        self.parser.arguments = args
        self.parser._build()
        assert self.parser.unkown_commands == args

    def test_catch_unkown_flag_except_version(self):
        args = ['--bar', '--version']
        self.parser.catch_version = True
        self.parser.arguments = args
        self.parser._build()
        assert self.parser.unkown_commands == ['--bar']



class Test_catches_help(object):

    def setup(self):
        self.parser = Parse(['--foo'])
        self.parser.writer = StringIO()

    def test_does_not_catch_help_if_catch_help_is_not_defined(self):
        self.parser.arguments = ['--help', '-h', 'help']
        assert self.parser.catches_help(force=False) is None

    def test_does_not_catch_version_if_version_is_not_defined(self):
        self.parser.arguments = ['--version', 'version']
        assert self.parser.catches_version(force=False) is None

    def test_catches_only_help_if_it_sees_it_as_an_argument(self):
        self.parser.arguments = ['foo', 'bar']
        self.parser.catch_help = 'this is the help menu'
        assert self.parser.catches_help() == False

    def test_force_catch_version_does_nothing_if_not_defined(self):
        self.parser.arguments = ['foo', 'bar']
        assert self.parser.catches_version() == None

    def test_force_catch_help_does_nothing_if_not_defined(self):
        self.parser.arguments = ['foo', 'bar']
        assert self.parser.catches_help() == None

    def test_catches_a_single_dash_h(self):
        self.parser.arguments = ['-h']
        assert self.parser.check_help is True
        self.parser.catch_help = 'this is the help menu'

        with raises(SystemExit):
            self.parser.catches_help()
        assert self.parser.writer.getvalue() == 'this is the help menu\n'

    def test_catches_double_dash_h(self):
        self.parser.arguments = ['--h']
        self.parser.catch_help = 'this is the help menu'

        with raises(SystemExit):
            self.parser.catches_help()
        assert self.parser.writer.getvalue() == 'this is the help menu\n'

    def test_catches_double_dash_help(self):
        self.parser.arguments = ['--help']
        self.parser.catch_help = 'this is the help menu'

        with raises(SystemExit):
            self.parser.catches_help()
        assert self.parser.writer.getvalue() == 'this is the help menu\n'


class Test_catches_version(object):

    def setup(self):
        self.parser = Parse(['/usr/bin/foo', '--foo'])
        self.parser.writer = StringIO()

    def test_catches_only_version_if_it_sees_it_as_an_argument(self):
        self.parser.arguments = ['foo', 'bar']
        self.parser.catch_version = "version 3"
        assert self.parser.catches_version() == False

    def test_catches_double_dash_version(self):
        self.parser.arguments = ['foo', '--version']
        self.parser.catch_version = "version 3"
        with raises(SystemExit):
            self.parser.catches_version()
        assert self.parser.writer.getvalue() == 'version 3\n'

    def test_catches_version_if_it_sees_it_as_an_argument(self):
        self.parser.arguments = ['foo', 'version']
        self.parser.catch_version = "version 3"
        with raises(SystemExit):
            self.parser.catches_version()
        assert self.parser.writer.getvalue() == 'version 3\n'

