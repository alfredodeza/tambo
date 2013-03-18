try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from tambo import dispatcher
from mock import Mock


class Test_dispatching_mapped_classes(object):

    def test_does_nothing_if_the_mapper_is_empty(self):
        transport = dispatcher.Transport([])
        assert transport.dispatch() is None

    def test_does_nothing_if_the_mapper_cannot_match_the_subcommand(self):
        transport = dispatcher.Transport(['bin/foo', 'bar', 'boo'])
        assert transport.dispatch() is None

    def test_returns_parse_args_called_with_the_instance(self):
        transport = dispatcher.Transport(['/usr/bin/foo', 'foo'])
        MyFoo = Mock()
        MyFoo.parse_args = Mock(return_value="Some string")
        MyFoo.return_value = MyFoo
        transport.mapper = {'foo': MyFoo}
        result = transport.dispatch()

        assert result == "Some string"
        assert MyFoo.call_args[0][0] == ['foo']

    def test_complains_about_unkown_commands(self):
        fake_out = StringIO()
        transport = dispatcher.Transport(['bin/foo', 'bar', 'boo'],
                                         writer=fake_out)
        transport.dispatch()
        assert fake_out.getvalue() == 'Unknown command(s): bar boo\n'
