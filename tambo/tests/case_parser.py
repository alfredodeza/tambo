import konira
from tambo import Parse
import sys
if sys.version < '3':
    from cStringIO import StringIO
else:
    from io import StringIO


describe "parsing arguments":


    it "removes the first item in the list always":
        parser = Parse([])
        parser.parse_args()
        assert parser.arguments == []


    it "matches an option in arguments":
        parser = Parse(['/usr/bin/foo', '--foo'])
        parser.options = ['--foo']
        parser.parse_args()

        assert parser == {} # No key/values
        assert parser.has('--foo') # But it does exist


    it "matches arguments with no values":
        parser = Parse(['/usr/bin/foo', '--foo'])
        parser.parse_args()
        assert parser._arg_count    == {'--foo' : 0}
        assert parser._count_arg[0] == '--foo'


    it "matches arguments with values":
        parser = Parse(['/usr/bin/foo', '--foo', 'BAR'])
        parser.parse_args()
        assert parser._arg_count['--foo'] == 0
        assert parser._count_arg[1]       == 'BAR'


    it "matches valid configured options only":
        parser = Parse(['/bin/tambo', '--foo', 'off', '--meh'])
        parser.options = ['--foo']
        parser.parse_args()
        assert parser.has('--foo')
        assert parser.has('--meh')
        assert parser.get('--foo') == 'off'
        assert parser.get('--meh') is None


    it "matches mixed values and arguments":
        parser = Parse(['/bin/tambo', '--foo', 'FOO', '--bar'])
        parser.parse_args()
        assert parser._arg_count['--foo'] == 0
        assert parser._arg_count['--bar'] == 2
        assert parser._count_arg[1]       == 'FOO'
        assert parser._count_arg.get(3)   == None


    it "deals with lists of lists in options":
        parser = Parse(['/bin/tambo', '--bar'])
        parser.options = ['--foo', ['--bar', 'bar']]
        parser.parse_args()
        assert parser._arg_count['--bar'] == 0
        assert parser.get('--bar') is None



describe "get values from arguments":


    before each:
        self.parser = Parse(['/bin/tambo', '--foo', 'BAR', '--bar'])
        self.parser.parse_args()


    it "returns a valid value from a matching argument":
        assert self.parser._get_value('--foo') == 'BAR'


    it "returns None when an argument does not exist":
        assert self.parser._get_value('--meh') == None


    it "returns None when an argument does not have a value":
        assert self.parser._get_value('--bar') == None



describe "has or does not have options":


    before each:
        self.parser = Parse(['/bin/tambo', '--foo', 'BAR', '--bar'])
        self.parser.parse_args()


    it "accepts lists and returns if one matches":
        opt = ['a', 'b', '--foo']
        assert self.parser.has(opt) == True


    it "returns none if cannot match from a list":
        opt = ['a', 'b']
        assert self.parser.has(opt) == False


    it "deals with single items that match":
        assert self.parser.has('--foo') == True


    it "returns False when a single item does not match":
        assert self.parser.has('--asdadfoo') == False



describe "catches help":


    before each:
        self.parser = Parse(['--foo'])
        self.parser.writer = StringIO()


    it "does not catch help if catch_help is not defined":
        self.parser.arguments = ['--help', '-h', 'help']
        assert self.parser.catches_help() is None


    it "does not catch version if version is not defined":
        self.parser.arguments = ['--version', 'version']
        assert self.parser.catches_version() is None


    it "catches only help if it sees it as an argument":
        self.parser.arguments = ['foo', 'bar']
        self.parser.catch_help = 'this is the help menu'
        assert self.parser.catches_help() == False


    it "catches a single dash h":
        self.parser.arguments = ['-h']
        assert self.parser.check_help is True
        self.parser.catch_help = 'this is the help menu'

        raises SystemExit: self.parser.catches_help()
        assert self.parser.writer.getvalue() == 'this is the help menu\n'


    it "catches double dash h":
        self.parser.arguments = ['--h']
        self.parser.catch_help = 'this is the help menu'

        raises SystemExit: self.parser.catches_help()
        assert self.parser.writer.getvalue() == 'this is the help menu\n'


    it "catches double dash help":
        self.parser.arguments = ['--help']
        self.parser.catch_help = 'this is the help menu'

        raises SystemExit: self.parser.catches_help()
        assert self.parser.writer.getvalue() == 'this is the help menu\n'



describe "catches version":


    before each:
        self.parser = Parse(['/usr/bin/foo', '--foo'])
        self.parser.writer = StringIO()


    it "catches only version if it sees it as an argument":
        self.parser.arguments = ['foo', 'bar']
        self.parser.catch_version = "version 3"
        assert self.parser.catches_version() == False


    it "catches double dash version":
        self.parser.arguments = ['foo', '--version']
        self.parser.catch_version = "version 3"
        raises SystemExit: self.parser.catches_version()
        assert self.parser.writer.getvalue() == 'version 3\n'


    it "catches version if it sees it as an argument":
        self.parser.arguments = ['foo', 'version']
        self.parser.catch_version = "version 3"
        raises SystemExit: self.parser.catches_version()
        assert self.parser.writer.getvalue() == 'version 3\n'

