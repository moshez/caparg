import sys

from caparg.test import helper_subcommands

ret = helper_subcommands.parser.parse(sys.argv[1:])
print(ret)
