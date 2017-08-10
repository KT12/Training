#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 15:46:02 2017

@author: kt12
"""

# http://www.giantflyingsaucer.com/blog/?p=5117

class Observable(object):
    def __init__(self):
        self.observers = []
    
    def register(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)
    
    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
    
    def unregister_all(self):
        if self.observers:
            del self.observers[:]
    
    def update_observers(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(*args, **kwargs)