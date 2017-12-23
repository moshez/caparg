import unittest

import caparg

class SubcommandTester(unittest.TestCase):

    def test_simple(self):
        simple = caparg.command('',
                     caparg.command('drink',
                                    caparg.positional('what', type=str)))
        parsed = dict(simple.parse(['drink', 'something']))
        self.assertEquals(parsed.pop('what'), 'something')
        self.assertEquals(list(parsed.pop('__caparg_subcommand__')),
                          ['drink'])
        self.assertEquals(parsed, {})

    def test_optional(self):
        simple = caparg.command('',
                     caparg.command('eat',
                                    what=caparg.option(type=str)))
        parsed = dict(simple.parse(['eat']))
        self.assertEquals(list(parsed.pop('__caparg_subcommand__')),
                          ['eat'])
        self.assertEquals(parsed, {})

    def test_inherit(self):
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
        simple = caparg.command('',
                     caparg.command('eat',
                               where=caparg.option(type=str, required=True)))
        with self.assertRaises(caparg.ParseError):
            simple.parse(['eat'])

    def test_no_command(self):
        simple = caparg.command('',
                     caparg.command('eat'))
        with self.assertRaises(caparg.ParseError):
            simple.parse(['drink'])

    def test_boolean_false(self):
        simple = caparg.command('',
                     caparg.command('eat',
                         alot=caparg.option(type=bool)))
        self.assertFalse(simple.parse(['eat'])['alot'])

    def test_boolean_true(self):
        simple = caparg.command('',
                     caparg.command('eat',
                         alot=caparg.option(type=bool)))
        self.assertTrue(simple.parse(['eat', '--alot'])['alot'])
