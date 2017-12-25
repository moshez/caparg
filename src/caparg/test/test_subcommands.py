"""
Testing for Captain Arguments' sub-commmands!
"""
import unittest

import caparg


class SubcommandTester(unittest.TestCase):

    """
    Subcommand parsing tests
    """

    def test_simple(self):
        """
        Parsing a subcommand with one positional returns subcommand and positional
        """
        simple = caparg.command('',
                                caparg.command('drink',
                                               caparg.positional('what',
                                                                 type=str)))
        parsed = dict(simple.parse(['drink', 'something']))
        self.assertEquals(parsed.pop('what'), 'something')
        self.assertEquals(list(parsed.pop('__caparg_subcommand__')),
                          ['drink'])
        self.assertEquals(parsed, {})

    def test_optional(self):
        """
        Not passing in an optional argument causes nothing to be in the return
        """
        simple = caparg.command('',
                                caparg.command('eat',
                                               what=caparg.option(type=str)))
        parsed = dict(simple.parse(['eat']))
        self.assertEquals(list(parsed.pop('__caparg_subcommand__')),
                          ['eat'])
        self.assertEquals(parsed, {})

    def test_inherit(self):
        """
        Subcommands inherit options from parents and grandparents
        """
        simple = caparg.command('',
                                caparg.options(where=caparg.option(type=str)),
                                caparg.command('eat',
                                               caparg.command('lunch')))
        parsed = dict(simple.parse(['eat', 'lunch', '--where', 'cafe']))
        self.assertEquals(list(parsed.pop('__caparg_subcommand__')),
                          ['eat', 'lunch'])
        self.assertEquals(parsed.pop('where'), 'cafe')
        self.assertEquals(parsed, {})

    def test_no_required(self):
        """
        Not passing in a required argument raises ParseError
        """
        command = caparg.command
        simple = command('',
                         command('eat',
                                 where=caparg.option(type=str, required=True)))
        with self.assertRaises(caparg.ParseError):
            simple.parse(['eat'])

    def test_no_command(self):
        """
        If no subcommand is given, ParseError is raised
        """
        simple = caparg.command('',
                                caparg.command('eat'))
        with self.assertRaises(caparg.ParseError):
            simple.parse(['drink'])

    def test_boolean_false(self):
        """
        Not passing in --option results in option being false
        """
        simple = caparg.command('',
                                caparg.command('eat',
                                               alot=caparg.option(type=bool)))
        self.assertFalse(simple.parse(['eat'])['alot'])

    def test_boolean_true(self):
        """
        Passing in --option results in option being true
        """
        simple = caparg.command('',
                                caparg.command('eat',
                                               alot=caparg.option(type=bool)))
        self.assertTrue(simple.parse(['eat', '--alot'])['alot'])

    def test_default(self):
        """
        Default for string is empty string
        """
        command = caparg.command
        option = caparg.option
        simple = command('',
                         command('eat',
                                 where=option(type=str,
                                              have_default=True)))
        self.assertEquals(simple.parse(['eat'])['where'], '')
