#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 15:52:58 2017

@author: kt12
"""

from abc import ABCMeta, abstractmethod

class Observer(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def update(self, *args, **kwargs):
        pass