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

    def test_failure(self):
        simple = caparg.command('',
                     caparg.command('eat',
                               where=caparg.option(type=str, required=True)))
        with self.assertRaises(caparg.ParseError):
            simple.parse(['eat'])
