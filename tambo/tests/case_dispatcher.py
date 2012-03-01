from tambo import dispatcher
from mock import Mock
import konira


describe "dispatching mapped classes":

    it "does nothing if the mapper is empty":
        transport = dispatcher.Transport([])
        assert transport.dispatch() is None

    it "does nothing if the mapper cannot match the subcommand":
        transport = dispatcher.Transport(['bin/foo', 'bar', 'boo'])
        assert transport.dispatch() is None

    it "returns parse_args called with the instance":
        transport = dispatcher.Transport(['/usr/bin/foo', 'foo'])
        MyFoo = Mock()
        MyFoo.parse_args = Mock(return_value="Some string")
        MyFoo.return_value = MyFoo
        transport.mapper = {'foo' : MyFoo}
        result = transport.dispatch()

        assert result == "Some string"
        assert MyFoo.call_args[0][0] == ['foo']
