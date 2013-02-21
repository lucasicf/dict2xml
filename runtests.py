#!/usr/bin/env python
import unittest
from tests import correct, wrong

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromModule(correct))
    suite.addTests(loader.loadTestsFromModule(wrong))
    unittest.TextTestRunner(verbosity=2).run(suite)
