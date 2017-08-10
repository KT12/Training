#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 21:57:42 2017

@author: kt12
"""

from collections import Container

class OddContainer():
    def __contains__(self, x):
        if not isinstance(x, int) or not x % 2:
            return False
        return True
    
' Example of duck typing'

odd_container = OddContainer()

isinstance(odd_container, Container)

issubclass(OddContainer, Container)

# Abstract base classes

import abc

class MediaLoader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def play(self):
        pass
    
    @abc.abstractproperty
    def ext (self):
        pass
    
    @classmethod
    def __subclasshook__(cls, C):
        if cls is MediaLoader:
            attrs = set(dir(C))
            if set(cls.__abstractmethods__) <= attrs:
                return True
        return NotImplemented
    
class Wav(MediaLoader):
    pass

class Ogg(MediaLoader):
    ext = '.ogg'
    def play(self):
        pass