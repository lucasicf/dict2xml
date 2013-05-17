#!/usr/bin/env python
import unittest
from tests import tests

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(tests))
    unittest.TextTestRunner(verbosity=2).run(suite)
