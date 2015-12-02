#!/usr/bin/env python

import unittest
from request_svc import make_call


class TestSomething(unittest.TestCase):

    def test_something(self):
        params = {'q': 'kroq'}
        result = make_call(params)
        self.assertEqual(result['status'], 'OK')


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(
        TestSomething)

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
