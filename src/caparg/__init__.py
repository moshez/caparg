"""
Captain arguments -- ready for subcommand!

A more functional way of doing argument parsing.
"""

from caparg._api import command, option, positional, options, ParseError

__all__ = ['command', 'option', 'positional', 'options', 'ParseError']
