import unittest

import caparg

from caparg.test import helper_subcommands

class SubcommandTester(unittest.TestCase):

    def test_simple(self):
        parsed = helper_subcommands.parser.parse(['remove', 'something'])
        raise ValueError(parsed)
