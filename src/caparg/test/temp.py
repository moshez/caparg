parser = caparg.command('',
    messages=caparg.option(type=str, required=True),
    config=caparg.option(type=str, required=True),
    caparg.command('add',
        name=caparg.option(type=str, required=True),
        cmd=caparg.option(type=str, required=True),
        arg=caparg.option(type=typing.List[str], have_default=True),
        env=caparg.option(type=typing.Dict[str], have_default=True),
        uid=caparg.option(type=int),
        gid=caparg.option(type=int),
    ),
    caparg.command('remove',
        name=caparg.option(type=str, required=True).
    ),
    caparg.command('restart',
        name=caparg.option(type=str, required=True).
    ),
    caparg.command('restart-all'),
)
parser = caparg.command('',
    caparg.command('commit', ...)
    caparg.command('remote',
                   verbose=caparg.option(type=bool),
    ),
    caparg.command('remote add', ...)
)

@attr.s(frozen=True)
class Parsed(object):
    values = attr.ib()
    subcommand = attr.ib()
    
    
