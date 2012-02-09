
Command Line Traversing Engine
==============================
``tempu`` is a Python package that helps to automatically traverse a tree of
command line options and subcommands.

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
have, say, 10 or 20 or those, or are combining some with subcommands, you get
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

This would be an example of how ``tampu`` would a dispatch of a subcommand::

    tampu.mapper = { 'subcommand' : MySubcommandClass }
    tampu.dispatch()

The dispatcher would call ``MySubcommandClass``  passing in all the arguments
that came in initially to the constructor and would then call the
``parse_args`` method so that your class can handle the logic of what to do
with the incoming arguments and options there.

You can still handle options, boolean flags and anything however you want
before hitting tampu to dispatch to subcommands, and you may use whatever
argument parser you want.

Help generation
---------------
A common problem for subcommands and command line tools that have these is
generating help in a semi-automated way. ``tampu`` has a way to do this for
subcommands that are mapped by calling the help property if there is one and
would in turn outpout that information when called::

    class MySubcommandClass(object):

        help = 'A sub-command that does some stuff'


And then in the handler for your arguments you would set the ``catch_help``
call::

    tampu.catch_help()

Which would make sure that when help is set on the command line it would output
something like this::

    my_cli_tool version 0.0.1

    SubCommands:

    subcommand          A sub-command that does some stuff

