
Command Line Traversing Engine
==============================
``tambo`` is a Python package that helps to automatically traverse a tree of
command line options and subcommands dispatching them to mapped classes that
can use any command line parser they want.

Whenever a command line interface of a program grows beyond a few flags and
options it becomes painful to manage all the different options and calls
happenning on a single place.

Even current, widely used command line option parsers in Python suffer from
this case: ``argparse`` and ``optparser`` both require one to explicitly
construct the objects with the parameters when the interface is called.

Not only it forces you to create them before hand, but it also forces one to
make decisions based on what the parsed objects got. For example, if you have
a ``--verbose`` flag you would first need to add it to the parsing object,
something along the lines of ::

    parser = ParserObject()
    options, arguments = parser.parse_args(args)

    parser.add_option('--verbose', action='store_true', help='Increase
    verbosity')

And then to act upon whatever the parser object got, you would do something
like::

    if parser.verbose:
        # do something about verbosity here
        my_program.verbose()

Again, this is all *OK* if you have just a few flags and options, but if you
have, say, 10 or 20 of those, or are combining some with subcommands, you get
highly convoluted methods or functions that are trying to deal with the high
demand for object construction.

Moreover, you are causing that method to create and evaluate *everything* all
the time.

If this was a web framework, it would be a highly inefficient one, wouldn't it?
Executing all the code all the time when a request comes in?

What if we could **map** the command line options to objects and just deal with
the incoming action *once*? Dealing with subcommands would not be up to
a single object that gets constructed, but rather, to a chain of events that
start at the root of an object that has the first level options mapped.

This would be an example of how ``tambo`` would a dispatch of a subcommand::

    parser = tambo.Transport(args)
    parser.mapper = { 'subcommand' : MySubcommandClass }
    parser.dispatch()

The dispatcher would call ``MySubcommandClass``  passing in all the arguments
that came in initially to the constructor and would then call the
``parse_args`` method so that your class can handle the logic of what to do
with the incoming arguments and options there.

The mapping dictionary can alternatively be passed in to the constructor::

    parser = tambo.Transport(args, mapper = { 'subcommand' : MySubCommand })


You can still handle options, boolean flags and anything you want
before hitting ``tambo`` to dispatch to subcommands, and you may use whatever
argument parser you want.

Lets put this abundantly clear:

**You can use whatever argument parser you want**

Command Line Class
------------------
The command line class is what ``tambo`` would look forward when dispatching to
subcommands. They need to follow a couple of constraints but will still allow
to handle the command line arguments in whatever way you want with whatever
library you want.

The most simple class you would need to have a valid dispatch call would look
like this (following the example of the verbose flag from above)::

    class MySubCommand(object):

        def __init__(self, argv):
            self.argv = argv

        def parse_args(self):
            if '--verbose' in self.argv:
                my_program.verbose()

In ``tambo`` internals, the above class will get called when it matches the
mapping defined in your root dictionary, and will receive the ``argv`` argument
which is nothing else than the list of arguments (same as what you would expect
from ``sys.argv`` received on the command line.
If we are following the examples from above, the call would've been like this
on the CLI::

    my_cli subcommand --verbose

Using ``tambo`` parsed args
---------------------------
Although you can use whatever argument parser you want, ``tambo`` also comes
with its own little engine that maps arguments in the command line to values,
that represents the flags and arguments that you expect::

    from tambo import Transport

    class MySubCommand(object):

        def __init__(self, argv):
            self.argv = argv
            self.parser = Transport(self.argv)

        def parse_args(self):
            if self.parser.has('--verbose'):
                my_program.verbose()

In the above case ``--verbose`` wasn't expecting a value assigned so later we
just verified it existed by calling ``has('--verbose')``.

The ``Transport`` object allows you to define all the flags and options you need as
a tuple or a list so that they can be taken into account when mapping the
values. If you want to define aliases, you can do so by grouping them in a list
within the main list passed in to ``Transport``::

    >>> from tambo import Transport
    >>> options = [['-i', '--import'], '--verbose']
    >>> parse = Transport(options)
    >>> sys_argv = ['/bin/myapp', '-i', 'somevalue']
    >>> parse.parse_args(sys_argv)
    >>> parse.get('-i')
    'somevalue'
    >>> parse.get('--import')
    'somevalue'

So aliases work by grouping them together in a list, but what happens on
boolean flags? You can check them by calling the ``has`` method::


    >>> sys_argv = ['/bin/myapp', '--verbose']
    >>> parse.parse_args(sys_argv)
    >>> parse.has('-i')
    False
    >>> parse.has('--verbose')
    True

If you need to check for boolean flags in batch, you can pass in a list::

    >>> sys_argv = ['/bin/myapp', '--verbose']
    >>> parse.parse_args(sys_argv)
    >>> parse.has('-i')
    False
    >>> parse.has(['-v', '--verbose'])
    True



Help generation
---------------
A common problem for subcommands and command line tools that have these is
generating help in a semi-automated way. ``tambo`` has a way to do this for
subcommands that are mapped by calling the help property if there is one and
would in turn outpout that information when called::

    class MySubcommandClass(object):

        help = 'A sub-command that does some stuff'


And then in the handler for your arguments it will automaticall check for the
presence of the help attribute to display it if needed::

    # parser is an instance of the Transport class from ``tambo``
    parser.parse_args()


Which would make sure that when help is set on the command line it would output
something like this::

    my_cli_tool version 0.0.1

    SubCommands:

    subcommand          A sub-command that does some stuff

This is again, entirely optional, as you can avoid making those calls to catch
help by telling the ``Transport`` class to avoid checking for it::

    parser = Transport(sys.argv, check_help=False)

If for some reason you wanted to force printing the help menu, for example when
no options have been matched, you can also do that with ``print_help()``

::

    parser = Transport(sys.argv, check_help=False)

    if parser.has('--verbose'):
        my_program.verbose()
    else:
        parser.print_help()
    
