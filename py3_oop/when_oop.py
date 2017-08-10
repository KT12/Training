#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:49:00 2017

@author: kt12
"""

# Java style (never access attributes directly)

class Color:
    def __init__(self, rgb_value, name):
        self._rgb_value = rgb_value
        self._name = name
        
    def set_name(self, name):
        self._name = name
        
    def get_name(self):
        return self._name


# Python style (direct access)

class Color:
    def __init__(self, rgb_value, name):
        self.rgb_value = rgb_value
        self._name = name
        
    def _set_name(self, name):
        if not name:
            raise Exception('Invalid Name')
        self._name = name
    
    def _get_name(self):
        return self._name

    name = property(_get_name, _set_name)

class Silly:
    def _get_silly(self):
        print('You are getting silly')
        return self._silly
    
    def _set_silly(self, value):
        print('You are making silly {}'.format(value))
        self._silly = value
    
    def _del_silly(self):
        print('Woah, you killed silly!')
        del self._silly
    
    silly = property(_get_silly, _set_silly, _del_silly, 
                     'This is a silly property!')

class Foo:
    @property
    def foo(self):
        return self._foo
    @foo.setter
    def foo(self, value):
        self._foo = value
        
# Equivalent code to previous Silly class

class Silly:
    @property
    def silly(self):
        "This is a silly property"
        print('You are getting silly')
        return self._silly
    
    @silly.setter
    def silly(self, value):
        print('You are making silly {}'.format(value))
        self._silly = value
    
    @silly.deleter
    def silly(self):
        print('Woah, you killed silly!')
        del self._silly