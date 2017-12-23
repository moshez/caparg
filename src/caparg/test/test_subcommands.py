import unittest

import caparg

#from caparg.test import helper_subcommands

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
