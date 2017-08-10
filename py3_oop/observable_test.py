#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 17:43:52 2017

@author: kt12
"""

import unittest

from observable import Observable
from observer import Observer

class AnObserver(Observer):
    def __init__(self):
        self.args = []
        self.kwargs = {}
    
    def update(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return

class observable_test(unittest.TestCase):
    
    def setUp(self):
        self.observable = Observable()
        
        self.observer1 = AnObserver()
        self.observer2 = AnObserver()
        self.observer3 = AnObserver()
    
    def test_remove_all(self):
        self.observable.register(self.observer1)
        self.observable.register(self.observer2)
        self.observable.register(self.observer3)
        
        self.observable.unregister_all()
        
        # Should be zero registered
        self.assertEqual(len(self.observable.observers), 0)
    
    def test_register(self):
        self.observable.register(self.observer1)
        self.observable.register(self.observer2)
        self.observable.register(self.observer3)
        
        # Should be three registered
        self.assertEqual(len(self.observable.observers), 3)
        self.observable.unregister_all()
    
    def test_unregister(self):
        self.observable.register(self.observer1)
        self.observable.register(self.observer2)
        self.observable.register(self.observer3)
        
        self.observable.unregister(self.observer2)
        self.observable.unregister(self.observer3)
        
        # Should be 1 registered
        self.assertEqual(len(self.observable.observers), 1)
        self.observable.unregister_all()
    
    def test_update_observers(self):
        self.observable.register(self.observer1)
        
        self.observable.update_observers('abc', msg='123')
        self.assertEqual(self.observer1.args[0], 'abc')
        self.assertEqual(self.observer1.kwargs['msg'], '123')
        self.observable.unregister_all()

if __name__ == '__main__':
    unittest.main()