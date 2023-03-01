import unittest

from importlib import import_module

#------------------------------------------------------------------------------

from parameterized import parameterized

parameters = [
        ["Idx", "idx", "main",],
        ["Parser", "idx.parser", "parse"],
    ]

class Test_ImportSequence(unittest.TestCase):

    @parameterized.expand(parameters)
    def test_import(self, name, package, entry_point):
        self.assertTrue ( import_module(package), f"'import {package}' failed" )

    @parameterized.expand(parameters)
    def test_entry_point_exists(self, name, package, entry_point):
        m = import_module(package)
        self.assertTrue ( hasattr(m, entry_point), f"{package} missing '{entry_point}'")

#------------------------------------------------------------------------------
