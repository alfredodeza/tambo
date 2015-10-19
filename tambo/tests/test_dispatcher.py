try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from tambo import dispatcher


class MySubCommand(object):

    def __init__(self, argv):
        self.argv = argv

    def parse_args(self):
        return self.argv


class MyNewSubCommand(object):

    def __init__(self, argv):
        self.argv = argv

    def main(self):
        return self.argv

    def parse_args(self):
        raise RuntimeError('this method should not be called')


class Test_dispatching_mapped_classes(object):

    def test_does_nothing_if_the_mapper_is_empty(self):
        transport = dispatcher.Transport([])
        assert transport.dispatch() is None

    def test_does_nothing_if_the_mapper_cannot_match_the_subcommand(self):
        transport = dispatcher.Transport(['bin/foo', 'bar', 'boo'])
        assert transport.dispatch() is None

    def test_returns_parse_args_called_with_the_instance(self):
        transport = dispatcher.Transport(['/usr/bin/foo', 'foo'])
        transport.mapper = {'foo': MySubCommand}
        result = transport.dispatch()
        assert result == ['foo']

    def test_returns_parse_args_called_with_the_instance_with_main(self):
        transport = dispatcher.Transport(['/usr/bin/foo', 'foo'])
        transport.mapper = {'foo': MyNewSubCommand}
        result = transport.dispatch()
        assert result == ['foo']

    def test_complains_about_unknown_commands(self):
        fake_out = StringIO()
        transport = dispatcher.Transport(['bin/foo', 'bar', 'boo'],
                                         writer=fake_out)
        transport.dispatch()
        assert fake_out.getvalue() == 'Unknown command(s): bar boo\n'
