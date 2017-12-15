import sys
import typing

import caparg

parser = caparg.command('',
    caparg.options(
        messages=caparg.option(type=str, required=True),
        config=caparg.option(type=str, required=True),
    ),
    caparg.command('add',
        name=caparg.option(type=str, required=True),
        cmd=caparg.option(type=str, required=True),
        arg=caparg.option(type=typing.List[str], have_default=True),
        env=caparg.option(type=typing.Dict[str,str], have_default=True),
        uid=caparg.option(type=int),
        gid=caparg.option(type=int),
        extras=caparg.option(type=str),
    ),
    caparg.command('remove',
        name=caparg.option(type=str, required=True),
    ),
    caparg.command('restart',
        name=caparg.option(type=str, required=True),
    ),
    caparg.command('restart-all',
    ),
    caparg.command('remote',
        caparg.options(verbose=caparg.option(type=bool, required=True)),
        caparg.command('remove',
            caparg.positional(name='name', type=bool, required=True),
        ),
    ),
    caparg.command('remote add',
        caparg.positional(name='name', type=bool, required=True),
        caparg.positional(name='url', type=bool, required=True),
    ),
)

ret = parser.parse(sys.argv[1:])
print(ret)
