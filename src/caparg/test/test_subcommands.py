"""
Testing for Captain Arguments' sub-commmands!
"""
from typing import List
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
        self.assertEqual(parsed.pop('what'), 'something')
        self.assertEqual(list(parsed.pop('__caparg_subcommand__')),
                          ['drink'])
        self.assertEqual(parsed, {})

    def test_evolution(self):
        """
        You can evolve a command to a different name
        """
        eat = caparg.command('eat')
        drink = eat.rename('drink')
        simple = caparg.command('', drink)
        parsed = dict(simple.parse(['drink']))
        self.assertEqual(list(parsed.pop('__caparg_subcommand__')),
                          ['drink'])
        self.assertEqual(parsed, {})

    def test_optional(self):
        """
        Not passing in an optional argument causes nothing to be in the return
        """
        simple = caparg.command('',
                                caparg.command('eat',
                                               what=caparg.option(type=str)))
        parsed = dict(simple.parse(['eat']))
        self.assertEqual(list(parsed.pop('__caparg_subcommand__')),
                          ['eat'])
        self.assertEqual(parsed, {})

    def test_inherit(self):
        """
        Subcommands inherit options from parents and grandparents
        """
        simple = caparg.command('',
                                caparg.options(where=caparg.option(type=str)),
                                caparg.command('eat',
                                               caparg.command('lunch')))
        parsed = dict(simple.parse(['eat', 'lunch', '--where', 'cafe']))
        self.assertEqual(list(parsed.pop('__caparg_subcommand__')),
                          ['eat', 'lunch'])
        self.assertEqual(parsed.pop('where'), 'cafe')
        self.assertEqual(parsed, {})

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
        self.assertEqual(simple.parse(['eat'])['where'], '')

    def test_dashes(self):
        """
        Underscores are interpreted as dashes on the command-line
        """
        command = caparg.command
        option = caparg.option
        simple = command('',
                         command('do_it',
                                 good_thing=option(type=str)))
        parsed = simple.parse(['do-it', '--good-thing', 'stuff'])
        self.assertEqual(parsed['good_thing'], 'stuff')

    def test_list_str(self):
        """
        option(type=List[str]) returns list of strings
        """
        command = caparg.command
        option = caparg.option
        simple = command('',
                         command('eat',
                                 what=option(type=List[str])))
        parsed = simple.parse(['eat', '--what', 'rice', '--what', 'beans'])
        self.assertEqual(parsed['what'], ['rice', 'beans'])

    def test_empty_list_str(self):
        """
        An empty list without a default does not appear in result
        """
        command = caparg.command
        option = caparg.option
        simple = command('',
                         command('eat',
                                 what=option(type=List[str])))
        parsed = simple.parse(['eat'])
        self.assertNotIn('what', parsed)

    def test_empty_list_str_default(self):
        """
        An empty list with a default is empty in result
        """
        command = caparg.command
        option = caparg.option
        simple = command('',
                         command('eat',
                                 what=option(type=List[str],
                                             have_default=True)))
        parsed = simple.parse(['eat'])
        self.assertEqual(list(parsed['what']), [])
