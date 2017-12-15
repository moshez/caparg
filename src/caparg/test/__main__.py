import argparse
import sys

def mkparser(*things):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for thing in things:
        thing.add_to(parser, subparsers)
    return parser.parse_args

@attr.s(frozen=True)
class argument(object):
    name = attr.ib()
    type = attr.ib(default=str)
    required = attr.ib(default=False)

    def add_to(self, parser, subparser):
        parser.add_argument(name=self.name, required=self.required)

@attr.s(frozen=True)
class Subcommand(object):
    name = attr.ib()
    things = attr.ib()

    @classmethod
    def create(cls, name, *things):
        return cls(name, things)

subcommand = 

parser = mkparser(
    subcommand(name="build",
    ),
    subcommand(name="run",
        argument("--port", type=int, required=True),
    ),
    subcommand(name="test",
        argument("--full", type=bool),
    ),
    subcommand(name="push",
    ),
)

print(parser(sys.argv[1:]))
