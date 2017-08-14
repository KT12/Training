#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 08:49:51 2017

@author: kt12
"""

# Unit Testing
import unittest

class CheckNumbers(unittest.TestCase):
    def test_int_float(self):
        self.assertEqual(1, 1.0)
    
    def test_str_float(self):
        self.assertEqual(1, '1')

if __name__ == '__main__':
    unittest.main()

# Assertion methods

