import sys
import typing

import caparg

parser = caparg.command('',
    # These are common options.
    # They will be inherited by all sub-commands.
    caparg.options(
        messages=caparg.option(type=str, required=True),
        config=caparg.option(type=str, required=True),
    ),
    # This is a subcommand, "add"
    # It takes a bewildering array of options!
    caparg.command('add',
        name=caparg.option(type=str, required=True),
        cmd=caparg.option(type=str, required=True),
        arg=caparg.option(type=typing.List[str], have_default=True),
        env=caparg.option(type=typing.Dict[str,str], have_default=True),
        uid=caparg.option(type=int),
        gid=caparg.option(type=int),
        extras=caparg.option(type=str),
    ),
    # This is a subcommand, "remove"
    # It takes one option
    caparg.command('remove',
        name=caparg.option(type=str, required=True),
    ),
    # This is a subcommand, "restart"
    # It takes one option
    caparg.command('restart',
        name=caparg.option(type=str, required=True),
    ),
    # This is a subcommand, "restart-all"
    # It takes no options.
    caparg.command('restart-all',
    ),
    # This is a subcommand, "remote".
    # It can be called directly...
    caparg.command('remote',
        caparg.options(verbose=caparg.option(type=bool, required=True)),
        # ...or with a sub-subcommand 'remove'
        caparg.command('remove',
            caparg.positional(name='name', type=str),
        ),
    ),
    # It is also possible to put sub-sub-commands at the top-level.
    # In that case, they are separated with whitespace.
    caparg.command('remote add',
        caparg.positional(name='name', type=str),
        caparg.positional(name='url', type=str),
    ),
)

ret = parser.parse(sys.argv[1:])
print(ret)
