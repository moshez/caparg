"""
Exercise option parsing on a command line.
"""
from __future__ import print_function
import sys

from caparg.test import helper_subcommands

if __name__ != '__main_':
    raise ImportError("module cannot be imported")

sys.stdout.write(str(helper_subcommands.PARSER.parse(sys.argv[1:])) + "\n")
