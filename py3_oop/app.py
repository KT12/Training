#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 15:54:44 2017

@author: kt12
"""

from observable import Observable
from observer import Observer

class AmericanStockMarket(Observer):
    def update(self, *args, **kwargs):
        print("American stock market received: {0}\n{1}".format(args, kwargs))

class EuropeanStockMarket(Observer):
    def update(self, *args, **kwargs):
        print("European stock market received: {0}\n{1}".format(args, kwargs))

if __name__ == "__main__":
    observable = Observable()
    
    american_observer = AmericanStockMarket()
    observable.register(american_observer)
    
    european_observer = EuropeanStockMarket()
    observable.register(european_observer)
    
    observable.update_observers('Market Rally', something='Hello World')