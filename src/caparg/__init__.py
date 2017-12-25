"""
Captain arguments -- ready for subcommand!

A more functional way of doing argument parsing.
"""

from caparg._api import command, option, positional, options, ParseError
from caparg._version import __version__ as _my_version

__version__ = _my_version.short()

__all__ = ['command', 'option', 'positional', 'options', 'ParseError',
           '__version__']
