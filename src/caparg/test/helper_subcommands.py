"""
Really complicated command-line parser definition.
"""

import typing

from caparg import command, options, option, positional

PARSER = command('',
                 # These are common options.
                 # They will be inherited by all sub-commands.
                 options(
                     messages=option(type=str, required=True),
                     config=option(type=str, required=True),
                 ),
                 # This is a subcommand, "add"
                 # It takes a bewildering array of options!
                 command('add',
                         name=option(type=str, required=True),
                         cmd=option(type=str, required=True),
                         arg=option(type=typing.List[str], have_default=True),
                         env=option(type=typing.Dict[str, str],
                                    have_default=True),
                         uid=option(type=int),
                         gid=option(type=int),
                         extras=option(type=str)),
                 # This is a subcommand, "remove"
                 # It takes one option
                 command('remove',
                         name=option(type=str, required=True)),
                 # This is a subcommand, "restart"
                 # It takes one option
                 command('restart',
                         name=option(type=str, required=True)),
                 # This is a subcommand, "restart-all"
                 # It takes no options.
                 command('restart-all'),
                 # This is a subcommand, "remote".
                 # It can be called directly...
                 command('remote',
                         options(verbose=option(type=bool)),
                         # ...or with a sub-subcommand 'remove'
                         command('remove',
                                 positional(name='name', type=str))),
                 # It is also possible to put sub-sub-commands at the top-level.
                 # In that case, they are separated with whitespace.
                 command('remote add',
                         positional(name='name', type=str),
                         positional(name='url', type=str)))
